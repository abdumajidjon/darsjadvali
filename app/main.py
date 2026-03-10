"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.api.routes import router
from app.database.connection import init_db
from app.bot.dispatcher import get_dispatcher, get_bot

app = FastAPI(title="Schedule Bot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    try:
        # Initialize database
        await init_db()
    except Exception as e:
        print(f"⚠️  Warning: Database initialization failed: {e}")
        print("⚠️  Application will continue, but database features may not work")
        print("📝 Please ensure PostgreSQL is running and DATABASE_URL is correct")
    
    # Set webhook if configured
    if settings.webhook_url:
        try:
            bot = get_bot()
            await bot.set_webhook(
                url=settings.webhook_url,
                secret_token=settings.webhook_secret
            )
            print(f"✅ Webhook set to: {settings.webhook_url}")
        except Exception as e:
            print(f"⚠️  Warning: Failed to set webhook: {e}")
    else:
        print("ℹ️  Webhook not configured. Using polling mode.")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    bot = get_bot()
    await bot.session.close()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
