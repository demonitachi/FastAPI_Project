from fastapi import FastAPI
from .routers.products import routers as products_router
from .routers.sellers import routers as sellers_router
from .routers.login import routers as login_router

app = FastAPI(
    title="Products API",
    description="An API for managing products and sellers",
    version="1.0.0",
    redoc_url=None,
    license_info={
        "name": "MIT",
        "url": "https://fastapi.tiangolo.com/license/",
    },
    terms_of_service="https://fastapi.tiangolo.com/terms/",
    contact={
        "name": "Kunal Anand",
        "url": "https://github.com/demonitachi",
        "email": "anandkunal926@gmail.com",
    }
)

app.include_router(products_router)
app.include_router(sellers_router)
app.include_router(login_router)