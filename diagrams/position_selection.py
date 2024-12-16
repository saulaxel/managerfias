import tkinter as tk
from PIL import ImageTk, Image
import os

WINDOW_SCALE = .25

root = tk.Tk()
root.resizable(width=True, height=True)


# Aux functions
def image_to_canvas(x: int, y: int) -> tuple[int, int]:
    ''' Transforms image coordinates to screen coordinates'''
    return int(x * WINDOW_SCALE), int(y * WINDOW_SCALE)


def canvas_to_image(cx: int, cy: int) -> tuple[int, int]:
    ''' Transforms screen coordinates to image coordinates'''
    return int(cx / WINDOW_SCALE), int(cy / WINDOW_SCALE)


# events
def set_product_position(event):
    x = event.x
    y = event.y

    img_x, img_y = canvas_to_image(x, y)

    print(f'Click at screen (x={x}, y={y}) image (x={img_x}, y={img_y})')


# Preparing the image
img_width = 1920
img_height = 1080
img = Image.open('esquina-libretas.png')

# Canvas to paint the images and other things
cw, ch = image_to_canvas(img_width, img_height)

resized_image = img.resize((cw, ch), Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(resized_image)
canvas = tk.Canvas(root, width=cw, height=ch, bg='white')
canvas.create_image(0, 0, image=tk_image, anchor=tk.NW)
canvas.pack()
canvas.bind("<Button-1>", set_product_position)

root.mainloop()
