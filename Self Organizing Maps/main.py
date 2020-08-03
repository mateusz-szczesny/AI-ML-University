##########################################
###      Politechnika Łódzka 2020      ###
### Sieć Kohonena do kompresji obrazów ###
###      Mateusz Szczęsny - 233266     ###
###        Dawid Wójcik - 233271       ###
##########################################
import time
from logger import Logger
from network import Network
import numpy as np

IMAGES = [
    "img/lena.png",
    "img/parrot.png",
    "img/boat.png",
    "img/oskar.jpg",
]

###############
### Program ###
###############
if __name__ == "__main__":
    np.random.seed(100)

    logger = Logger(path=f"log/")
    network = Network(
        epochs=150,
        learning_step=0.05,
        neurons_count=8,
        image=IMAGES[0],
        image_width=512,
        image_height=512,
        frame_size=2,
        how_many_training_frames=512,
        logger=logger,
        new_image_name=f"log/compressed_{int(time.time())}.png",
    )

    network.prepare()
    network.learn()
    network.compress()
    network.decompress()
    network.report()
