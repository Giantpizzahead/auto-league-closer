import cv2
from .context import *
from . import findimg
import numpy as np
import mss
import time
import tkinter as tk
from tkinter import messagebox

# This code is to hide the main tkinter window
root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.eval("tk::PlaceWindow . center")
root.withdraw()


def show_error(message):
    messagebox.showerror("Error", message, parent=root)
    root.withdraw()


def process_image(img):
    # Check if league is on screen using find_template
    navbar_template = cv2.imread(str(MODULE_PATH / "data" / "leaguenavbar.png"))
    navbar_match = findimg.find_template(img, navbar_template)

    # exit_template = cv2.imread(str(MODULE_PATH / "data" / "leagueexit.png"))
    # exit_match = findimg.find_template(img, exit_template)
    exit_match = False

    if navbar_match:
        LOG.warning("League is on screen")
        show_error("WHAT ARE YOU DOING\nCLOSE LEAGUE LMAO")
        return True
    elif exit_match:
        LOG.warning("Exit dialog is on screen")
        show_error("do it you won't")
        return True


def main():
    with mss.mss() as sct:
        pause_time = 0
        last_time = time.time()
        while True:
            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(sct.monitors[1]))

            # Check for League
            if time.time() - 1 >= pause_time:
                if process_image(img):
                    # League found; wait a bit before starting again
                    pause_time = time.time()

            # Display the picture
            # cv2.imshow("OpenCV/Numpy normal", img)

            # Display the picture in grayscale
            # cv2.imshow('OpenCV/Numpy grayscale',
            #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            LOG.debug(f"FPS: {1 / (time.time() - last_time):.2f}")
            last_time = time.time()

            # # Press "q" to quit
            # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
            #     break


# def main():
#     # https://stackoverflow.com/a/51607041
#     # Get images
#     image = cv2.imread(
#         str(MODULE_PATH / ".." / "tests" / "data" / "leaguenavbar" / "navbar4.png")
#     )
#     template = cv2.imread(str(MODULE_PATH / "data" / "leaguenavbar.png"))
#     # image = cv2.imread(str(MODULE_PATH / "data" / "leaguenavbar.png"))

#     image = cv2.imread("/Users/kylefu/Desktop/auto-league-closer/tests/data/leaguenavbar/navbar5.png")
#     template = cv2.imread("/Users/kylefu/Desktop/auto-league-closer/tests/data/smileytemplates/smiley2.png")

#     # Find template in image
#     import time
#     start = time.time()
#     match = findimg.find_template(image, template, preprocessed=False)
#     print(f"Time taken: {time.time() - start:.2f} seconds")

#     # Visualize match
#     if not match:
#         print("No match found")
#         return
#     print(f"{match=}")
#     cv2.rectangle(image, (match.x, match.y), (match.x+match.w, match.y+match.h), (0, 255, 0), 3)
#     image[0:0+template.shape[0], 0:0+template.shape[1]] = template
#     cv2.imshow("Visualize", image)
#     cv2.waitKey(0)


if __name__ == "__main__":
    main()
