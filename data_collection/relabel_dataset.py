import numpy as np
from random import shuffle

to_relabel = np.load('../datasets/rights.npy')
all_data = []

for data in to_relabel:
    img = data[0]
    choice = data[1]
    all_data.append([img, [0,1,1]])

print('Total samples: ', len(all_data))
shuffle(all_data)
np.save('../datasets/relabeled_rights.npy', all_data)
print('done')
