from fastapi import APIRouter, Query, Body

from sqlalchemy import insert, select, func

from models.hotels import HotelsORM
from src.schemas.dependencies import PaginationDep

from src.schemas.hotels import Hotels
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    id: int | None = Query(None, description="Айди отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_ 


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: Hotels):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.get("/paginated")
async def get_page_hotel(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/paginated_hotel")
async def get_paginated_hotel (
    pagination: PaginationDep,
    id: int | None = Query(None, description="ID"),
    title: str | None = Query(None, description="Title"),
):
    global hotels
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels.append(hotel)
    if pagination.page and pagination.per_page:   
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int, 
    title: str = Body(),
    name: str = Body(),
):  
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    title: str | None = Body(),
    name: str | None = Body(),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}    
    
