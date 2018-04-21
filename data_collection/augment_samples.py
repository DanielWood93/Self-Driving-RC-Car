"""augment_samples.py
augment dataset by mirroring image and label data to create extra samples
"""

import numpy as np
from random import shuffle
import cv2

dataset = np.load('datasets/sample_dataset.npy')
print('Samples in dataset: ', len(dataset))
all_data = []

for sample in dataset:
    original_image = sample[0]
    original_label = sample[1]
    flipped_img = cv2.flip(original_image, 1)

    if original_label == [0, 1, 0]:  # forward only
        flipped_label = [0, 1, 0]

    elif original_label == [1, 1, 0]:  # forward left
        flipped_label = [0, 1, 1]

    elif original_label == [0, 1, 1]:  # forward right
        flipped_label = [1, 1, 0]

    all_data.append([original_image, original_label])
    all_data.append([flipped_img, flipped_label])

print('Total samples: ', len(all_data))
shuffle(all_data)
np.save('dataset_with_mirrored_samples.npy', all_data)
print('done')
