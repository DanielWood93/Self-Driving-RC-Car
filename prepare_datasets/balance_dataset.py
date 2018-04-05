import numpy as np
import pandas as pd
from random import shuffle

training_data = np.load('../datasets/joined_datasets.npy')
print('Training data: ', len(training_data))

# balance training data to have an equal amount of samples in each direction

forward_only = []
forward_left = []
forward_right = []

shuffle(training_data)

for data in training_data:
    img = data[0]
    choice = data[1]
    if choice == [0, 1, 0]:  # forward only
        forward_only.append([img, choice])

    elif choice == [1, 1, 0]:  # forward left
        forward_left.append([img, choice])

    elif choice == [0, 1, 1]:  # forward right
        forward_right.append([img, choice])

forward_only = forward_only[:983]
forward_left = forward_left[:983]
forward_right = forward_right[:983]

print('Balanced')
print('Forward: ', len(forward_only))
print('Left: ', len(forward_left))
print('Right: ', len(forward_right))

balanced_samples = forward_only + forward_left + forward_right
print('Total samples: ', len(balanced_samples))

np.save('../datasets/balanced_dataset.npy', balanced_samples)
print('done')
