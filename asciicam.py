import cv2
import time
from img2ascii import img2ascii
import sys
from shutil import get_terminal_size


def fit_to_terminal(img, max_width=None, max_height=None):
    width, height = img.shape[:2]
    aspect_ratio = height / width

    # scale by width first
    new_width = max_width or width
    new_height = int(aspect_ratio * new_width * 0.45)

    # If height too big for terminal, shrink further
    if max_height and new_height > max_height:
        new_height = max_height
        new_width = int(new_height / (aspect_ratio * 0.45))

    resized = cv2.resize(img, (new_width, new_height))
    return resized


def ascii_cam(max_height, max_width):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: could not open webcam.")
        exit()

    try:
        print("\x1b[2J")  # clear screen

        while True:
            width, _ = get_terminal_size()
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to ASCII
            frame = fit_to_terminal(frame, max_width=max_width, max_height=max_height)
            ascii_frame = img2ascii(frame, new_width=min(max_width, width-1))

            sys.stdout.write("\x1b[H")  # move cursor to top-left
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            # Control frame rate
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.stdout.flush()
        pass
    finally:
        cap.release()
        print("Stream ended.")


if __name__ == "__main__":
    ascii_cam(max_height=None, max_width=196)