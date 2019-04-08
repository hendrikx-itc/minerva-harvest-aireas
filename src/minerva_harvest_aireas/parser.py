import datetime
import json

from minerva.harvest.plugin_api_trend import HarvestParserTrend
from minerva.storage.trend.datapackage import DataPackage, DataPackageType
from minerva.directory.entityref import entity_alias_ref_class
from minerva.storage.trend.trend import Trend
from minerva.storage.trend.granularity import create_granularity

AireasPackageType = DataPackageType(entity_alias_ref_class('airbox', 'airbox'), lambda x: 'airbox', 'airbox')

class Parser(HarvestParserTrend):
    def __init__(self, config):
        self.config = config

    def packages(self, stream, name):
        reading_mapppings = [
            ('AmbHum', lambda readings: readings.get('AmbHum')),
            ('PM1', lambda readings: readings.get('PM1')),
            ('UFP', lambda readings: readings.get('UFP')),
            ('PM25', lambda readings: readings.get('PM25')),
            ('Ozon', lambda readings: readings.get('Ozon')),
            ('PM10', lambda readings: readings.get('PM10')),
            ('Temp', lambda readings: readings.get('Temp')),
            ('RelHum', lambda readings: readings.get('RelHum')),
            ('AmbTemp', lambda readings: readings.get('AmbTemp')),
            ('NO2', lambda readings: readings.get('NO2')),
            ('GPS.lat', lambda readings: readings.get('GPS')['lat']),
            ('GPS.lon', lambda readings: readings.get('GPS')['lon'])
        ]

        data = json.load(stream)

        rows = []

        for measurement in data:
            timestamp_int = measurement['last_measurement']['calibrated']['when']['$date']

            timestamp = datetime.datetime.fromtimestamp(
                timestamp_int / 1000.0, None
            )

            readings = measurement['last_measurement']['calibrated']['readings']
            reading_values = [
                str(measurement['_id']),
                timestamp,
                [
                    mapping(readings)
                    for meas_name, mapping in reading_mapppings
                ]
            ]

            rows.append(reading_values)

        trends = [Trend(0, meas_name, float, 0, meas_name) for meas_name, mapping in reading_mapppings]

        yield DataPackage(
            AireasPackageType,
            create_granularity('1 day'),
            trends,
            rows
        )
