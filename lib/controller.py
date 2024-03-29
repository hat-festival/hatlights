import os
from multiprocessing import Process
from time import sleep

from lib.boot_sequence import boot_hat
from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes_list import load_modes, modes
from lib.oled import Oled
from lib.tools.logger import logging


class Controller:
    """Hat controller."""

    def __init__(self):
        """Construct."""
        self.conf = conf
        self.custodian = Custodian(conf=self.conf, namespace="hat")
        self.custodian.populate(flush=False)

        # we pre-load all the modes because it takes a long time
        self.modes = modes
        load_modes(self.custodian)
        self.custodian.next("mode")

        self.hat = Hat()
        self.oled = Oled(self.custodian)

        self.process = None

        boot_hat(self.custodian, self.oled, self.hat)
        self.restart_hat()

    def restart_hat(self):
        """Restart the hat."""
        logging.info("restarting hat")
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode = self.modes[self.custodian.get("mode")](self.hat)

        self.process = Process(target=self.mode.run)
        self.process.start()

        logging.info("hat restarted")
        self.oled.update()

    def next_mode(self):
        """Bump to next mode."""
        self.custodian.next("mode")
        logging.info("`mode` is now `%s`", self.custodian.get("mode"))

        self.restart_hat()

    def show_ip(self):
        """Show our IP."""
        self.custodian.set("display-type", "ip-address")
        self.oled.update()
        sleep(5)
        self.custodian.set("display-type", "show-mode")
        self.oled.update()

    def hard_reset(self):
        """Reset when we get stuck."""
        self.custodian.set("display-type", "reset")
        self.oled.update()
        logging.info("doing hard reset")

        os.system("/usr/bin/sudo service controller restart")  # noqa: S605
