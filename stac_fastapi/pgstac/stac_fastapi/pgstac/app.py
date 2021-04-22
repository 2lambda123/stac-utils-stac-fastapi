"""FastAPI application using PGStac."""
from stac_fastapi.api.app import StacApi
from stac_fastapi.pgstac.config import Settings
from stac_fastapi.pgstac.db import connect_to_db, close_db_connection
from stac_fastapi.pgstac.core import CoreCrudClient
from stac_fastapi.pgstac.transactions import TransactionsClient
from mangum import Mangum

from stac_fastapi.extensions.core import (
    FieldsExtension,
    QueryExtension,
    SortExtension,
    TransactionExtension,
)

settings = Settings()

api = StacApi(
    settings=settings,
    extensions=[
        TransactionExtension(client=TransactionsClient),
        QueryExtension(),
        SortExtension(),
        FieldsExtension(),
    ],
    client=CoreCrudClient(),
)
app = api.app


@app.on_event("startup")
async def startup_event():
    """ Connect to database on startup """
    await connect_to_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    await close_db_connection(app)


def run():
    import uvicorn

    uvicorn.run(
        "stac_fastapi.pgstac.app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )


if __name__ == "__main__":
    run()

handler = Mangum(app)