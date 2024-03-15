from lib.modes.brain_waves import BrainWaves
from lib.modes.crawler import Crawler
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.subtle_roller import SubtleRoller

modes = {
    "subtleroller": SubtleRoller,
    "larsen": Larsen,
    "crawler": Crawler,
    # "eye": Eye,
    "brainwaves": BrainWaves,
    "pulsator": Pulsator,
    # "bigtop": BigTop,
    # "cuttlefish": Cuttlefish,
    # # "directiontester": DirectionTester,
    # "sweeper": Sweeper,
    # "accelerator": Accelerator,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
