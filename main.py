
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import groq_client
from database import supabase
from models import PlantRequest, PlantCreate
from datetime import datetime, timezone

app = FastAPI(title="Marina's Garden Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/api/plants/{user_id}")
def get_user_plants(user_id: str):
    try:
        response = supabase.table("plants").select("*").eq("user_id", user_id).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plants")
def create_plant(plant: PlantCreate):
    prompt = f"""
        You are an expert botanist. Provide care instructions for a {plant.plant_type}.
        Return ONLY a valid JSON object with the following keys:
        - water_frequency_days (integer)
        - sunlight_needs (string)
        - fun_fact (string)
        Do not include any markdown, code blocks, or extra text.
    """
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            )
        respone_text = chat_completion.choices[0].message.content
        care_data = json.loads(respone_text)
    except Exception as e:
        care_data = {
            "water_frequency_days": 7,
            "sunlight_needs": "Unknown",
            "fun_fact": "AI is taking a nap."
        }
    
    new_plant_data = {
        "name": plant.name,
        "plot_index": plant.plot_index,
        "plant_type": plant.plant_type,
        "user_id": plant.user_id,
        "stage": plant.stage,
        "room": plant.room,
        "plant_start": plant.plant_start,
        "last_watered": plant.last_watered,
        "ai_care_tips": care_data
    }

    try:
        response = supabase.table("plants").insert(new_plant_data).execute()
        return {"success": True, "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/plants/{plant_id}")
def delete_plant(plant_id: str):
    try:
        response = supabase.table("plants").delete().eq("id", plant_id).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/plants/{plant_id}/water")
def water_plant(plant_id: str):
    try:
        now = datetime.now(timezone.utc).isoformat()
        response = supabase.table("plants").update({"last_watered": now}).eq("id", plant_id).execute()
        return {"success": True, "data": response.data[0] if response.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
