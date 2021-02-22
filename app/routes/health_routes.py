from fastapi import APIRouter

from ..services import HealthService

router = APIRouter()


@router.get('')
async def health_check():
    service = HealthService()
    return await service.health_check()
