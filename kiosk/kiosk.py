import pyglet
from pyglet.window import key
from pyglet import font
from time import sleep
import os
import ConfigParser

class Kiosk(pyglet.window.Window):
    def __init__(self, *args, **kwargs):

        super(Kiosk, self).__init__(*args, **kwargs)

        self.image_path = "./resources/"
        self.images = []
        self.image_idx = 0

        self.printing = False


    def setup_ui(self):
        self.set_caption("Kiosk")
        # self.set_exclusive_mouse(True)
        # self.set_exclusive_keyboard(True)
        self.set_mouse_visible(False)

        self.printing_label = pyglet.text.Label(text="Printing...", x=self.width-250, y=20, font_name='Arial', font_size=30, bold=True, color=(255,255,255,255))


    def center_image(self, image):
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2

    def reset_clock(self):
        pyglet.clock.unschedule(self.next_image)
        pyglet.clock.schedule_interval(self.next_image, 10.0)

    def dismiss_dialog(self, dt):
        self.on_draw()

    def on_draw(self):

        self.clear()
        # nav_layout.draw()
        # print_layout.draw()
        self.images[self.image_idx].blit(self.width/2, self.height/2)
        if self.printing:
            self.printing_label.draw()
            self.printing = False



    def on_key_press(self, symbol, modifiers):
        global image_idx
        global printing

        if symbol == key.RIGHT:
            self.image_idx = (self.image_idx + 1) % len(self.images)
            self.reset_clock()
        elif symbol == key.LEFT:
            self.image_idx = (self.image_idx + len(self.images) -1) % len(self.images)
            self.reset_clock()
        elif symbol == key.ENTER:
            self.printing = True
            self.reset_clock()
            pyglet.clock.schedule_once(self.dismiss_dialog, 5.0)
        elif symbol == key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
        elif symbol == key.C and modifiers & key.MOD_CTRL:
            pyglet.app.exit()


    def load_images(self):
        for fn in os.listdir(self.image_path):
            if os.path.isfile(os.path.join(self.image_path, fn)):
                self.images.append(pyglet.image.load(os.path.join(self.image_path, fn)))

        for image  in self.images:
            self.center_image(image)


    def next_image(self, dt):
        self.image_idx = (self.image_idx + 1) % len(self.images)



    def start(self):

        self.setup_ui()
        self.load_images()
        pyglet.clock.schedule_interval(self.next_image, 10.0)
        pyglet.app.run()



if __name__ == '__main__':
    kiosk = Kiosk(fullscreen=True)
    kiosk.start()