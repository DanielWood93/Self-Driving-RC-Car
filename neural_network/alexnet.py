# alexnet.py

""" AlexNet.
References:
    - Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet
    Classification with Deep Convolutional Neural Networks. NIPS, 2012.
Links:
    - [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
"""

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization


def alexnet(width, height, lr):
    network = input_data(shape=[None, width, height, 1],    # [None, image_width, image_height, layers(1 for greyscale)]
                         name='input')  # name of input data, used in train_model.py file

    network = conv_2d(network,  # incoming (tensor) incoming 4-D tensor
                      96,   # nb_filter (int) number of convolutional filters
                      11,   # filter_size (int) size of filters
                      strides=4,    # (int) strides of conv operation
                      activation='relu')    # (str) activation applied to layer (relu, rectified linear function)

    network = max_pool_2d(network,  # incoming (tensor) incoming 4-D tensor
                          3,    # pooling kernel size
                          strides=2)    # (int) strides of conv operation

    network = local_response_normalization(network)  # incoming (tensor) incoming 4-D tensor

    network = conv_2d(network,  # incoming (tensor) incoming 4-D tensor
                      256,   # nb_filter (int) number of convolutional filters
                      5,   # filter_size (int) size of filters
                      activation='relu')    # (str) activation applied to layer (relu, rectified linear function)

    network = max_pool_2d(network,  # incoming (tensor) incoming 4-D tensor
                          3,    # pooling kernel size
                          strides=2)    # (int) strides of conv operation

    network = local_response_normalization(network)  # incoming (tensor) incoming 4-D tensor

    network = conv_2d(network,  # incoming (tensor) incoming 4-D tensor
                      384,   # nb_filter (int) number of convolutional filters
                      3,   # filter_size (int) size of filters
                      activation='relu')    # (str) activation applied to layer (relu, rectified linear function)

    network = conv_2d(network,  # incoming (tensor) incoming 4-D tensor
                      384,   # nb_filter (int) number of convolutional filters
                      3,   # filter_size (int) size of filters
                      activation='relu')    # (str) activation applied to layer (relu, rectified linear function)

    network = conv_2d(network,  # incoming (tensor) incoming 4-D tensor
                      256,   # nb_filter (int) number of convolutional filters
                      3,   # filter_size (int) size of filters
                      activation='relu')    # (str) activation applied to layer (relu, rectified linear function)

    network = max_pool_2d(network,  # incoming (tensor) incoming 4-D tensor
                          3,    # pooling kernel size
                          strides=2)    # (int) strides of conv operation

    network = local_response_normalization(network)  # incoming (tensor) incoming 4-D tensor

    network = fully_connected(network,  # incoming (tensor) incoming 4-D tensor
                              4096,     # n_units (int) number of units for this layer.
                              activation='tanh')    # (str) activation applied to layer (tanh, hyperbolic tangent)

    network = dropout(network,  # incoming (tensor) incoming 4-D tensor
                      0.5)      # keep_prob (float) probability that each element is kept

    network = fully_connected(network,  # incoming (tensor) incoming 4-D tensor
                              4096,     # n_units (int) number of units for this layer
                              activation='tanh')    # (str) activation applied to layer (tanh, hyperbolic tangent)

    network = dropout(network,  # incoming (tensor) incoming 4-D tensor
                      0.5)      # keep_prob (float) probability that each element is kept

    network = fully_connected(network,  # incoming (tensor) incoming 4-D tensor
                              3,     # n_units (int) number of units for this layer
                              activation='softmax')    # (str) activation applied to layer (softmax)

    network = regression(network,  # incoming (tensor) incoming 4-D tensor
                         optimizer='momentum',  # (str) optimizer to use
                         loss='categorical_crossentropy',  # (str) Loss function used by this layer optimizer
                         learning_rate=lr,  # (float) this layer optimizer's learning rate
                         name='targets')  # (str) name for layers placeholder scope

    model = tflearn.DNN(network,  # incoming (tensor) incoming 4-D tensor
                        checkpoint_path='model_alexnet',    # (str) path to store model checkpoints
                        max_checkpoints=1,  # (int) maximum amount of checkpoints
                        tensorboard_verbose=2,  # (int) summary verbose level, 2=[Loss, Accuracy, Gradients, Weights]
                        tensorboard_dir='log')  # (str) directory to store tensorboard logs

    return model
