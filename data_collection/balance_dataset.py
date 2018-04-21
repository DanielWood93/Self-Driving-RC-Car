"""balance_dataset.py
balance dataset to get an equal number of samples in each direction
"""

import numpy as np
from random import shuffle

dataset = np.load('datasets/sample_dataset.npy')
print('Samples in dataset: ', len(dataset))

forward_samples = []
left_samples = []
right_samples = []
shuffle(dataset)  # shuffle the samples

# sort each sample by its direction label
for sample in dataset:
    image = sample[0]
    label = sample[1]
    if label == [0, 1, 0]:  # forward
        forward_samples.append([image, label])

    elif label == [1, 1, 0]:  # left
        left_samples.append([image, label])

    elif label == [0, 1, 1]:  # right
        right_samples.append([image, label])

print('Before balancing')
print('Forward samples: ', len(forward_samples))
print('Left samples: ', len(left_samples))
print('Right samples: ', len(right_samples))

shuffle(forward_samples)  # shuffle the samples
shuffle(left_samples)  # shuffle the samples
shuffle(right_samples)  # shuffle the samples

# find which direction has lowest number of samples and reduce all directions to that length
lowest_samples = min(len(forward_samples), len(left_samples), len(right_samples))
forward_samples = forward_samples[:lowest_samples]
left_samples = left_samples[:lowest_samples]
right_samples = right_samples[:lowest_samples]

print('After balancing')
print('Forward samples: ', len(forward_samples))
print('Left samples: ', len(left_samples))
print('Right samples: ', len(right_samples))

balanced = forward_samples + left_samples + right_samples
print('Total samples: ', len(balanced))

shuffle(balanced)  # shuffle the samples
np.save('datasets/balanced_dataset.npy', balanced)  # save to new dataset file
print('done')
