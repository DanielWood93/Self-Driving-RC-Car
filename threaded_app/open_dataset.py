import os
import numpy as np
import cv2

training_data = np.load("dataset.npy")

for data in training_data:
    img = data[0]
    choice = [1]
    cv2.imshow("test", img)
    print(choice)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
