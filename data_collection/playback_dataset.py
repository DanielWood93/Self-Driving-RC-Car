import numpy as np
import cv2

training_data = np.load('dataset.npy')

for count, sample in enumerate(training_data):
    frame_data = sample[0]
    input_data = sample[1]
    cv2.imshow('Image Data'.format(count+1), frame_data)
    print('Sample {} of {} - Input Data: {}'.format(count+1, len(training_data), input_data))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
