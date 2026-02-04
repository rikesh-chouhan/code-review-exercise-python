from http import HTTPStatus

from fastapi import HTTPException


class PackageVersionNotFoundError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, detail)


class PackageNotFoundError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, f"Package: {detail} not found. Please check the name.")


class PackageFetchError(HTTPException):
    def __init__(self, detail: str, status_code=None) -> None:
        super().__init__(
            status_code if status_code is not None else HTTPStatus.INTERNAL_SERVER_ERROR,
            f"Package fetch error: {detail}",
        )
