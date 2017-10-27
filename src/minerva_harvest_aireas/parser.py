import datetime
import json

from minerva.harvest.plugin_api_trend import HarvestParserTrend
from minerva.storage.trend.datapackage import DefaultPackage
from minerva.storage.trend.granularity import create_granularity


class Parser(HarvestParserTrend):
    def __init__(self, config):
        self.config = config

    def load_packages(self, stream, name):
        reading_mapppings = [
            ('AmbHum', lambda readings: readings.get('AmbHum')),  # 84.37
            ('PM1', lambda readings: readings.get('PM1')),      # 3.0
            ('WBGT', lambda readings: readings.get('WBGT')),     # 0.0
            ('UFP', lambda readings: readings.get('AmbHum')),      # 0.0
            ('PM25', lambda readings: readings.get('AmbHum')),     # 3.0
            ('Ozon', lambda readings: readings.get('AmbHum')),     # 0.0
            ('PM10', lambda readings: readings.get('AmbHum')),     # 6.0
            ('Temp', lambda readings: readings.get('AmbHum')),     # 12.92
            ('RelHum', lambda readings: readings.get('AmbHum')),   # 57.35
            ('AmbTemp', lambda readings: readings.get('AmbHum')),  # 13.23
            ('NO2', lambda readings: readings.get('AmbHum')),      # 63.9
            ('GPS.lat', lambda readings: readings.get('GPS')['lat']),
            ('GPS.lon', lambda readings: readings.get('GPS')['lon'])  #
                        #   "lat": 5134.187115,
                        #   "lon": 449.162761
                        # }
        ]

        data = json.load(stream)

        rows_by_timestamp = {}

        for measurement in data:
            timestamp_int = measurement['last_measurement']['calibrated']['when']['$date']

            timestamp = datetime.datetime.fromtimestamp(
                timestamp_int / 1000.0, None
            )

            rows = rows_by_timestamp.get(timestamp)

            if rows is None:
                rows = []
                rows_by_timestamp[timestamp] = rows

            readings = measurement['last_measurement']['calibrated']['readings']
            reading_values = [
                mapping(readings)
                for meas_name, mapping in reading_mapppings
            ]

            rows.append((
                'airbox={}'.format(measurement['_id']),
                reading_values
            ))

        trend_names = [meas_name for meas_name, mapping in reading_mapppings]

        for timestamp, rows in rows_by_timestamp.items():
            yield DefaultPackage(
                create_granularity('1 day'),
                timestamp,
                trend_names,
                rows
            )
