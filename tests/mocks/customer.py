from app.serializers.customer import (
    CustomerSerializer,
    QueryCustomerSerializer,
    BaseCustomerSerializer,
)
from app.models.customer import Customer


customer = CustomerSerializer(id=1, name="Mr Test Customer")
updated_customer = CustomerSerializer(id=1, name="Mr Updated Test Customer")

customer_json = {"id": 1, "name": "Mr Test Customer"}

updated_customer_json = {"id": 1, "name": "Mr Updated Test Customer"}

query_params = QueryCustomerSerializer(name="Mr Test Customer")

customer_model = Customer(**customer.model_dump())

updated_customer_model = Customer(**updated_customer.model_dump())

update_info = BaseCustomerSerializer(name="Mr new name")
