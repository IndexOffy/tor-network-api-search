from fastapi import FastAPI, Depends
from mangum import Mangum

from app import __version__
from app.core.auth.security import authorization
from app.core.auth.url import auth
from app.api.v1.routers import router
from app.core.settings import set_up


config = set_up()
app = FastAPI(
    title="TorNetwork API",
    description="TorNetwork Project API",
    version=__version__)


@app.get("/status", include_in_schema=False)
def get_status(user=Depends(authorization)):
    """Get status of messaging server."""
    return ({"status": "it's alive"})


app.include_router(auth, prefix="/auth")
app.include_router(router, prefix="/v1")
handler = Mangum(app)
