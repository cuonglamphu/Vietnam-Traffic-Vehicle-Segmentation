import cv2

points = []

image_path = '../data/3.jpg'  
image = cv2.imread(image_path)

def select_point(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)} selected: ({x}, {y})")
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1) 
            cv2.imshow("Select 4 Points", image)

if image is None:
    raise ValueError("Could not load image")

cv2.namedWindow("Select 4 Points")
cv2.setMouseCallback("Select 4 Points", select_point)

while True:
    cv2.imshow("Select 4 Points", image)
    key = cv2.waitKey(1) & 0xFF
    if len(points) == 4 or key == ord('q'):  
        break

cv2.destroyAllWindows()

print("Selected points:", points)