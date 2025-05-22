import cv2
import numpy as np
from typing import List, Tuple

class TrafficVisualizer:
    @staticmethod
    def draw_results(frame: np.ndarray, 
                    roi_coordinates: List[Tuple[int, int]],
                    processed_segments: List[np.ndarray],
                    congestion_percentage: float) -> np.ndarray:
        overlay = frame.copy()
        primary_color = (118, 205, 48)
        secondary_color = (190, 235, 189)
        text_color = (189, 255, 247)

        # Draw ROI
        cv2.polylines(overlay, [np.array(roi_coordinates, dtype=np.int32)], 
                     True, secondary_color, 2)
        
        # Draw segments
        for segment in processed_segments:
            cv2.polylines(overlay, [segment], True, primary_color, 2)
            cv2.fillPoly(overlay, [segment], primary_color,50)

        # Blend overlay
        alpha = 0.5
        result = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Add text
        cv2.putText(result, f"{congestion_percentage:.2f}%", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)
        
        return result 