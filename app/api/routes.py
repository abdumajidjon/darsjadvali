"""FastAPI routes"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from datetime import date
import httpx

from app.config import settings
from app.workers.tasks import process_schedule_upload
from app.bot.dispatcher import get_dispatcher, get_bot

router = APIRouter()


def verify_admin_api_key(x_api_key: str = Header(...)) -> bool:
    """Verify admin API key"""
    if x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@router.post("/bot-webhook")
async def bot_webhook(request: dict):
    """
    Telegram webhook endpoint for aiogram.
    """
    from aiogram.types import Update
    
    dispatcher = get_dispatcher()
    bot = get_bot()
    update = Update(**request)
    
    await dispatcher.feed_update(bot=bot, update=update)
    
    return {"ok": True}


@router.post("/admin/upload-schedule")
async def upload_schedule(
    file: UploadFile = File(...),
    target_date: str | None = None,
    _: bool = Depends(verify_admin_api_key)
):
    """
    Admin endpoint to upload schedule file.
    Returns 202 Accepted and processes file in background.
    
    Args:
        file: Excel file (.xlsx)
        target_date: Target date for substitutions (ISO format, optional)
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .xlsx and .xls files are allowed."
        )
    
    # Validate target_date if provided
    if target_date:
        try:
            date.fromisoformat(target_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use ISO format (YYYY-MM-DD)."
            )
    
    # Read file content
    file_content = await file.read()
    
    # Enqueue background task
    try:
        task = await process_schedule_upload.kiq(file_content, target_date)
        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": "Schedule upload queued for processing",
                "task_id": str(task.task_id) if hasattr(task, 'task_id') else None
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to queue task: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "schedule-bot"}
