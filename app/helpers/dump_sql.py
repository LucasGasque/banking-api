from sqlalchemy import func
from sqlalchemy.future import select
from app.configs.settings import settings
from app.configs.database import async_session, Base, engine
from app.controllers.customer import CustomerController
from app.models.customer import Customer


class DumpSQL:
    CUSTOMERS = [
        "Arisha Barron",
        "Branden Gibson",
        "Rhonda Church",
        "Georgina Hazel",
    ]

    @staticmethod
    async def dump_info() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        if settings.ENVIROMENT == "development":
            async with async_session() as session:
                controller = CustomerController(session)

                result = await session.execute(select(func.count(Customer.id)))

                number_of_customers = result.scalar() or 0

                if number_of_customers == 0:
                    for customer in DumpSQL.CUSTOMERS:
                        await controller.create_customer(
                            Customer(
                                name=customer,
                            )
                        )
