import pyglet
from pyglet.window import key
import os
import ConfigParser

import util


class Kiosk(pyglet.window.Window):

    image_path = "resources"
    view_path = "ads"
    print_path = "coupons"
    view_file_prefix = "ad_"
    print_file_prefix = "cpn_"
    view_time = 10.0

    def __init__(self, *args, **kwargs):
        super(Kiosk, self).__init__(*args, **kwargs)

        self.images = []
        self.image_idx = 0

        self.usbdrive = ''

    def setup_ui(self):
        self.set_caption("Kiosk")
        # self.set_exclusive_mouse(True)
        # self.set_exclusive_keyboard(True)
        self.set_mouse_visible(False)

        self.printing_label = pyglet.text.Label(text="",
                                                x=self.width-600, y=20,
                                                font_name='Arial', font_size=28, bold=True,
                                                color=(255,255,255,255))
        self.error_label = pyglet.text.Label(text="",
                                             x=self.width/2, y=self.height/2,
                                             anchor_x='center', anchor_y='center',
                                             font_name='Arial', font_size=20, bold=True,
                                             color=(255,255,255,255))

    def reset_clock(self):
        pyglet.clock.unschedule(self.next_image)
        pyglet.clock.schedule_interval(self.next_image, self.view_time)

    def dismiss_dialog(self, dtime):
        # Callback for removing status messages

        # Clear any previously set messages
        self.error_label.text = ""
        self.printing_label.text = ""

        self.on_draw()

    def error_dialog(self, err_message):
        self.error_label.text = err_message
        # self.reset_clock()
        # pyglet.clock.schedule_once(self.dismiss_dialog, 5.0)

    def on_draw(self):

        self.clear()
        # nav_layout.draw()
        # print_layout.draw()
        if len(self.images) > 0:
            self.images[self.image_idx][1].blit(self.width/2, self.height/2)

        if len(self.printing_label.text) > 0:
            self.printing_label.draw()
            self.printing_label.text = ""

        if len(self.error_label.text) > 0:
            self.error_label.draw()

    def on_key_press(self, symbol, modifiers):

        if symbol == key.RIGHT:
            self.image_idx = (self.image_idx + 1) % len(self.images)
            self.reset_clock()
        elif symbol == key.LEFT:
            self.image_idx = (self.image_idx + len(self.images) - 1) % len(self.images)
            self.reset_clock()
        elif symbol == key.ENTER:
            self.send_print(self.images[self.image_idx][0])
        elif symbol == key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
        elif symbol == key.C and modifiers & key.MOD_CTRL:
            pyglet.app.exit()

    def load_images(self, dtime):

        # Verify resource drive is available
        if util.usbdrive_available():
            self.usbdrive = util.get_usb_drive()
            # Verify resource folders are valid
            full_path = os.path.join(self.usbdrive, self.image_path, self.view_path)
            if os.path.isdir(full_path):
                # Looks like resources are available so go ahead and load them after validating names
                for fn in os.listdir(full_path):
                    if os.path.isfile(os.path.join(full_path, fn)) and fn[:len(self.view_file_prefix)] == self.view_file_prefix:
                        self.images.append((fn, pyglet.image.load(os.path.join(full_path, fn))))
                if len(self.images) > 0:
                    for image in self.images:
                        self.center_image(image[1])

                    # Clear any errors in case drive was hot plugged
                    pyglet.clock.unschedule(self.load_images)
                    self.dismiss_dialog(0)
                    pyglet.clock.schedule_interval(self.next_image, self.view_time)
                else:
                    self.error_dialog("Error: No valid resources found!")
                    pyglet.clock.schedule_interval(self.load_images, self.view_time)
            else:
                self.error_dialog("Error: Resource folder not found!")
                pyglet.clock.schedule_interval(self.load_images, self.view_time)
        else:
            self.error_dialog("Error: Resource drive not found!")
            pyglet.clock.schedule_interval(self.load_images, self.view_time)

    def center_image(self, image):
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2

    def next_image(self, dtime):
        # Callback for auto-increment
        if len(self.images) > 0:
            self.image_idx = (self.image_idx + 1) % len(self.images)

    def send_print(self, fname):
        if len(fname) > 0:
            print_name = ''.join([self.print_file_prefix, fname[len(self.view_file_prefix):]])
            if os.path.isfile(os.path.join(self.usbdrive, self.image_path, self.print_path, print_name)):
                self.printing_label.text = "Printing: {0}".format(print_name)
            else:
                self.error_dialog("Error: Print file '{0}' not found".format(print_name))
            self.reset_clock()
            pyglet.clock.schedule_once(self.dismiss_dialog, 5.0)

    def start(self):

        self.setup_ui()
        self.load_images(0)
        pyglet.app.run()


if __name__ == '__main__':
    kiosk = Kiosk(fullscreen=True)
    kiosk.start()