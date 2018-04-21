"""join_datasets.py
join multiple datasets together
"""

import numpy as np
from random import shuffle

dataset_1 = np.load('datasets/sample_dataset1.npy')
dataset_2 = np.load('datasets/sample_dataset2.npy')
dataset_3 = np.load('datasets/sample_dataset3.npy')

all_datasets = [dataset_1, dataset_2, dataset_3]
joined = []

print('length of datasets = 1: {}, 2: {}, 3: {}'.format(dataset_1.shape, dataset_2.shape, dataset_3.shape))

for dataset in all_datasets:
    for sample in dataset:
        image = sample[0]
        label = sample[1]
        joined.append([image, label])

print('Total samples: ', len(joined))
shuffle(joined)
np.save('datasets/joined.npy', joined)
print('done')
