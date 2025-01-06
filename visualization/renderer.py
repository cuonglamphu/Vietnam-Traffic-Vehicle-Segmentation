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
        
        # Draw ROI
        cv2.polylines(overlay, [np.array(roi_coordinates, dtype=np.int32)], 
                     True, (0, 255, 0), 2)
        
        # Draw segments
        for segment in processed_segments:
            cv2.polylines(overlay, [segment], True, (255, 0, 0), 2)
            cv2.fillPoly(overlay, [segment], (255, 0, 0, 50))

        # Blend overlay
        alpha = 0.5
        result = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Add text
        cv2.putText(result, f"Congestion: {congestion_percentage:.2f}%", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return result 