import cv2
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import glob
import requests
import numpy as np
from urllib.parse import urlparse

class CoordinateSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Coordinate Selector")
        self.root.geometry("800x600")
        
        # Variables
        self.camera_id = tk.StringVar()
        self.image_urls = []
        self.current_image_index = 0
        self.points = []
        self.results = []
        self.original_image = None  # Store original image
        self.display_image = None   # Store resized image for display
        self.current_photo = None
        self.scale_factor = 1.0
        self.image_label_width = 0
        self.image_label_height = 0
        self.image_x_offset = 0  # X offset of image in label
        self.image_y_offset = 0  # Y offset of image in label
        self.display_width = 0   # Width of displayed image
        self.display_height = 0  # Height of displayed image
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Camera ID Frame
        camera_frame = ttk.LabelFrame(self.root, text="Camera Information", padding=10)
        camera_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(camera_frame, text="Camera ID:").pack(side="left", padx=5)
        ttk.Entry(camera_frame, textvariable=self.camera_id).pack(side="left", padx=5)
        
        # URL Entry Frame
        url_frame = ttk.LabelFrame(self.root, text="Image URLs", padding=10)
        url_frame.pack(fill="x", padx=10, pady=5)
        
        self.url_text = tk.Text(url_frame, height=3)
        self.url_text.pack(fill="x", padx=5, pady=5)
        ttk.Label(url_frame, text="Enter image URLs (one per line)").pack(side="left", padx=5)
        
        # Buttons Frame
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Load Images", command=self.load_images_from_urls).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save Results", command=self.save_results).pack(side="left", padx=5)
        
        # Image Frame
        self.image_frame = ttk.LabelFrame(self.root, text="Image View", padding=10)
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)
        
        # Status Frame
        status_frame = ttk.Frame(self.root, padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Please enter camera ID and image URLs")
        self.status_label.pack(side="left")
        
    def load_images_from_urls(self):
        if not self.camera_id.get():
            messagebox.showerror("Error", "Please enter camera ID first!")
            return
            
        # Get URLs from text widget
        urls = self.url_text.get("1.0", tk.END).strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            messagebox.showerror("Error", "Please enter at least one image URL!")
            return
            
        self.image_urls = urls
        self.current_image_index = 0
        self.points = []
        self.results = []
        self.load_current_image()
        
    def load_current_image(self):
        if 0 <= self.current_image_index < len(self.image_urls):
            image_url = self.image_urls[self.current_image_index]
            
            try:
                # Download image from URL
                response = requests.get(image_url)
                if response.status_code != 200:
                    raise Exception(f"Failed to download image: {response.status_code}")
                
                # Convert to numpy array
                image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                self.original_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                
                if self.original_image is None:
                    raise Exception("Failed to decode image")
                    
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                
                # Force update of GUI to get correct dimensions
                self.root.update_idletasks()
                
                # Calculate initial display size
                self.calculate_display_size()
                
                # Create display image
                self.display_image = cv2.resize(self.original_image, (self.display_width, self.display_height))
                
                # Update display
                self.update_display()
                
                # Update status
                self.status_label.configure(
                    text=f"Image {self.current_image_index + 1}/{len(self.image_urls)}: {urlparse(image_url).path}"
                )
                
                # Bind mouse click event
                self.image_label.bind('<Button-1>', self.on_image_click)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
                return

    def calculate_display_size(self):
        # Get current label size
        self.image_label_width = self.image_label.winfo_width()
        self.image_label_height = self.image_label.winfo_height()
        
        # Get original image size
        original_height, original_width = self.original_image.shape[:2]
        
        # Calculate scale factors to fit the image in the label
        width_scale = self.image_label_width / original_width
        height_scale = self.image_label_height / original_height
        self.scale_factor = min(width_scale, height_scale)
        
        # Calculate display dimensions
        self.display_width = int(original_width * self.scale_factor)
        self.display_height = int(original_height * self.scale_factor)
        
        # Calculate centering offsets
        self.image_x_offset = (self.image_label_width - self.display_width) // 2
        self.image_y_offset = (self.image_label_height - self.display_height) // 2
    
    def update_display(self):
        if self.display_image is not None:
            # Create a copy of the display image
            display_image = self.display_image.copy()
            
            # Create a black background of label size
            background = np.zeros((self.image_label_height, self.image_label_width, 3), dtype=np.uint8)
            
            # Calculate where to place the image
            y1 = self.image_y_offset
            y2 = y1 + self.display_height
            x1 = self.image_x_offset
            x2 = x1 + self.display_width
            
            # Place the image on the background
            background[y1:y2, x1:x2] = display_image
            
            # Draw all points
            for i, (orig_x, orig_y) in enumerate(self.points):
                # Convert original coordinates to display coordinates
                x = int(orig_x * self.scale_factor) + self.image_x_offset
                y = int(orig_y * self.scale_factor) + self.image_y_offset
                
                # Draw point
                cv2.circle(background, (x, y), 5, (0, 255, 0), -1)
                # Draw point number
                cv2.putText(background, str(i+1), (x+10, y+10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Convert to PhotoImage
            image = Image.fromarray(background)
            self.current_photo = ImageTk.PhotoImage(image)
            
            # Update image label
            self.image_label.configure(image=self.current_photo)
            self.image_label.image = self.current_photo
            
    def on_image_click(self, event):
        if len(self.points) < 4:
            # Get click coordinates relative to the image origin
            x = event.x - self.image_x_offset
            y = event.y - self.image_y_offset
            
            # Check if click is within image bounds
            if (0 <= x < self.display_width and 
                0 <= y < self.display_height):
                
                # Convert to original image coordinates
                original_x = int(x / self.scale_factor)
                original_y = int(y / self.scale_factor)
                
                # Store original coordinates
                self.points.append((original_x, original_y))
                
                # Print debug information
                print(f"Click at ({event.x}, {event.y})")
                print(f"Offset: ({self.image_x_offset}, {self.image_y_offset})")
                print(f"Adjusted: ({x}, {y})")
                print(f"Original: ({original_x}, {original_y})")
                print(f"Scale factor: {self.scale_factor}")
                
                # Update display with all points
                self.update_display()
                
                # Update status
                self.status_label.configure(
                    text=f"Point {len(self.points)}/4 selected at ({original_x}, {original_y})"
                )
                
                # If 4 points selected, save and move to next image
                if len(self.points) == 4:
                    self.save_current_image_data()
                    self.current_image_index += 1
                    self.points = []
                    
                    if self.current_image_index < len(self.image_urls):
                        self.load_current_image()
                    else:
                        self.status_label.configure(text="All images processed! Click 'Save Results' to save.")
    
    def save_current_image_data(self):
        image_data = {
            "camID": self.camera_id.get(),
            "cordinate": self.points
        }
        self.results.append(image_data)
    
    def save_results(self):
        if not self.results:
            messagebox.showerror("Error", "No data to save!")
            return
            
        output_file = "camera_coordinates.json"
        
        # Load existing data if file exists
        existing_data = []
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        
        # Create a dictionary to store the latest data for each camera ID
        camera_data = {}
        
        # First, add existing data to dictionary
        for item in existing_data:
            cam_id = item.get("camID")
            if cam_id:
                camera_data[cam_id] = item
        
        # Then, update with new data (this will overwrite existing entries)
        for item in self.results:
            cam_id = item.get("camID")
            if cam_id:
                camera_data[cam_id] = item
        
        # Convert dictionary back to list
        updated_data = list(camera_data.values())
        
        # Save updated data
        with open(output_file, 'w') as f:
            json.dump(updated_data, f, indent=4)
        
        messagebox.showinfo("Success", f"Results saved to {output_file}")

def main():
    root = tk.Tk()
    app = CoordinateSelector(root)
    root.mainloop()

if __name__ == "__main__":
    main()