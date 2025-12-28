from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
import asyncio
from app.workers.processor import transaction_processor
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse

# Створюємо екземпляр застосунку
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Підключаємо роутери (аналог AppModule imports)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Monad Scanner API is running", "docs": "/docs"}

@app.on_event("startup")
async def startup_event():
    # Запускаємо процесор як фонову задачу
    asyncio.create_task(transaction_processor())
    print("✅ Фоновий воркер успішно запущено.")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"❌ Помилка валідації Pydantic: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(exc.body)},
    )