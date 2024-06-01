from fastapi import HTTPException
from app.configs.database import Base


class BaseController:
    def get_last_page(self, number_of_objects: int, number_per_page: int) -> int:
        last_page_number = (number_of_objects + number_per_page - 1) // number_per_page
        return last_page_number

    def verify_if_object_exists(self, object: Base | None, object_name: str) -> None:
        if not object:
            raise HTTPException(status_code=404, detail=f"{object_name} not found.")
