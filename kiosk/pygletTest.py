import pyglet
from pyglet.window import key
import time

# window = pyglet.window.Window(800, 600)
window = pyglet.window.Window(fullscreen=True)
window.set_mouse_visible(False)
window.set_exclusive_mouse(True)

images = []
image_idx = 0

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2


@window.event
def on_draw():
    window.clear()
    # window.set_size(images[image_idx].width, images[image_idx].height)
    # images[image_idx].blit(0, 0)
    images[image_idx].blit(window.width/2, window.height/2)


@window.event
def on_key_press(symbol, modifiers):
    global image_idx
    if symbol == key.RIGHT:
        image_idx = (image_idx + 1) % len(images)
    elif symbol == key.LEFT:
        image_idx = (image_idx + len(images) -1) % len(images)
    elif symbol == key.ENTER:
        print 'The enter key (PRINT) was pressed.'
    elif symbol == key.ESCAPE:
        return pyglet.event.EVENT_HANDLED
    elif symbol == key.C and modifiers & key.MOD_CTRL:
        pyglet.app.exit()



def main():

    global image_idx

    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    images.append(pyglet.image.load("./resources/test01.jpg"))
    images.append(pyglet.image.load("./resources/test02.jpg"))
    images.append(pyglet.image.load("./resources/test03.jpg"))

    for image  in images:
        center_image(image)

    pyglet.app.run()


if __name__ == '__main__':
    main()