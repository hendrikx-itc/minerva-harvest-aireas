import datetime
import json

from minerva.harvest.plugin_api_trend import HarvestParserTrend
from minerva.storage.trend.datapackage import DefaultPackage
from minerva.storage.trend.granularity import create_granularity


class Parser(HarvestParserTrend):
    def __init__(self, config):
        self.config = config

    def load_packages(self, stream, name):
        reading_names = [
            'AmbHum',   # 84.37
            'PM1',      # 3.0
            'WBGT',     # 0.0
            'UFP',      # 0.0
            'PM25',     # 3.0
            'Ozon',     # 0.0
            'PM10',     # 6.0
            'Temp',     # 12.92
            'RelHum',   # 57.35
            'AmbTemp',  # 13.23
            'NO2',      # 63.9
            'GPS'       #
                        #   "lat": 5134.187115,
                        #   "lon": 449.162761
                        # }
        ]

        data = json.load(stream)

        rows = []

        for measurement in data:
            timestamp_str = measurement['last_measurement']['calibrated']['when']['$date']
            readings = measurement['last_measurement']['calibrated']['readings']
            reading_values = [
                readings.get(meas_name)
                for meas_name in reading_names
            ]

            rows.append((
                'airbox={}'.format(measurement['_id']),
                reading_values
            ))

        yield DefaultPackage(
            create_granularity('1 day'),
            datetime.datetime.utcnow(),
            reading_names,
            rows
        )

