import pyglet
from pyglet.window import key
from pyglet import font
from time import sleep
import os

image_path = "./resources/"

# window = pyglet.window.Window(800, 600)
window = pyglet.window.Window(fullscreen=True)
window.set_caption("Kiosk")
# window.set_exclusive_mouse(True)
# window.set_exclusive_keyboard(True)
window.set_mouse_visible(False)


nav_document = pyglet.text.decode_attributed("Use WHITE buttons to go to previous or next screen")
nav_document.set_style(0, len(nav_document.text), dict(font_name='Arial', font_size=14, color=(172,172,172,255)))
nav_document.set_style(4, 9, dict(font_name='Arial', bold=True, color=(255,255,255,255)))
nav_layout = pyglet.text.layout.TextLayout(nav_document, 250, 100, multiline=True)
nav_layout.x = window.width-320
nav_layout.y = (window.height/3)*2


print_document = pyglet.text.decode_attributed(text="Press RED button to print a coupon")
print_document.set_style(0, len(nav_document.text), dict(font_name='Arial', font_size=14, color=(172,172,172,255)))
print_document.set_style(6, 9, dict(font_name='Arial', bold=True, color=(255,0,0,255)))
print_layout = pyglet.text.layout.TextLayout(print_document, 320, 100, multiline=True)
print_layout.x = window.width-320
print_layout.y = window.height/3

images = []
image_idx = 0

# printing_label = pyglet.text.Label(text="Printing...", x=window.width/2, y=window.height/2, anchor_x='center', anchor_y='center', font_name='Arial', font_size=30, bold=True, color=(255,255,255,255))
printing_label = pyglet.text.Label(text="Printing...", x=window.width-250, y=(window.height/3)+20, font_name='Arial', font_size=30, bold=True, color=(255,255,255,255))
printing = False


def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

def reset_clock():
    pyglet.clock.unschedule(next_image)
    pyglet.clock.schedule_interval(next_image, 10.0)


def dismiss_dialog(self):
    on_draw()

def next_image(self):
    global image_idx

    image_idx = (image_idx + 1) % len(images)


@window.event
def on_draw():
    global printing

    window.clear()
    nav_layout.draw()
    print_layout.draw()
    images[image_idx].blit(window.width/2, window.height/2)
    if printing:
        printing_label.draw()
        printing = False



@window.event
def on_key_press(symbol, modifiers):
    global image_idx
    global printing

    if symbol == key.RIGHT:
        image_idx = (image_idx + 1) % len(images)
        reset_clock()
    elif symbol == key.LEFT:
        image_idx = (image_idx + len(images) -1) % len(images)
        reset_clock()
    elif symbol == key.ENTER:
        printing = True
        reset_clock()
        pyglet.clock.schedule_once(dismiss_dialog, 5.0)
    elif symbol == key.ESCAPE:
        return pyglet.event.EVENT_HANDLED
    elif symbol == key.C and modifiers & key.MOD_CTRL:
        pyglet.app.exit()



def main():

    # global window
    global image_idx

    for fn in os.listdir(image_path):
        if os.path.isfile(os.path.join(image_path, fn)):
            images.append(pyglet.image.load(os.path.join(image_path, fn)))

    for image  in images:
        center_image(image)

    pyglet.clock.schedule_interval(next_image, 10.0)

    pyglet.app.run()


if __name__ == '__main__':
    main()