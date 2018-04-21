"""convert_to_jpg.py
convert images from numpy array to .jpg files
"""

import numpy as np
import cv2

dataset = np.load('datasets/sample_dataset.npy')
print('Samples in dataset: ', len(dataset))

for count, sample in enumerate(dataset):
    image = sample[0]
    label = sample[1]

    if label == [0, 1, 0]:  # forward
        cv2.imwrite('dataset_jpg/forward/{}.jpg'.format(count + 1), image)

    elif label == [1, 1, 0]:  # forward
        cv2.imwrite('dataset_jpg/left/{}.jpg'.format(count + 1), image)

    elif label == [0, 1, 1]:  # forward
        cv2.imwrite('dataset_jpg/right/{}.jpg'.format(count + 1), image)
print('done')
