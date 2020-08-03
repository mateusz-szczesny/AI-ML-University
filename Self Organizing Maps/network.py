##########################################
###      Politechnika Łódzka 2020      ###
### Sieć Kohonena do kompresji obrazów ###
###      Mateusz Szczęsny - 233266     ###
###        Dawid Wójcik - 233271       ###
##########################################
import cv2.cv2 as cv2
import numpy as np
from utils import vector_length, normalize_vector, vector_distance, vector_similarity
from typing import List
import random, time, sys, math

################################
### Parametry uruchomieniowe ###
################################
FRAME_SIZE = 4  # (N x N)
IMG_WIDTH = 512
IMG_HEIGHT = 512

EPOCHS = 100
LEARNING_STEP = 0.1
NEURONS_COUNT = 8


class Image:
    def __init__(
        self,
        *,
        file: str,
        target_width: int,
        target_height: int,
        scale=cv2.IMREAD_GRAYSCALE,
    ):
        self.file = file
        self.width = target_width
        self.height = target_height
        self.scale = scale
        self.load_image()

    def load_image(self):
        self.original_image = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)
        self.image = cv2.resize(
            self.original_image, (self.height, self.width), interpolation=cv2.INTER_AREA
        )

    def convert_to_frames(self, frame_size: int):
        self.frame_size = frame_size
        temp = []
        for row_index in range(0, self.width - 1, frame_size):
            for col_index in range(0, self.height - 1, frame_size):
                temp.append(
                    (
                        self.image[
                            row_index : row_index + frame_size,
                            col_index : col_index + frame_size,
                        ]
                    ).flatten()
                )
        self.framed_image = np.array(temp)
        self.__count_brightness()
        self.__normalize_framed_image()

    @property
    def col_count(self) -> int:
        return int(self.width / self.frame_size)

    @property
    def row_count(self) -> int:
        return int(self.height / self.frame_size)

    def __count_brightness(self):
        self.image_brightness = np.array(
            [vector_length(frame) for frame in self.framed_image]
        )

    def __normalize_framed_image(self):
        self.normalized_framed_image = np.array(
            [normalize_vector(frame) for frame in self.framed_image]
        )

    def get_normal_frame(self, index) -> List[float]:
        return self.normalized_framed_image[index]

    def get_frame(self, index) -> List[float]:
        return self.framed_image[index]

    @property
    def frames_count(self) -> int:
        return self.framed_image.shape[0]


