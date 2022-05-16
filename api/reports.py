from fastapi import (APIRouter, Depends, UploadFile,
                     File, BackgroundTasks)
from fastapi.responses import StreamingResponse
from services.reports import ReportService


router = APIRouter(
    prefix='/reports',
    tags=['reports']
)


@router.post('/import')
def import_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    report_service: ReportService = Depends(),

):
    background_tasks.add_task(report_service.import_csv,  file.file)


@router.get('/export')
def export_csv(
    report_service: ReportService = Depends()

):
    report = report_service.export_csv()
    return StreamingResponse(
        report,
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=report.csv'})
