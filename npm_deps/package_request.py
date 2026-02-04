import logging
from http import HTTPStatus

import requests
from npm_deps.error import PackageNotFoundError, PackageFetchError
import functools

NPM_REGISTRY_URL = "https://registry.npmjs.org"

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=128)
async def request_package(name: str) -> dict:
    logger.debug("Calling for package: %s", name)
    response_error = None
    try:
        response = requests.get(f"{NPM_REGISTRY_URL}/{name}")
        logger.info("Status: %s", response.status_code)
        if response.status_code != HTTPStatus.OK:
            response_error = response.text
            logger.error("Package: %s get error %s", name, response_error)
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise PackageNotFoundError(
                    detail=f"{name}",
                )
            else:
                raise PackageFetchError(
                    detail=f"{name}: {response_error}",
                    status_code=response.status_code,
                )
        # TODO: define a domain type to return
        return response.json()  # type: ignore[no-any-return]
    except Exception as e:
        if response_error:
            raise e from e
        else:
            logger.exception("Error requesting package: %s", name)
            raise PackageFetchError(
                detail=f"{name}: {str(e)}",
            ) from e
