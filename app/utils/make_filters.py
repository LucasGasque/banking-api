from fastapi.params import Query
from sqlalchemy import or_


class MakeQueryFilters:
    @staticmethod
    def __make_integer_filters(filters: dict):
        int_filters = set()
        for key, value in filters.items():
            if value:
                split_values = value.split(",")

                if len(split_values) > 1:
                    int_filters.add(key.in_([int(value) for value in split_values]))

                if len(split_values) == 1:
                    int_filters.add(key == int(value))

        return int_filters

    @staticmethod
    def __make_string_filters(filters: dict):
        str_filters = set()
        for key, value in filters.items():
            if value:
                split_values = value.split(",")

                if len(split_values) > 1:
                    or_filters = set()
                    for string in split_values:
                        or_filters.add(key.ilike(f"{string}"))

                    str_filters.add(or_(*or_filters))

                if len(split_values) == 1:
                    str_filters.add(key.ilike(f"{split_values[0]}"))

        return str_filters

    @staticmethod
    def __clean_null_values(filters: dict = {}):
        return {
            key: value
            for key, value in filters.items()
            if value and not isinstance(value, Query)
        }

    @staticmethod
    def make_filters(
        integer_filters: dict = {},
        string_filters: dict = {},
        min_timestamp_filters: dict = {},
        max_timestamp_filters: dict = {},
    ):
        integer_filters = MakeQueryFilters.__clean_null_values(integer_filters)
        string_filters = MakeQueryFilters.__clean_null_values(string_filters)
        min_timestamp_filters = MakeQueryFilters.__clean_null_values(
            min_timestamp_filters
        )
        max_timestamp_filters = MakeQueryFilters.__clean_null_values(
            max_timestamp_filters
        )

        min_timestamp_filters = {
            key >= value for key, value in min_timestamp_filters.items()
        }

        max_timestamp_filters = {
            key <= value for key, value in max_timestamp_filters.items()
        }

        return {
            *MakeQueryFilters.__make_integer_filters(integer_filters),
            *MakeQueryFilters.__make_string_filters(string_filters),
            *min_timestamp_filters,
            *max_timestamp_filters,
        }
