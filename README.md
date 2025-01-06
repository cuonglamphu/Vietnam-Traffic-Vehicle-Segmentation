# Vietnam Traffic Vehicle Segmentation (VTVS)

## Introduction

Vietnam Traffic Vehicle Segmentation (VTVS) is a research tool designed by Data4Life team to analyze traffic conditions using YOLO (You Only Look Once) for vehicle detection and segmentation. VTVS allows users to define a Region of Interest (ROI) and calculate congestion levels based on vehicle density within the specified area (using pre-defined ROI).

## Features

-   **Vehicle Detection**: Accurately detect vehicles using YOLO.
-   **ROI Customization**: Define custom Regions of Interest (ROI) for traffic analysis.
-   **Congestion Calculation**: Calculate congestion percentage based on vehicle density.
-   **Visualization**: Generate visual results with highlighted ROI and congestion levels.
-   **Docker Support**: Easy deployment using Docker and Docker Compose.

## Requirements

-   Docker ([Installation Guide](https://docs.docker.com/engine/install/))
-   Docker Compose
-   Python 3.10

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/cuonglamphu/Vietnam-Traffic-Vehicle-Segmentation.git
    cd Vietnam-Traffic-Vehicle-Segmentation
    ```

2. **Install Docker and Docker Compose**
   Ensure that Docker and Docker Compose are installed on your machine. Refer to the official documentation for installation instructions:
    - [Docker Installation](https://docs.docker.com/get-docker/)
    - [Docker Compose Installation](https://docs.docker.com/compose/install/)

## Running the Application

0. **Load model**

    - Download the pre-trained model and put it into the `pretrained_models/` directory
    - Change the model name (the `model_name` variable) in the `yolo_model.py` file
    - You can also use your own model by putting it into the `pretrained_models/` directory and change the model name (the `model_name` variable) in the `yolo_model.py` file
    - ** Our pre-trained is available here**: [here](https://drive.google.com/file/d/1ZEUUb8SDYpF2WVmUcrLnVhsA4nEFhibQ/view?usp=sharing)

1. **Build and Run the Container**

    - **First Time**: Build and run the container using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    - **Subsequent Runs**: Start the container without rebuilding:

    ```bash
    docker-compose up
    ```

2. **Define ROI Coordinates**
   Modify the `roi_coordinates` variable in the `main.py` file to specify the Region of Interest (ROI) in the format:

    ```python
    roi_coordinates = [(25, 280), (295, 76), (422, 83), (452, 283)]
    ```

    **Pro Tip**: Use the `tools/getcordinate.py` script to interactively select ROI coordinates with a GUI.

3. **View Results**
    - **Output Image**: The processed image with ROI and congestion analysis will be saved to `result/result.jpg`.
    - **Console Output**: The congestion percentage will be printed in the console.

## Notes

-   **Model File**: Ensure that the YOLO model file (`best.pt`) or your custom model is placed in the `pretrained_models/` directory.
-   **GUI Issues**: If you encounter issues with the GUI, ensure that your environment variables are correctly configured and that an X11 server is installed if needed.

## Screenshots

-   **ROI Selection**:
-   **Congestion Analysis**:

## References

-   [YOLO Documentation](https://docs.ultralytics.com/)
-   [OpenCV Documentation](https://docs.opencv.org/)
-   [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.