class Network:
    def __init__(
        self,
        *,
        epochs=EPOCHS,
        learning_step=LEARNING_STEP,
        neurons_count=NEURONS_COUNT,
        image,
        image_width=IMG_WIDTH,
        image_height=IMG_HEIGHT,
        frame_size=FRAME_SIZE,
        how_many_training_frames,
        logger=None,
        new_image_name=None,
    ):
        self.epochs = epochs
        self.neurons_count = neurons_count
        self.learning_step = learning_step
        self.neurons = [
            Neuron(0, 254, frame_size ** 2) for _ in range(self.neurons_count)
        ]
        self.training_frames_count = how_many_training_frames

        self.image_file = image
        self.new_image_name = new_image_name
        self.image_width = image_width
        self.image_height = image_height
        self.frame_size = frame_size

        self.logger = logger

    def generate_frames_queue(self):
        self.training_frames_queue = np.array(
            [
                random.randint(0, self.image.frames_count - 1)
                for _ in range(self.training_frames_count)
            ]
        )

    def prepare(self):
        self.image = Image(
            file=self.image_file,
            target_width=self.image_width,
            target_height=self.image_height,
        )
        self.image.convert_to_frames(self.frame_size)
        self.generate_frames_queue()

    # LEARNING LOOP
    def learn(self):
        # for each epoch
        for _ in range(self.epochs):
            # for each training frame
            for training_frame_index in self.training_frames_queue:
                matching_unit = []
                for neuron_index, neuron in enumerate(self.neurons):
                    # count distanse between each training frame and neuron
                    distance = vector_distance(
                        self.image.get_normal_frame(training_frame_index),
                        normalize_vector(neuron.weights),
                    )
                    matching_unit.append(
                        [training_frame_index, neuron_index, distance,]
                    )
            # find frame and neuron with closes distance
            bmu = min(matching_unit, key=lambda x: x[2])
            # recalculate weights for neuron
            new_weights = normalize_vector(
                self.neurons[bmu[1]].weights
            ) + self.learning_step * (
                self.image.get_normal_frame(bmu[0])
                - normalize_vector(self.neurons[bmu[1]].weights)
            )
            # update weights
            self.neurons[bmu[1]].weights = new_weights

    # COMPRESSION PART
    def compress(self):
        self._prototypes = []
        # for each frame
        for frame_index, normalized_frame in enumerate(
            self.image.normalized_framed_image
        ):
            potential_winners = []
            # for each normalized neuron weights
            for neuron in self.neurons:
                potential_winners.append(
                    (
                        frame_index,
                        neuron,
                        vector_similarity(normalized_frame, neuron.normalized_weights,),
                    )
                )
            # find the most simmilar neuron for each frame
            winner = max(potential_winners, key=lambda x: x[2],)
            # save winning neuron as prototype
            self._prototypes.append(winner[1])

    # DECOMPRESSION PART
    def decompress(self):
        new_frames = []
        # for every prototype neuron
        for i, prototype_neuron in enumerate(self._prototypes):
            # calculate new frame based on
            decompressed_frame = (
                prototype_neuron.normalized_weights * self.image.image_brightness[i]
            )
            new_frames.append(
                np.array(
                    decompressed_frame.reshape(self.frame_size, self.frame_size),
                    dtype=np.uint8,
                )
            )
        # arrange new frames
        new_frames = np.concatenate(new_frames, axis=1)

        sorted_frames = []
        # for every image row
        for x in range(0, new_frames.shape[1], self.frame_size * self.image.col_count):
            # reshape calculated frames to match original image
            sorted_frames.append(
                new_frames[:, x : x + (self.frame_size * self.image.col_count)]
            )

        # convert frames to final picture
        self.final_image = np.concatenate(sorted_frames)
        # save final image to new file
        cv2.imwrite(self.new_image_name, self.final_image)

    # generate raport of inclass parameters
    def report(self):
        self.logger.dump_to_file("==================================================")
        self.logger.dump_to_file(f"Image: {self.image}")
        self.logger.dump_to_file(f"Frame: {self.frame_size}px x {self.frame_size}px")
        self.logger.dump_to_file(f"Neurons count: {self.neurons_count}")
        self.logger.dump_to_file(f"Learning step: {self.learning_step}")
        self.logger.dump_to_file(f"Epochs count: {self.epochs}")
        self.logger.dump_to_file(
            f"Number of training frames: {self.training_frames_count}"
        )

        int_size_in_bits = sys.getsizeof(int())
        int_size_in_bytes = int(int_size_in_bits / 8)
        float_size_in_bits = sys.getsizeof(float())
        float_size_in_bytes = int(float_size_in_bits / 8)
        self.logger.dump_to_file(f"Int bits: {int_size_in_bits}")
        self.logger.dump_to_file(f"Int bytes: {int_size_in_bytes}")
        self.logger.dump_to_file(f"Float bits: {float_size_in_bits}")
        self.logger.dump_to_file(f"Float bytes: {float_size_in_bytes}")

        # bits required to store original image
        image_size_in_bits = self.image.width * self.image.height * 8
        self.logger.dump_to_file(f"Source image size in bits: {image_size_in_bits}")
        self.logger.dump_to_file(
            f"Source image size in bytes: {int(image_size_in_bits / 8)}"
        )

        # bits required to store the highest index of neuron
        bits_to_save_neurons_indexes = math.ceil(math.log(self.neurons_count, 2))

        # bits required to store lenght of each frame
        image_brigtness_size_in_bits = len(self.image.image_brightness) * (
            float_size_in_bytes
        )
        # bits required to store neurons with weights
        neurons_size_in_bits = self.neurons_count * (
            (self.frame_size ** 2) * float_size_in_bytes
        )
        # bits required to store array of prototype neurons
        prototypes_size_in_bits = len(self._prototypes) * bits_to_save_neurons_indexes

        # bit required to store compressed image (sum of factors)
        compressed_image_size_in_bits = (
            image_brigtness_size_in_bits
            + neurons_size_in_bits
            + prototypes_size_in_bits
        )
        compression_ratio = image_size_in_bits / compressed_image_size_in_bits
        self.logger.dump_to_file(
            f"Compression ratio: {'{:.4f}'.format(compression_ratio)}"
        )
        self.logger.dump_to_file(
            f"Bits count of original image: {format(image_size_in_bits, 'n')}"
        )
        self.logger.dump_to_file(
            f"Bits count of compressed image: {format(compressed_image_size_in_bits, 'n')}"
        )

        MSE = (1 / self.image.width ** 2) * np.sum(
            ((self.image.original_image - self.final_image) ** 2)
        )
        PSNR = 10 * np.log10(255 ** 2 / MSE)
        self.logger.dump_to_file(f"Mean Square Error: {'{:.4f}'.format(MSE)}")
        self.logger.dump_to_file(
            f"Peak Signal-to-Noise Ratio: {'{:.4f}'.format(PSNR)} dB"
        )
        self.logger.dump_to_file("==================================================")


class Neuron:
    def __init__(self, low: int, high: int, weights_count: int):
        self.low = low
        self.high = high
        self.weights = np.random.uniform(
            low=self.low, high=self.high, size=weights_count
        )

    @property
    def normalized_weights(self) -> List[float]:
        return normalize_vector(self.weights)

    def __str__(self) -> str:
        return f"Weights: {self.weights}"
