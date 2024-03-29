# pylint: skip-file

import json
import sys
from pathlib import Path
from time import sleep

import requests
from picamera import PiCamera

from conf import conf

hat = f"http://{sys.argv[1]}:{conf['webserver-port']}"
aspect = sys.argv[2]

root_dir = Path("/home", "pi", "analysis", aspect)
Path.mkdir(root_dir, parents=True, exist_ok=True)

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.awb_mode = "off"

input("Align hat and hit return when ready...")


def make_outdir(colour):  # noqa: ARG001
    """Make an outdir."""
    odir = root_dir
    Path.mkdir(odir, parents=True, exist_ok=True)

    return odir


def snap(index, colour, shutter_speed=2000, suffix=""):
    """Take a picture of light `i` with colour `colour`."""
    print(
        f"Capturing light {index} with colour {colour} at shutter-speed {shutter_speed}"
    )

    outdir = make_outdir(colour)

    requests.post(  # noqa: S113
        f"{hat}/light",
        data=json.dumps({"index": index, "colour": colour}),
        headers={"Content-Type": "application/json"},
    )
    sleep(0.5)
    camera.shutter_speed = shutter_speed
    camera.capture(f"{outdir!s}/{str(index).zfill(3)}{suffix}.jpg")
    sleep(0.5)


colour = [255, 0, 0]
for index in range(conf["lights"]):
    # take a regular photo
    snap(index, colour)

    # take a longer-exposure photo
    snap(index, [255, 255, 255], 1000000, "-long")

# take a photo with all lights on
requests.post(  # noqa: S113
    f"{hat}/light-all",
    data=json.dumps({"colour": colour}),
    headers={"Content-Type": "application/json"},
)
sleep(1)
camera.capture(f"{make_outdir(colour)!s}/all.jpg")
sleep(1)
