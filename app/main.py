from fastapi import FastAPI
from mangum import Mangum

from app import __version__
from app.core.auth.url import auth
from app.core.settings import set_up


config = set_up()
app = FastAPI(
    title="TorNetwork API",
    description="TorNetwork Project API",
    version=__version__)


@app.get("/status", include_in_schema=False)
def get_status():
    """Get status of messaging server."""
    return ({"status": "it's alive"})


@app.get("/error", include_in_schema=False)
def get_error():
    """Get error of messaging server."""
    raise


app.include_router(auth, prefix="/auth")
handler = Mangum(app)
