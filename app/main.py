from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Note(BaseModel):
    id: int
    title: str
    text: str


@app.post("/notes", response_model=Note)
async def create_note(note: Note):
    return note


@app.get("/notes", response_model=List[Note])
async def get_notes():
    return [
        Note(id=1, title="First", text="Hello"),
        Note(id=2, title="Second", text="FastAPI"),
    ]

#if __name__ == "__main__":
#    main()
