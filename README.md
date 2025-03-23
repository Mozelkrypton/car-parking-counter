# car-parking-counter
car parking counter in opencv 
#Parking Spot Counter
This project utilizes OpenCV to process video footage and count the number of free parking slots based on pre-defined coordinates. The program analyzes each frame of the video, converts it to grayscale, and determines the occupancy of each parking slot.

#Prerequisites
Ensure you have the following libraries installed:

OpenCV
NumPy
You can install these using pip:
#Copy code
pip install opencv-python-headless numpy
Usage
Clone the Repository:
#Copy code
git clone https://github.com/mozelkrypton/parking-spot-counter.git
cd parking-spot-counter
Specify the Video File Path:Open the script file and set the path to your video file:
python
#Copy code
video_file_path = r"C:\path\to\your\video.mp4"
Define Parking Slot Coordinates:
