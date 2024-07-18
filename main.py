import cv2
import numpy as np
import time

# Import video raw image from a Seville camera footage, provide the path 
video_file_path = r"C:\Users\Admin\OneDrive\Desktop\wallpaper\cp.mp4"
video_capture = cv2.VideoCapture(video_file_path)

# Define parking slot coordinates and dimensions
parking_coordinates = [(402, 239), (753, 377), (55, 100), (56, 146), (51, 241), (53, 290), 
                       (51, 192), (405, 189), (402, 138), (405, 90), (514, 92), (511, 139), 
                       (514, 187), (512, 236), (163, 99), (164, 147), (158, 194), (159, 243), 
                       (161, 290), (55, 337), (162, 339), (160, 388), (162, 429), (52, 431), 
                       (53, 479), (163, 479), (168, 525), (165, 576), (165, 620), (56, 623), 
                       (51, 573), (52, 527), (402, 289), (402, 338), (404, 382), (405, 427), 
                       (405, 526), (403, 569), (406, 619), (512, 524), (512, 568), (513, 620), 
                       (511, 426), (511, 380), (513, 329), (511, 284), (751, 88), (751, 136), 
                       (750, 188), (753, 232), (753, 276), (751, 327), (757, 427), (753, 472), 
                       (757, 518), (760, 573), (760, 616), (901, 620), (901, 576), (892, 141), 
                       (892, 190), (893, 235), (894, 284), (897, 330), (898, 375), (901, 424), 
                       (903, 474), (899, 522), (46, 385)]
rect_width, rect_height = 100, 33
slot_color = (0, 0, 255)
slot_thickness = 1
occupancy_threshold = 30
last_updated_time = time.time()
previous_free_slots = 0

def convert_to_grayscale(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = frame.copy()
    contour_image[:] = 0
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=2)
    return contour_image

def mark_parking_slots(frame, grayscale_frame):
    global last_updated_time, previous_free_slots
    current_time = time.time()
    free_slots_count = 0
    for x, y in parking_coordinates:
        x_start, x_end = x + 10, x + rect_width - 11
        y_start, y_end = y + 4, y + rect_height
        start_point, end_point = (x_start, y_start), (x_end, y_end)
        cropped_region = grayscale_frame[y_start:y_end, x_start:x_end]
        gray_cropped_region = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
        non_zero_count = cv2.countNonZero(gray_cropped_region)
        slot_color, slot_thickness = [(0, 255, 0), 5] if non_zero_count < occupancy_threshold else [(0, 0, 255), 2]
        if non_zero_count < occupancy_threshold:
            free_slots_count += 1
        cv2.rectangle(frame, start_point, end_point, slot_color, slot_thickness)

    if current_time - last_updated_time >= 0.1:
        cv2.putText(frame, "Free  Parking Slots: " + str(free_slots_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
        last_updated_time = current_time
        previous_free_slots = free_slots_count
    else:
        cv2.putText(frame, "Free  Parking Slots: " + str(previous_free_slots), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
    return frame

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    grayscale_frame = convert_to_grayscale(frame)
    output_frame = mark_parking_slots(frame, grayscale_frame)
    cv2.imshow("Parking Spot Counter", output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
