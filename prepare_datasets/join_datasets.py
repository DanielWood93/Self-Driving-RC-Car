import numpy as np
import pandas as pd
from random import shuffle

# combine multiple datasets into 1 file

dataset_1 = np.load('../datasets/relabled_lefts.npy')
dataset_2 = np.load('../datasets/relabled_rights.npy')
dataset_3 = np.load('../datasets/relabled_forwards.npy')

all_datasets = [dataset_1, dataset_2, dataset_3]
all_data = []

print('dataset_1: ', dataset_1.shape))
print('dataset_2: ', dataset_2.shape))
print('dataset_3: ', dataset_3.shape))

for sets in all_sets:
    for sample in sets:
        img = sample[0]
        choice = sample[1]
        all_data.append([img, choice])

print('Total samples: ', len(all_data))
shuffle(all_data)
np.save('../datasets/joined_datasets.npy', all_data)
print('done')
