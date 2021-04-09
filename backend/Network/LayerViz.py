import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import tensorflow as tf
from tensorflow import keras
import cv2
from PIL import Image
import re
import pathlib
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import keras
import os

from models import *

def LayerVisualise(model_name,image_path = "./Data/Train/00000_00006_00029.png"):

    '''
    Returns visualisation of image after passing through the model, for each layer
        Parameters:
            model_name: name of model user passes
            
            image_path: path of the image
            
    '''
    count = np.load('./Data/isLess.npy')
    mypath = "./Network/UserLayers"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

    f = open('./Network/net_mod.json')

    data = json.load(f)
    count = np.load('./Data/isLess.npy')
    num_classes = len(count) - sum(count)

    regularizer_type = data[model_name]['regularizer_type']
    regularizer_value = data[model_name]['regularizer_value']
    dropout_prob = data[model_name]['dropout_prob']

    files = os.listdir('./Network/weights')
    weight_path = './Network/weights/' + model_name + '/'  + files[-1] 

    if model_name == 'baseline':
        model = create_baseline(num_classes, dropout_prob, regularizer_type, regularizer_value)
    elif model_name == 'mobilenet':
        model = create_mobilenet(num_classes, dropout_prob)
    elif model_name == 'resnet':
        model = create_resnet(num_classes, dropout_prob)
    elif model_name == 'googlenet':
        model = create_googlenet(num_classes, dropout_prob)

    IMG_HEIGHT = 48
    IMG_WIDTH = 48
    model.load_weights(weight_path)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_fromarray = Image.fromarray(image, 'RGB')
    image = image_fromarray.resize((IMG_HEIGHT , IMG_WIDTH))
    image = np.array(image)/255
    image = np.expand_dims(image, axis=0)

    successive_outputs = [layer.output for layer in model.layers[1:]]
    #visualization_model = Model(img_input, successive_outputs)
    visualization_model = tf.keras.models.Model(inputs = model.input, outputs = successive_outputs)

    # Let's run input image through our vislauization network
    successive_feature_maps = visualization_model.predict(image)
    images_per_row = 16

    # Retrieve are the names of the layers, so can have them as part of our plot
    layer_names = [layer.name for layer in model.layers]
    for layer_name, feature_map in zip(layer_names, successive_feature_maps):
        if len(feature_map.shape) == 4:
        
            # Plot Feature maps for the conv / maxpool layers, not the fully-connected layers
            n_features = feature_map.shape[-1]  # number of features in the feature map
            size       = feature_map.shape[ 1]  # feature map shape (1, size, size, n_features)
            
            # We will tile the activation channels in this matrix
            n_cols = n_features // images_per_row
            display_grid = np.zeros((size * n_cols, images_per_row * size))

            # We'll tile each filter into this big horizontal grid
            for col in range(n_cols):
                for row in range(images_per_row):
                    x = feature_map[0,:, :,col * images_per_row + row]
                    x -= x.mean()
                    x /= x.std () + 1e-5
                    x *=  64
                    x += 128

                    x = np.clip(x, 0, 255).astype('uint8')
                    display_grid[col * size : (col + 1) * size,
                                row * size : (row + 1) * size] = x
            # Display the grid
            scale = 1. / size
            plt.figure(figsize=(scale * display_grid.shape[1],scale * display_grid.shape[0]))
            plt.title(layer_name)
            plt.axis("off")
            plt.grid(False)
            plt.imshow(display_grid, aspect='auto', cmap='viridis')
            if layer_name[:2] == "tf":
                plt.savefig(model_name + layer_name[3:],bbox_inches='tight')

            else:
                plt.savefig("./Network/UserLayers/"+ layer_name,bbox_inches='tight')
            plt.close()

