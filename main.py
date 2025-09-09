from fastapi import FastAPI, Body, HTTPException
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@app.get("/hotels")
def print_hotels():
    return hotels


@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int, 
    title: str = Body(description="Название"),
    name: str = Body(description="Имя"),
):  
    if not title.strip():
        raise HTTPException(400, "Title cannot be empty")
    if not name.strip():
        raise HTTPException(400, "Name cannot be empty")
    
    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(400, "Hotel is not found")
    
    hotel["title"] = title.strip()
    hotel["name"] = name.strip()
    
    return {"message": "Hotel updated", "hotel": hotel}


@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    title:  str | None = Body(None, description="Имя"),
    name: str | None = Body(None, description="Имя"),
):
    if title is None and name is None:
        raise HTTPException(400, "Title and name cannot be None")
    
    if title is not None and not title.strip():
        raise HTTPException(400, "Title cannot be empty")
    if name is not None and not title.strip():
        raise HTTPException(400, "Name cannot be empty")
    
    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(400, "Hotel isn`t found")
    
    if title is not None:
        hotel["title"] = title.strip()
    if name is not None:
        hotel["name"] = name.strip()
        
    return {"message": "Hotel partially update", "hotel": hotel}
    
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)