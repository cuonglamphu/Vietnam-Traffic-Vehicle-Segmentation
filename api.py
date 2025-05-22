from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
import json
from typing import List, Dict
from main import process_camera
import os
import asyncio
from datetime import datetime, timedelta
import time
from threading import Lock

app = FastAPI()

# Mount the result directory for static file serving
app.mount("/images", StaticFiles(directory="result"), name="images")

# Load ROI data
try:
    with open('camera_coordinates.json', 'r') as f:
        roi_data = json.load(f)
except FileNotFoundError:
    roi_data = []

# Create result directory if it doesn't exist
os.makedirs('result', exist_ok=True)

# Cache for storing results
class CameraCache:
    def __init__(self):
        self.cache = {}
        self.last_update = None
        self.lock = Lock()
    
    def update(self, camera_id: str, data: Dict):
        with self.lock:
            self.cache[camera_id] = data
            self.last_update = datetime.now()
    
    def get_all(self) -> List[Dict]:
        return list(self.cache.values())
    
    def get_one(self, camera_id: str) -> Dict:
        return self.cache.get(camera_id)
    
    def needs_update(self) -> bool:
        if self.last_update is None:
            return True
        return (datetime.now() - self.last_update) > timedelta(seconds=5)

camera_cache = CameraCache()

async def update_cache():
    """Background task to update cache every 30 seconds"""
    while True:
        try:
            if camera_cache.needs_update():
                print("Updating cache...")
                for camera_data in roi_data:
                    camera_id = camera_data['camID']
                    try:
                        output_path, congestion = process_camera(camera_id, roi_data)
                        camera_cache.update(camera_id, {
                            "camera_id": camera_id,
                            "image_url": f"/images/{camera_id}.jpg",
                            "congestion_percentage": round(congestion, 2),
                            "last_updated": datetime.now().isoformat()
                        })
                    except Exception as e:
                        print(f"Error processing camera {camera_id}: {str(e)}")
                        continue
        except Exception as e:
            print(f"Error in update task: {str(e)}")
        
        await asyncio.sleep(30)  # Wait for 30 seconds before next update

@app.on_event("startup")
async def startup_event():
    """Start the background task when the application starts"""
    asyncio.create_task(update_cache())

@app.get("/cameras/", response_model=List[Dict])
async def get_all_cameras():
    """Get cached traffic data for all cameras"""
    # If cache is empty, wait for first update
    if not camera_cache.cache:
        return []
    
    return camera_cache.get_all()

@app.get("/cameras/{camera_id}", response_model=Dict)
async def get_camera(camera_id: str):
    """Get cached traffic data for a specific camera"""
    result = camera_cache.get_one(camera_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found or not yet processed")
    return result

@app.get("/status")
async def get_status():
    """Get the cache status"""
    return {
        "last_update": camera_cache.last_update.isoformat() if camera_cache.last_update else None,
        "cameras_cached": len(camera_cache.cache),
        "next_update_in": 30 - ((datetime.now() - camera_cache.last_update).seconds if camera_cache.last_update else 30)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 