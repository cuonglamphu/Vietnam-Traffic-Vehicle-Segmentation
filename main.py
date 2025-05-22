import cv2
import numpy as np
import requests
from models.yolo_model import YOLOModel
from utils.geometry import GeometryCalculator
from services.congestion_analyzer import CongestionAnalyzer
from visualization.renderer import TrafficVisualizer
import json
from urllib.parse import urlparse
import os
from typing import Dict, Tuple

def load_image_from_url(url):
    # Download image from URL
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")
    
    # Convert to numpy array
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    # Decode the image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise Exception("Failed to decode image")
    return image

def get_camera_id_from_url(url):
    # Extract camera ID from URL
    # Example URL: https://...../662b83ff1afb9c00172dcffb_latest.jpg
    path = urlparse(url).path
    filename = path.split('/')[-1]
    camera_id = filename.split('_')[0]
    return camera_id

def get_roi_coordinates_for_camera(roi_data, camera_id):
    # Find the ROI coordinates for the specific camera
    for item in roi_data:
        if item['camID'] == camera_id:
            # Convert the coordinates to the format expected by the geometry calculator
            return [tuple(coord) for coord in item['cordinate']]
    return None

def process_camera(camera_id: str, roi_data) -> Tuple[str, float]:
    """Process a single camera and return the result path and congestion percentage"""
    base_url = 'https://traffic-camera-api-868447533878.asia-southeast1.run.app/temp_images/'
    image_url = base_url + camera_id + '_latest.jpg'
    
    # Get ROI coordinates for this camera
    roi_coordinates = get_roi_coordinates_for_camera(roi_data, camera_id)
    
    if roi_coordinates is None:
        raise Exception(f"No ROI coordinates found for camera {camera_id}")
    
    # Load the image from URL
    frame = load_image_from_url(image_url)
    
    # Initialize components
    image_size = (800, 800)
    
    # Initialize services
    yolo_model = YOLOModel()
    geometry_calculator = GeometryCalculator()
    congestion_analyzer = CongestionAnalyzer(geometry_calculator)
    
    # Get YOLO predictions
    results = yolo_model.predict(frame)
    segments = results[0].masks.xy if results[0].masks else []
    
    processed_segments = [np.array(segment, dtype=np.int32) for segment in segments]
    
    congestion_percentage = congestion_analyzer.calculate_congestion(
        processed_segments, roi_coordinates, image_size)
    
    result_frame = TrafficVisualizer.draw_results(
        frame, roi_coordinates, processed_segments, congestion_percentage)
    
    # Save result
    output_path = f'result/{camera_id}.jpg'
    cv2.imwrite(output_path, result_frame)
    
    return output_path, congestion_percentage

def main(roi_data):
    # Create result directory if it doesn't exist
    os.makedirs('result', exist_ok=True)
    
    # Process all cameras from roi_data
    for camera_data in roi_data:
        camera_id = camera_data['camID']
        try:
            output_path, congestion = process_camera(camera_id, roi_data)
            print(f"\nProcessing Camera ID: {camera_id}")
            print(f"Results saved to {output_path}")
            print(f"Congestion percentage: {congestion:.2f}%")
        except Exception as e:
            print(f"Error processing camera {camera_id}: {e}")
            continue

if __name__ == "__main__":
    # Load ROI coordinates from JSON file
    try:
        with open('camera_coordinates.json', 'r') as f:
            roi_data = json.load(f)
            if not roi_data:
                print("Warning: No camera coordinates found in camera_coordinates.json")
    except FileNotFoundError:
        print("Error: camera_coordinates.json not found")
        roi_data = []
    
    main(roi_data) 