from fastapi import APIRouter, HTTPException, Response
from app.schemas.item_schema import ItemSchema
from app.services.item_service import create_item, get_all_items, get_item, update_item, delete_item
from app.services.model_service import generate_text  # Importar la función que genera texto
from app.schemas.model_schema import GenerateRequest  # Importar el esquema
from app.schemas.prompt import TextInput 
from gtts import gTTS
from app.services.virtual_assistant import generate_response
import os

router = APIRouter()

@router.post("/items/", response_model=dict)
async def create_new_item(item: ItemSchema):
    item = await create_item(item.dict())
    return item

@router.get("/items/", response_model=list)
async def read_items():
    items = await get_all_items()
    return items

@router.get("/items/{item_id}", response_model=dict)
async def read_item(item_id: str):
    item = await get_item(item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}", response_model=dict)
async def update_existing_item(item_id: str, item: ItemSchema):
    updated_item = await update_item(item_id, item.model_dump())
    if updated_item:
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}", response_model=dict)
async def delete_existing_item(item_id: str):
    deleted_item = await delete_item(item_id)
    if deleted_item:
        return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/generate/")
async def generate_text_endpoint(request: GenerateRequest):
    generated_text = await generate_text(request.prompt)  # Usar el prompt del esquema
    raise {"generated_text": generated_text}



@router.post("/generate-audio/")
async def generate_audio(request: TextInput):
    # Generar el audio usando gTTS
    tts = gTTS(request.text)
    audio_file = "output.mp3"
    tts.save(audio_file)

    # Devolver el archivo de audio
    with open(audio_file, "rb") as f:
        audio_data = f.read()
    
    # Eliminar el archivo de audio temporal
    os.remove(audio_file)
    
    raise Response(content=audio_data, media_type="audio/mpeg")


@router.post("/virtual_assistant/")
async def generate_text_virtual_assistant(request: GenerateRequest):
    generated_response = await generate_response(request.prompt)  # Usar el prompt del esquema
    return {"generated_response": generated_response}