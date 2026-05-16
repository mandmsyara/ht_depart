import uuid

import pytest


@pytest.mark.asyncio
async def test_create_department(client):
    response = await client.post(
        "/departments/",
        json={
            "name": f"Test Department {uuid.uuid4()}",
            "parent_id": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_department_returns_409(client):
    payload = {
        "name": f"Duplicate Department {uuid.uuid4()}",
        "parent_id": None,
    }

    first_response = await client.post(
        "/departments/",
        json=payload,
    )

    second_response = await client.post(
        "/departments/",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_create_employee_for_nonexistent_department_returns_404(client):
    response = await client.post(
        "/departments/999999/employees/",
        json={
            "full_name": "Ivan Ivanov",
            "position": "Backend Developer",
            "hired_at": "2026-05-15",
        },
    )

    assert response.status_code == 404
