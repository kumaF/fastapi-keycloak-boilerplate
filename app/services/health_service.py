from ..utils import build_response
from ..db import get_client, MongoDB

class HealthService:
    def __init__(self):
        super().__init__()

    async def health_check(self):
        db = MongoDB(get_client())

        msg: dict = {
            'application': 'success',
            'database': 'success' if db.db_health_check() else 'failed'
        }

        return await build_response(msg=msg)