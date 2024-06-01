from sqlalchemy import func
from sqlalchemy.future import select
from app.configs.settings import settings
from app.configs.database import async_session
from app.controllers.customer import CustomerController
from app.models.customer import Customer


class DumpSQL:
    CUSTOMERS = [
        {"id": 1, "name": "Arisha Barron"},
        {"id": 2, "name": "Branden Gibson"},
        {"id": 3, "name": "Rhonda Church"},
        {"id": 4, "name": "Georgina Hazel"},
    ]

    @staticmethod
    async def dump_info() -> None:
        if settings.ENVIROMENT == "development":
            async with async_session() as session:
                controller = CustomerController(session)

                result = await session.execute(select(func.count(Customer.id)))

                number_of_customers = result.scalar() or 0

                if number_of_customers == 0:
                    for customer in DumpSQL.CUSTOMERS:
                        await controller.create_customer(
                            Customer(
                                id=customer.get("id"),
                                name=customer.get("name"),
                            )
                        )
