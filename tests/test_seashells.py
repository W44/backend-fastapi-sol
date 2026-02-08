from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """
    Checks if the health endpoint is working.
    This is used by monitoring systems to verify the API is up.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_seashell_success(client: TestClient):
    """
    Checks if we can add a new seashell to the collection.
    Should return the created seashell with an ID and a 201 status.
    """
    response = client.post(
        "/seashells/",
        json={
            "name": "Conch Shell",
            "species": "Strombus gigas",
            "description": "Beautiful pink conch shell"
        }
    )
    data = response.json()
    
    assert response.status_code == 201
    assert data["name"] == "Conch Shell"
    assert data["species"] == "Strombus gigas"
    assert "id" in data


def test_create_seashell_missing_name(client: TestClient):
    """
    Tries to create a seashell without a name.
    This should fail since name is required.
    """
    response = client.post(
        "/seashells/",
        json={
            "species": "Unknown species",
            "description": "A mysterious shell"
        }
    )
    assert response.status_code == 422


def test_list_seashells_with_data(client: TestClient):
    """
    Creates a couple of seashells and then lists them.
    Should see both shells in the results.
    """
    client.post(
        "/seashells/",
        json={"name": "Shell A", "species": "Species A"}
    )
    client.post(
        "/seashells/",
        json={"name": "Shell B", "species": "Species B"}
    )
    
    response = client.get("/seashells/")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Shell A"


def test_list_seashells_pagination(client: TestClient):
    """
    Creates multiple seashells and tests pagination.
    Checks if we can get specific pages with custom page sizes.
    """
    for i in range(5):
        client.post(
            "/seashells/",
            json={"name": f"Shell {i}", "species": f"Species {i}"}
        )
    
    response = client.get("/seashells/?page=1&page_size=2")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Shell 0"


def test_list_seashells_sort_by_name(client: TestClient):
    """
    Creates seashells with different names and sorts them alphabetically.
    Should come back in A-Z order.
    """
    client.post("/seashells/", json={"name": "Zebra Shell", "species": "Z species"})
    client.post("/seashells/", json={"name": "Apple Shell", "species": "A species"})
    client.post("/seashells/", json={"name": "Mango Shell", "species": "M species"})
    
    response = client.get("/seashells/?sort_by=name&order=asc")
    data = response.json()
    
    assert response.status_code == 200
    assert data[0]["name"] == "Apple Shell"
    assert data[2]["name"] == "Zebra Shell"


def test_list_seashells_search(client: TestClient):
    """
    Creates several seashells and searches for one by name.
    Only matching shells should appear in results.
    """
    client.post("/seashells/", json={"name": "Cowrie Shell", "species": "Cypraea"})
    client.post("/seashells/", json={"name": "Conch Shell", "species": "Strombus"})
    client.post("/seashells/", json={"name": "Clam Shell", "species": "Mercenaria"})
    
    response = client.get("/seashells/?search=Conch")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Conch Shell"


def test_get_seashell_by_id(client: TestClient):
    """
    Creates a seashell and then fetches it by its ID.
    Should get back the exact same seashell.
    """
    create_response = client.post(
        "/seashells/",
        json={"name": "Test Shell", "species": "Test Species"}
    )
    seashell_id = create_response.json()["id"]
    
    response = client.get(f"/seashells/{seashell_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data["id"] == seashell_id
    assert data["name"] == "Test Shell"


def test_get_nonexistent_seashell(client: TestClient):
    """
    Tries to fetch a seashell with an ID that doesn't exist.
    Should return a 404 error.
    """
    response = client.get("/seashells/99999")
    assert response.status_code == 404


def test_update_seashell(client: TestClient):
    """
    Updates just the name of a seashell.
    Other fields should stay unchanged.
    """
    create_response = client.post(
        "/seashells/",
        json={"name": "Old Name", "species": "Old Species", "description": "Old Description"}
    )
    seashell_id = create_response.json()["id"]
    
    response = client.put(
        f"/seashells/{seashell_id}",
        json={"name": "New Name"}
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == "New Name"
    assert data["species"] == "Old Species"


def test_delete_seashell(client: TestClient):
    """
    Creates a seashell and then deletes it.
    After deletion, trying to fetch it should return 404.
    """
    create_response = client.post(
        "/seashells/",
        json={"name": "To Delete", "species": "Deletable"}
    )
    seashell_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/seashells/{seashell_id}")
    assert delete_response.status_code == 204
    
    get_response = client.get(f"/seashells/{seashell_id}")
    assert get_response.status_code == 404
