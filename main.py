import cv2
from models.yolo_model import YOLOModel
from utils.geometry import GeometryCalculator
from services.congestion_analyzer import CongestionAnalyzer
from visualization.renderer import TrafficVisualizer
import numpy as np



def main(roi_coordinates):
    # Initialize components
    frame = cv2.imread('data/3.jpg')
    if frame is None:
        raise ValueError("Could not load image")

    image_size = (800, 800)
    
    # Initialize services
    yolo_model = YOLOModel()
    geometry_calculator = GeometryCalculator()
    congestion_analyzer = CongestionAnalyzer(geometry_calculator)
    
    try:
        h, w = frame.shape[:2]
        margin = 100 

        print("ROI coordinates:", roi_coordinates)
        
        # Get YOLO predictions
        results = yolo_model.predict(frame)
        segments = results[0].masks.xy if results[0].masks else []
        

        processed_segments = [np.array(segment, dtype=np.int32) for segment in segments]
        

        congestion_percentage = congestion_analyzer.calculate_congestion(
            processed_segments, roi_coordinates, image_size)
        

        result_frame = TrafficVisualizer.draw_results(
            frame, roi_coordinates, processed_segments, congestion_percentage)
        

        output_path = 'result/result.jpg'
        cv2.imwrite(output_path, result_frame)
        print(f"Results saved to {output_path}")
        print(f"Congestion percentage: {congestion_percentage:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    roi_coordinates = [(25, 280), (295, 76), (422, 83), (452, 283)]
    main(roi_coordinates) 