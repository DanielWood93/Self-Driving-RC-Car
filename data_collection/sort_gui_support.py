import numpy as np
import cv2
from random import shuffle

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

current_sample_id = 0
good_forwards_arr = []
good_lefts_arr = []
good_rights_arr = []
loaded_from_dataset_tools = []


def load_forwards_dataset():
    global loaded_dataset
    global current_sample_id
    loaded_dataset = np.load("datasets/forwards_dataset.npy")
    print('Loaded forwards dataset, Length is: ', len(loaded_dataset))
    sys.stdout.flush()
    load_sample()


def load_lefts_dataset():
    global loaded_dataset
    global current_sample_id
    loaded_dataset = np.load("datasets/lefts_dataset.npy")
    print('Loaded lefts dataset, Length is: ', len(loaded_dataset))
    sys.stdout.flush()
    load_sample()


def load_rights_dataset():
    global loaded_dataset
    global current_sample_id
    print("use forwards only")
    loaded_dataset = np.load("datasets/rights_dataset.npy")
    print('Loaded rights dataset, Length is: ', len(loaded_dataset))
    sys.stdout.flush()
    load_sample()


def load_sample():
    global image_data
    global choice_data
    image_data = loaded_dataset[current_sample_id, 0]
    choice_data = loaded_dataset[current_sample_id, 1]

    if choice_data == [0, 1, 0]:  # forward only
        print(current_sample_id, ": ", choice_data)

    elif choice_data == [1, 1, 0]:  # forward left
        print(current_sample_id, ": ", choice_data)

    elif choice_data == [0, 1, 1]:  # forward right
        print(current_sample_id, ": ", choice_data)
    display_image(image_data)


def display_image(image):
    global current_sample_id
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def check_collected_samples():
    print("----------")
    print("lefts: ", len(good_lefts_arr))
    print("rights: ", len(good_rights_arr))
    print("forwards: ", len(good_forwards_arr))
    print("----------")


def set_forward():
    global good_forwards_arr
    global choice_data
    choice_data == [0, 1, 0]
    good_forwards_arr.append([image_data, choice_data])
    next_sample()


def set_left():
    global good_lefts_arr
    global choice_data
    choice_data == [1, 0, 0]
    good_lefts_arr.append([image_data, choice_data])
    next_sample()


def set_right():
    global good_rights_arr
    global choice_data
    choice_data == [0, 0, 1]
    good_rights_arr.append([image_data, choice_data])
    next_sample()


def undo_last_forward():
    del good_forwards_arr[-1]
    print('removed last element from forwards')
    sys.stdout.flush()


def undo_last_left():
    del good_lefts_arr[-1]
    print('removed last element from forwards')
    sys.stdout.flush()


def undo_last_right():
    del good_rights_arr[-1]
    print('removed last element from forwards')
    sys.stdout.flush()


def next_sample():
    global current_sample_id
    current_sample_id = current_sample_id + 1
    load_sample()


def prev_sample():
    global current_sample_id
    current_sample_id = current_sample_id - 1
    load_sample()


def save_as_separate_datasets():
    np.save('good_forwards.npy', good_forwards_arr)
    np.save('good_lefts.npy', good_lefts_arr)
    np.save('good_rights.npy', good_rights_arr)
    print('sort_gui_support.save_as_separate_dataset')
    sys.stdout.flush()


def save_forwards_only():
    print('sort_gui_v2_support.save_forwards_only')
    sys.stdout.flush()


def save_lefts_only():
    print('sort_gui_v2_support.save_lefts_only')
    sys.stdout.flush()


def save_rights_only():
    print('sort_gui_v2_support.save_rights_only')
    sys.stdout.flush()


# ----- dataset tools -----
def load_dataset_1():
    global loaded_from_dataset_tools
    loaded_from_dataset_tools = np.load("dataset_1.npy")
    print('Loaded dataset 1, Length is: ', len(loaded_from_dataset_tools))
    sys.stdout.flush()

def load_dataset_2():
    global loaded_from_dataset_tools
    loaded_from_dataset_tools = np.load("dataset_2.npy")
    print('Loaded dataset 1, Length is: ', len(loaded_from_dataset_tools))
    sys.stdout.flush()


def load_dataset_3():
    global loaded_from_dataset_tools
    loaded_from_dataset_tools = np.load("dataset_3.npy")
    print('Loaded dataset 1, Length is: ', len(loaded_from_dataset_tools))
    sys.stdout.flush()


def flip_and_duplicate():
    global loaded_from_dataset_tools
    data_with_flipped = []
    for sample in loaded_from_dataset_tools:
        original_image = sample[0]
        original_label = sample[1]
        flipped_image = cv2.flip(original_image, 1)

        if original_label == [0, 1, 0]:  # forward only
            flipped_label = [0, 1, 0]

        elif original_label == [1, 1, 0]:  # forward left
            flipped_label = [0, 1, 1]

        elif original_label == [0, 1, 1]:  # forward right
            flipped_label = [1, 1, 0]

        data_with_flipped.append([original_image, original_label])
        data_with_flipped.append([flipped_image, flipped_label])

    print("Total samples: ", len(data_with_flipped))
    shuffle(data_with_flipped)
    np.save('with_duplicated_samples.npy', data_with_flipped)
    print("flipped and mixed with original samples")


def convert_to_rgb():
    global loaded_from_dataset_tools
    rgb_data = []
    for sample in loaded_from_dataset_tools:
        original_image = sample[0]
        original_label = sample[1]
        rgb_image = np.stack((original_image,) * 3, -1)
        rgb_data.append([rgb_image, original_label])
    np.save('rgb_data.npy', rgb_data)
    print("converted to rgb")


def dataset_tools_save():
    print('sort_gui_v2_support.dataset_tools_save')
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import sort_gui

    loaded_dataset = []

    image_data = 0
    choice_data = [0, 0, 0]
    sort_gui.vp_start_gui()