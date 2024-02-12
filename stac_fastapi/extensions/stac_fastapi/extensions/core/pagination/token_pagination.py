"""Token pagination API extension."""

from typing import Optional

import attr
from fastapi import FastAPI

from stac_fastapi.api.models import GETTokenPagination, POSTTokenPagination
from stac_fastapi.types.extension import ApiExtension


@attr.s
class TokenPaginationExtension(ApiExtension):
    """Token Pagination.

    Though not strictly an extension, the chosen pagination will modify the form of the
    request object. By making pagination an extension class, we can use
    create_request_model to dynamically add the correct pagination parameter to the
    request model for OpenAPI generation.
    """

    GET = GETTokenPagination
    POST = POSTTokenPagination

    conformance_classes: list[str] = attr.ib(factory=list)
    schema_href: Optional[str] = attr.ib(default=None)

    def register(self, app: FastAPI) -> None:
        """Register the extension with a FastAPI application.

        Args:
            app: target FastAPI application.

        Returns:
            None
        """
        pass
