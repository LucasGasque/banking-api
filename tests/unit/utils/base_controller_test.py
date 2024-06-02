import pytest
from fastapi.exceptions import HTTPException
from app.utils.base_controller import BaseController


def test_get_last_page_is_1():
    last_page = BaseController().get_last_page(10, 10)

    assert last_page == 1


def test_get_last_page_is_2():
    last_page = BaseController().get_last_page(11, 10)

    assert last_page == 2


def test_verify_if_object_doenst_exists():
    with pytest.raises(HTTPException):
        BaseController().verify_if_object_exists(None, "Test Object")


def test_verify_if_object_exists():
    BaseController().verify_if_object_exists(1, "Test Object")
