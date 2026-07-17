from typing import Any
import pytest

from httpx import AsyncClient, Response


@pytest.mark.parametrize(
    argnames="room_id, date_from, date_to, status_code",
    argvalues=[
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 409),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient
):
    # room_id = (await db.rooms.get_all())[0].id

    response_booking: Response = await authenticated_ac.post(
        url="/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    # assert response_booking.status_code == status_code
    if status_code == 200:
        res: Any = response_booking.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"


@pytest.mark.parametrize(
    argnames="room_id, date_from, date_to",
    argvalues=[
        (1, "2024-08-01", "2024-08-10"),
        (2, "2024-09-01", "2024-09-05"),
        (3, "2024-10-10", "2024-10-15"),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, authenticated_ac: AsyncClient
):
    response_booking: Response = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response_booking.status_code == 200

    check_booking: Response = await authenticated_ac.get(url="/bookings/me")
    assert check_booking.status_code == 200
    result: Any = check_booking.json()
    assert isinstance(result, list)
    assert len(result) == 1
    saved_booking = result[0]
    assert saved_booking["room_id"] == room_id
    assert saved_booking["date_from"] == date_from
    assert saved_booking["date_to"] == date_to
