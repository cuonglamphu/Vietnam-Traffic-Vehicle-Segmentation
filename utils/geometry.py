import numpy as np
import cv2
from typing import List, Tuple

class GeometryCalculator:
    @staticmethod
    def calculate_polygon_area(points: List[Tuple[int, int]]) -> float:
        points = np.array(points)
        return 0.5 * np.abs(np.dot(points[:, 0], np.roll(points[:, 1], 1)) - 
                           np.dot(points[:, 1], np.roll(points[:, 0], 1)))

    @staticmethod
    def calculate_intersection_area(segment: np.ndarray, roi: List[Tuple[int, int]], 
                                  image_size: Tuple[int, int]) -> float:
        roi_polygon = np.array(roi, dtype=np.float32).reshape((-1, 2))
        segment_polygon = np.array(segment, dtype=np.float32).reshape((-1, 2))
        
        mask = np.zeros(image_size, dtype=np.uint8)
        cv2.fillPoly(mask, [roi_polygon.astype(np.int32)], 1)
        
        segment_mask = np.zeros(image_size, dtype=np.uint8)
        cv2.fillPoly(segment_mask, [segment_polygon.astype(np.int32)], 1)
        
        intersection = cv2.bitwise_and(mask, segment_mask)
        return cv2.countNonZero(intersection) 