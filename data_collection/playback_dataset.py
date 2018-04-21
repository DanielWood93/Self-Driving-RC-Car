"""playback_dataset.py
playback and view captured samples
"""

import numpy as np
import cv2
import time

dataset = np.load('datasets/sample_dataset.npy')
print('Samples in dataset: ', len(dataset))

for count, sample in enumerate(dataset):
    image = sample[0]
    label = sample[1]
    print(image.shape)
    cv2.imshow('Image Data'.format(count + 1), image)
    print('Sample {} of {} - Label: {}'.format(count+1, len(dataset), label))
    # time.sleep(0.5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
