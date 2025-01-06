from typing import List, Tuple
from utils.geometry import GeometryCalculator
import numpy as np
class CongestionAnalyzer:
    def __init__(self, geometry_calculator: GeometryCalculator):
        self.geometry_calculator = geometry_calculator

    def calculate_congestion(self, segments: List[np.ndarray], 
                           roi: List[Tuple[int, int]], 
                           image_size: Tuple[int, int]) -> float:
        roi_area = self.geometry_calculator.calculate_polygon_area(roi)
        total_area = 0

        for segment in segments:
            intersection_area = self.geometry_calculator.calculate_intersection_area(
                segment, roi, image_size)
            total_area += intersection_area

        congestion_percentage = (total_area / roi_area) * 100 if roi_area > 0 else 0
        return min(congestion_percentage, 100) 