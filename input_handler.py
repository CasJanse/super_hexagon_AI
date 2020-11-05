import pyautogui
import keyboard

keys_pressed_down = []


def press_left():
    pyautogui.keyDown('left')


def release_left():
    pyautogui.keyUp('left')


def press_right():
    pyautogui.keyDown('right')


def release_right():
    pyautogui.keyUp('right')


def set_key_events():
    add_key_events("q")


def add_key_events(key):
    keyboard.on_press_key(key, lambda _: add_key_to_list(key))


def add_key_to_list(key):
    if key not in keys_pressed_down:
        keys_pressed_down.append(key)


def get_keys_pressed_down():
    return keys_pressed_down
