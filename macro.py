import pyautogui
import time
import main

pt = main.PATH
for s in pt:
    pyautogui.keyDown(s)
    #time.sleep(0.)
    pyautogui.keyUp(s)
    #time.sleep(0.1)