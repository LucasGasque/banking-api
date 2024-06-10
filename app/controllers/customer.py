from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.serializers.customer import (
    CustomerSerializer,
    UpdateCustomer,
    QueryCustomerSerializer,
)
from app.utils.make_filters import MakeQueryFilters
from app.utils.base_controller import BaseController


class CustomerController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def __get_filters(self, query_params: QueryCustomerSerializer) -> set:
        return MakeQueryFilters.make_filters(
            string_filters={Customer.name: query_params.name}
        )

    async def count_customers(self, query_params: QueryCustomerSerializer) -> int:
        filters = self.__get_filters(query_params)
        result = await self.__session.execute(
            select(func.count(Customer.id)).where(*filters)
        )
        return result.scalar() or 0

    async def list_customers(
        self, query_params: QueryCustomerSerializer, limit: int, offset: int
    ) -> list[CustomerSerializer]:
        filters: set = self.__get_filters(query_params)

        result = await self.__session.execute(
            select(Customer)
            .where(*filters)
            .offset(offset)
            .limit(limit)
            .order_by(Customer.id.desc())
        )

        return [
            CustomerSerializer(**customer.__dict__)
            for customer in result.scalars().all()
        ]

    async def create_customer(self, customer: Customer) -> Customer:
        self.__session.add(customer)
        await self.__session.commit()
        await self.__session.refresh(customer)
        return customer

    async def fetch_customer(self, customer_id: int) -> Customer:
        result = await self.__session.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        customer = result.scalars().first()

        self.verify_if_object_exists(customer, "Customer")

        return customer  # type: ignore

    async def update_customer(
        self, customer: Customer, update_info: UpdateCustomer
    ) -> Customer:
        customer.name = update_info.name
        await self.__session.commit()
        await self.__session.refresh(customer)

        return customer

    async def delete_customer(self, customer: Customer) -> None:
        await self.__session.delete(customer)
        await self.__session.commit()
