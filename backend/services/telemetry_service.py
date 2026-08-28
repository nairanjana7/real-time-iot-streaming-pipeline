from datetime import datetime, timezone

from influxdb_client import Point

from backend.database.influx import (
    write_api,
    query_api,
)

from backend.core.config import settings


class TelemetryService:

    @staticmethod
    def write(request):

        point = (
            Point("telemetry")
            .tag("machine_id", str(request.machine_id))
            .field("temperature", request.temperature)
            .field("pressure", request.pressure)
            .field("humidity", request.humidity)
            .field("vibration", request.vibration)
            .field("rpm", request.rpm)
            .time(datetime.now(timezone.utc))
        )

        write_api.write(
            bucket=settings.INFLUX_BUCKET,
            record=point,
        )

        return {
            "message": "Telemetry stored successfully."
        }

    @staticmethod
    def latest(machine_id: int):

        query = f'''
from(bucket:"{settings.INFLUX_BUCKET}")
|> range(start: -24h)
|> filter(fn:(r)=>r._measurement=="telemetry")
|> filter(fn:(r)=>r.machine_id=="{machine_id}")
|> last()
'''

        tables = query_api.query(
            query=query,
            org=settings.INFLUX_ORG,
        )

        result = []

        for table in tables:
            for record in table.records:
                result.append(
                    {
                        "field": record.get_field(),
                        "value": record.get_value(),
                        "time": record.get_time(),
                    }
                )

        return result
