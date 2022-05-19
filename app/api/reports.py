from fastapi import (APIRouter, Depends, UploadFile,
                     File, BackgroundTasks)
from services.reports import ReportService


router = APIRouter(
    prefix='/reports',
    tags=['reports']
)


@router.post('/import')
async def import_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    report_service: ReportService = Depends(),

) -> None:
    background_tasks.add_task(report_service.import_csv,  file.file)
