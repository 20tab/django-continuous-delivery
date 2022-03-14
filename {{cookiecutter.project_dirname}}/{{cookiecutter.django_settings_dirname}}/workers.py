"""Custom uvicorn supported worker."""

from uvicorn.workers import UvicornWorker


class UvicornDjangoWorker(UvicornWorker):
    """A Uvicorn worker having lifespan option disabled."""

    CONFIG_KWARGS = {**UvicornWorker.CONFIG_KWARGS, "lifespan": "off"}
