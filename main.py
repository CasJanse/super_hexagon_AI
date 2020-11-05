import network
import input_handler
import number_recognition
import time
import cv2
import win32gui
import pyautogui
import numpy as np
import pytesseract
import sys

show_debug_cv2_frame = False
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def terminate_program(line_number=0, message="Program terminated (DEBUG)"):
    sys.exit(message + "\nLine: {}".format(line_number))


def setup_number_network():
    number_model = number_recognition.create_model()
    number_model.load_weights("number_recognition/model.h5")
    return number_model


def get_window_position():
    window = win32gui.GetForegroundWindow()
    window_rect = win32gui.GetWindowRect(window)
    win32gui.SetForegroundWindow(window)
    return window_rect


def start_recording():
    start_time = time.time()
    frame_amount = 0
    frame_timestamp = time.time()

    if show_debug_cv2_frame:
        cv2.namedWindow("SH")
        cv2.moveWindow("SH", -1920, 0)

    input_handler.set_key_events()
    print("Start recording...")

    # Keep recording until the loop is broken
    while True:
        # Record a frame whenever enough time has passed since the previous frame
        if time.time() - frame_timestamp >= 1 / fps or frame_amount == 0:
            # Take the screenshot
            frame, frame_timestamp = take_screenshot()

            greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            compressed_frame = cv2.resize(greyscale_frame, (128, 72))

            # Show the recording in a separate screen if needed (disabled for performance optimisation)
            # cv2.imshow("SH", DEBUG_CUT_IMAGE)

            input_frame = np.array(compressed_frame)
            input_frame = np.reshape(input_frame, (1, 128, 72, 1))

            prediction = model.predict(input_frame)

            # Input - Arrow keys
            input_handler.release_left()
            input_handler.release_right()

            if prediction[0][0] > 0.6:
                input_handler.press_left()
            if prediction[0][1] > 0.6:
                input_handler.press_right()

            # Check if level has ended
            level_end_check(frame)

            # Get the keys that are currently held down
            input_keys = input_handler.get_keys_pressed_down()

            # Stop the recording when the q key is pressed
            if (cv2.waitKey(1) & 0xFF == ord('q')) or "q" in input_keys:
                network.save_weights(model)
                break


def take_screenshot():
    frame_timestamp = time.time()
    window = get_window_position()
    img = pyautogui.screenshot(region=(window[0] + 8, window[1] + 32, window[2] - window[0] - 16, window[3] - window[1] - 40))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, frame_timestamp


def level_end_check(frame):
    res = cv2.matchTemplate(frame, end_game_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        get_game_score(frame)


def get_game_score(frame):
    first_number_image = frame[162:194, 610:643]
    second_number_image = frame[162:194, 646:679]
    cv2.imshow("SH", second_number_image)
    first_number = get_text(first_number_image)
    second_number = get_text(second_number_image)
    if first_number:
        score = first_number * 10 + second_number
    else:
        score = second_number
    print(score)
    input_handler.press_space()
    pass


def get_text(number_image):
    number_image = cv2.cvtColor(number_image, cv2.COLOR_RGB2GRAY)
    number_image = np.array(number_image)
    number_image = np.reshape(number_image, (1, 32, 33))
    number = number_model.predict(number_image)
    if 1 in number[0]:
        return np.argmax(number[0])
    return None


number_model = setup_number_network()

high_score = 0.0
fps = 15
end_game_template = cv2.imread("template/end_screen.png")

current_model_name = "model_0"
# model = network.create_model()
model = network.load_weights(current_model_name)


time.sleep(2)
window = get_window_position()

start_recording()
