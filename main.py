import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller import router
from app.core.database import engine, Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lemong Backend API", version="1.0.0",docs_url="/docs", redoc_url="/redoc")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Lemong Backend API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 