"""Filter Extension."""
from enum import Enum
from typing import List, Type, Union

import attr
from fastapi import APIRouter, FastAPI
from starlette.responses import Response

from stac_fastapi.api.models import CollectionUri, EmptyRequest, JSONSchemaResponse
from stac_fastapi.api.routes import create_async_endpoint
# from stac_fastapi.types.core import AsyncBaseFiltersClient, BaseFiltersClient
from stac_fastapi.types.extension import ApiExtension

from .request import AggregationExtensionGetRequest, AggregationExtensionPostRequest


class AggregationConformanceClasses(str, Enum):
    """Conformance classes for the Aggregation extension.

    See
    https://github.com/stac-api-extensions/aggregation
    """

    AGGREGATION = "https://api.stacspec.org/v0.3.0/aggregation"


@attr.s
class AggregationExtension(ApiExtension):
    """Aggregation Extension.

    The purpose of the Aggregation Extension is to provide an endpoint similar to 
    the Search endpoint (/search), but which will provide aggregated information 
    on matching Items rather than the Items themselves. This is highly influenced 
    by the Elasticsearch and OpenSearch aggregation endpoint, but with a more 
    regular structure for responses.

    The Aggregation extension adds several endpoints which allow the retrieval of
    available aggregation fields and aggregation buckets based on a seearch query:
        GET /aggregation
        GET /aggregate
        GET /collections/{collection_id}/aggregations
        GET /collections/{collection_id}/aggregate

    https://github.com/stac-api-extensions/aggregation/blob/main/README.md

    Attributes:
        conformance_classes: Conformance classes provided by the extension
    """

    GET = AggregationExtensionGetRequest
    POST = AggregationExtensionPostRequest

    conformance_classes: List[str] = attr.ib(
        default=[
            AggregationConformanceClasses.AGGREGATION
        ]
    )
    router: APIRouter = attr.ib(factory=APIRouter)
    response_class: Type[Response] = attr.ib(default=JSONSchemaResponse)

    def register(self, app: FastAPI) -> None:
        """Register the extension with a FastAPI application.

        Args:
            app: target FastAPI application.

        Returns:
            None
        """
        self.router.prefix = app.state.router_prefix
        self.router.add_api_route(
            name="Aggregations",
            path="/aggregations",
            methods=["GET"],
            endpoint=create_async_endpoint(
                self.client.get_aggregations, EmptyRequest, self.response_class
            ),
        )
        self.router.add_api_route(
            name="Collection Aggregations",
            path="/collections/{collection_id}/aggregations",
            methods=["GET"],
            endpoint=create_async_endpoint(
                self.client.get_aggregations, CollectionUri, self.response_class
            ),
        )
        self.router.add_api_route(
            name="Aggregate",
            path="/aggregate",
            methods=["GET", "POST"],
            endpoint=create_async_endpoint(
                self.client.aggregate, EmptyRequest, self.response_class
            ),
        )
        self.router.add_api_route(
            name="Collection Aggregate",
            path="/collections/{collection_id}/aggregate",
            methods=["GET", "POST"],
            endpoint=create_async_endpoint(
                self.client.aggregate, CollectionUri, self.response_class
            ),
        )
        app.include_router(self.router, tags=["Aggregation Extension"])