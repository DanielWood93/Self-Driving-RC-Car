"""relabel_dataset.py
change labels of all samples in a dataset
"""

import numpy as np
from random import shuffle

dataset = np.load('datasets/sample_dataset.npy')
print('Samples in dataset: ', len(dataset))
all_data = []

for sample in dataset:
    image = sample[0]
    label = sample[1]

    # all_data.append([image, [1, 1, 0]])     # for left
    # all_data.append([image, [0, 1, 0]])     # for forward
    all_data.append([image, [0, 1, 1]])     # for right

print('Total samples: ', len(all_data))
shuffle(all_data)

# np.save('datasets/relabled_lefts.npy', all_data)
# np.save('datasets/relabled_forwards.npy', all_data)
np.save('datasets/relabled_rights.npy', all_data)
print('done')
