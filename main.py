from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import chat_router, rag_router

app = FastAPI()

# 🔹 Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://127.0.0.1:5500"] si usas Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Incluir los routers
app.include_router(chat_router.router)
app.include_router(rag_router.router)

# 🔹 Servir carpeta "static" (donde pondrás index.html)
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/")
async def index():
    return {"message": "Hello, World!"}