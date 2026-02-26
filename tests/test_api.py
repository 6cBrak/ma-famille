from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_full_mvp_flow():
    r1 = client.post(
        "/users/register",
        json={
            "email": "admin@example.com",
            "password": "secret12",
            "first_name": "Admin",
            "last_name": "Famille",
        },
    )
    assert r1.status_code == 200
    admin_id = r1.json()["id"]

    r2 = client.post("/families", json={"name": "Famille Diallo", "owner_user_id": admin_id})
    assert r2.status_code == 200
    family = r2.json()

    r3 = client.post(
        "/users/register",
        json={
            "email": "membre@example.com",
            "password": "secret12",
            "first_name": "Membre",
            "last_name": "Diallo",
        },
    )
    assert r3.status_code == 200
    member_id = r3.json()["id"]

    r4 = client.post("/families/join", json={"user_id": member_id, "invite_code": family["invite_code"]})
    assert r4.status_code == 200

    father = client.post(
        "/persons",
        json={
            "family_id": family["id"],
            "created_by_user_id": admin_id,
            "first_name": "Papa",
            "last_name": "Diallo",
        },
    )
    mother = client.post(
        "/persons",
        json={
            "family_id": family["id"],
            "created_by_user_id": admin_id,
            "first_name": "Maman",
            "last_name": "Diallo",
        },
    )
    child = client.post(
        "/persons",
        json={
            "family_id": family["id"],
            "created_by_user_id": member_id,
            "first_name": "Enfant",
            "last_name": "Diallo",
        },
    )
    assert father.status_code == 200
    assert mother.status_code == 200
    assert child.status_code == 200

    rf = client.post(
        "/relationships",
        json={
            "family_id": family["id"],
            "person_a_id": father.json()["id"],
            "person_b_id": child.json()["id"],
            "relation_type": "PARENT_OF",
        },
    )
    rm = client.post(
        "/relationships",
        json={
            "family_id": family["id"],
            "person_a_id": mother.json()["id"],
            "person_b_id": child.json()["id"],
            "relation_type": "PARENT_OF",
        },
    )
    assert rf.status_code == 200
    assert rm.status_code == 200

    tree = client.get(f"/tree/{family['id']}")
    assert tree.status_code == 200
    assert len(tree.json()["persons"]) == 3
    assert len(tree.json()["relationships"]) == 2
