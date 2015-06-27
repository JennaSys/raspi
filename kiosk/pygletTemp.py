import pyglet

window = pyglet.window.Window(800, 600)

score_label = pyglet.text.Label(text="Score: 0", x=10, y=575)
level_label = pyglet.text.Label(text="My Amazing Game", x=400, y=575, anchor_x='center')

images = []

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2


@window.event
def on_draw():
    window.clear()
    level_label.draw()
    score_label.draw()
    images[0].blit(0, 0)


def main():
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    images.append(pyglet.resource.image("test01.jpg"))
    images.append(pyglet.resource.image("test02.jpg"))
    images.append(pyglet.resource.image("test03.jpg"))

    # for image in images:
    #     center_image(image)

    pyglet.app.run()


if __name__ == '__main__':
    main()