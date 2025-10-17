import cv2


def img2ascii(img, new_width=100) -> str:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    edges = cv2.Canny(gray, 50, 150)
    gray = cv2.addWeighted(gray, 0.8, edges, 0.5, 0)

    height, width = gray.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.45)
    resized = cv2.resize(gray, (new_width, new_height))

    # ascii_chars = "@%#*+=-:. "    # Darkness is '@', Lightness is ' '
    ascii_chars = " .:-=+*#%@"      # Darkness is ' ', Lightness is '@'

    ascii_str = ""
    for row in resized:
        for pixel in row:
            intensity = int(pixel)
            ascii_str += ascii_chars[intensity * len(ascii_chars) // 256]
        ascii_str += "\n"
    
    return ascii_str

