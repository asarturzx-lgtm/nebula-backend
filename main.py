from fastapi import FastAPI
from app.api.routers.v1.wallets import router as wallets_router
from app.api.routers.v1.operations import router as operations_router
from app.api.routers.v1.users import router as users_router
from app.database import Base
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000",
    "https://asarturzx-lgtm.github.io",  # Добавь эту строку
]

app = FastAPI()

# Добавь этот блок:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любых адресов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешает все заголовки (включая Authorization)
)





app.include_router(wallets_router, prefix="/api/v1", tags=["wallet"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])

Base.metadata.create_all(bind=engine)


