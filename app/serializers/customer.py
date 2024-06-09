from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional
from app.serializers import Pageinfo


class BaseCustomerSerializer(BaseModel):
    name: str


class CustomerSerializer(BaseCustomerSerializer):
    id: int


class CreateCustomer(BaseCustomerSerializer): ...


class UpdateCustomer(BaseCustomerSerializer): ...


class QueryCustomerSerializer(BaseModel):
    name: Optional[str] = Field(
        Query(
            default="",
            description="You can pass multiple values separated by commas, and you can pass a LIKE operator such as % or _",
        )
    )


class ExportCustomerList(Pageinfo):
    total: int
    customers: list[CustomerSerializer]
