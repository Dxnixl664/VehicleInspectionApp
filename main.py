from fastapi import FastAPI
from routers.users import router as users_router
from routers.vehicle_inspection_reports import router as reports_router
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(reports_router, prefix="/vehicle_inspection_reports", tags=["reports"])


app.mount("/frontend", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_static_index():
    return FileResponse("frontend/index.html")
