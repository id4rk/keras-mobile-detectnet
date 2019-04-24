import os
import cv2
import plac
import numpy as np
from imgaug import augmenters as iaa
import imgaug as ia


def create_augmenter(stage: str = "train"):
    if stage == "train":
        return iaa.Sequential([
        iaa.Fliplr(0.5),
        iaa.CropAndPad(px=(0, 112), sample_independently=False),
        iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}),
        iaa.SomeOf((0, 3), [
            iaa.AddToHueAndSaturation((-10, 10)),
            iaa.Affine(scale={"x": (0.9, 1.1), "y": (0.9, 1.1)}),
            iaa.GaussianBlur(sigma=(0, 1.0)),
            iaa.AdditiveGaussianNoise(scale=0.1 * 255)
        ])
    ])
    elif stage == "val":
        return iaa.Sequential([
            iaa.CropAndPad(px=(0, 112), sample_independently=False),
            iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)})
        ])
    elif stage == "test":
        return iaa.Sequential([])


@plac.annotations(
    test_path=("Path to images", "positional", None, str),
    stage=("Augmentation stage", "option", "S", str)
)
def main(test_path: str = "test",
         stage: str = "train"):

    seq = create_augmenter(stage)

    for r, d, f in os.walk(test_path):
        for file in f:
            image_full = cv2.imread(os.path.join(r, file))

            image_input = cv2.resize(image_full, (224, 224))

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_image(image_input)
            ia.imshow(image_aug)


if __name__ == '__main__':
    plac.call(main)