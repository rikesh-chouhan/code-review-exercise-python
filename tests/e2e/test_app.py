from http import HTTPStatus

from fastapi.testclient import TestClient

from app import app
from npm_deps.models import VersionedPackage

def test_healthcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_package():
    client = TestClient(app)
    response = client.get("/package/minimatch/3.1.2")
    assert response.status_code == HTTPStatus.OK
    assert response.json().get("name") == "minimatch"
    assert response.json().get("version") == "3.1.2"
    deps = response.json().get("dependencies")
    list_of_deps = list(map(convert_json_versioned_package, deps))
    assert len(list_of_deps) > 0
    brace_expansion_iterator = (dep for dep in list_of_deps if dep.name == "brace-expansion")
    brace_dep = next(brace_expansion_iterator)
    assert brace_dep.version == "1.1.7"
    assert len(brace_dep.dependencies) >= 2
    name_version = {dep.name: dep.version for dep in brace_dep.dependencies}
    assert name_version.get("balanced-match") == "0.4.1"
    assert name_version.get("concat-map") == "0.0.1"
    
    

def convert_json_versioned_package(pkg_json) -> VersionedPackage:
    return VersionedPackage(
        name=pkg_json["name"],
        version=pkg_json["version"],
        dependencies=[
            convert_json_versioned_package(dep) for dep in pkg_json.get("dependencies", [])
        ] if pkg_json.get("dependencies") else None
    )

def test_get_package_by_name():
    client = TestClient(app)
    response = client.get("/package/react")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() is not None


def test_unsupported_route():
    client = TestClient(app)
    response = client.get("/something")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() is not None
