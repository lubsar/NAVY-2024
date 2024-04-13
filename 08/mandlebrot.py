import colorsys
import numpy as np
from PIL import Image

#x - realna zlozka, y - imaginarna
def calculateMandelbrot(c : complex, m : float, max_iter : int):
    z = 0
    num_iter = 0

    while(abs(z) <= m) and (num_iter < max_iter):
        z = (z ** 2) + c
        num_iter += 1

    return num_iter


def createPixels(width : int, height : int, x_interval : tuple[float, float], y_interval : tuple[float, float], m : float, max_iter : int):
    pixels = [0] * (width * height)
    
    x_step = (x_interval[1] - x_interval[0]) / float(width)
    y_step = (y_interval[1] - y_interval[0]) / float(height)

    y = y_interval[0] 
    for p_y in range(height): 
        x = x_interval[0]
        for p_x in range(width):
            mb = calculateMandelbrot(complex(x, y), m, max_iter)
            hue = (1.0 - (mb / float(max_iter)))
            saturation = 1.0
            value = 1.0

            pixel = colorsys.hsv_to_rgb(hue, saturation, value) if hue != 0.0 else (0.0, 0.0, 0.0)
            pixels[p_x + p_y * width] = (int(pixel[0] * 255.0), 
                                         int(pixel[1] * 255.0), 
                                         int(pixel[2] * 255.0))
            
            x += x_step
            
        y += y_step
       

    return pixels

def createMandleBrotImage(image_width : int, image_height : int, x_interval : tuple[float, float], y_interval : tuple[float, float], m : float, path) -> None:
    pixels = createPixels(image_width, image_height, x_interval, y_interval, m, 1000)
    
    array = np.array(pixels).reshape((image_height, image_width, 3))
    array = np.array(array, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save(path)

def pixel_to_coords(image_width : int, image_height : int, x_interval : tuple[float, float], y_interval : tuple[float, float], p_x : int, p_y : int) -> tuple[float, float]:
    x_step = (x_interval[1] - x_interval[0]) / float(image_width)
    y_step = (y_interval[1] - y_interval[0]) / float(image_height)

    return (x_interval[0] + p_x * x_step, y_interval[0] + p_y * y_step)

image_width = 15000
image_height = (image_width * 2) // 3

#createMandleBrotImage(image_width, image_height, (-2.0, 1.0), (-1.0, 1.0), 2.0, "15k_no_zoom.png")
#print(pixel_to_coords(image_width, image_height, (-2.0, 1.0), (-1.0, 1.0), 4067, 3481))

#createMandleBrotImage(1000, 1000, (-1.2865, -1.0865), (-0.4037, -0.2037), 2.0, "1k_zoom1.png")
#print(pixel_to_coords(1000, 1000, (-1.2865, -1.0865), (-0.4037, -0.2037), 506, 493))

createMandleBrotImage(1000, 1000, (-1.1863, -1.1843), (-0.3061, -0.3041), 2.0, "1k_zoom2.png")
