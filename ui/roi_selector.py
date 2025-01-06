import cv2
import numpy as np
from typing import List, Tuple, Callable

class ROISelector:
    def __init__(self, image_size: Tuple[int, int]):
        self.roi_coordinates: List[Tuple[int, int]] = []
        self.image_size = image_size

    def draw_roi(self, event: int, x: int, y: int, flags: int, param: np.ndarray) -> None:
        if event == cv2.EVENT_LBUTTONDOWN and len(self.roi_coordinates) < 4:
            self.roi_coordinates.append((x, y))
            cv2.circle(param, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Select ROI", param)
            
            if len(self.roi_coordinates) == 4:
                cv2.polylines(param, [np.array(self.roi_coordinates, dtype=np.int32)], 
                            True, (0, 255, 0), 2)
                cv2.imshow("Select ROI", param)
                cv2.destroyWindow("Select ROI")

    def select_roi(self, frame: np.ndarray) -> List[Tuple[int, int]]:
        cv2.imshow("Select ROI", frame)
        cv2.setMouseCallback("Select ROI", self.draw_roi, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if len(self.roi_coordinates) != 4:
            raise ValueError("ROI must have exactly 4 points")
        
        return self.roi_coordinates 