# pip install --upgrade tf-keras-vis 

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import tensorflow as tf
from tensorflow import keras
from tf_keras_vis.utils import normalize
from tf_keras_vis.gradcam import Gradcam
from tf_keras_vis.gradcam import GradcamPlusPlus
import cv2
from PIL import Image
import re
import pathlib
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

from Network.models import *

def GradCP(corr_label,model_name,weight_path, paths,result_name):

    '''
        Return grad cam ++ results on image passed
            Parameters:
                model_name: name of model user passes
                corr_label: class of the image
                weight_path: weights to use
                image_path: path of all images in txt file
                result: str
                
    '''

    def loss(output):
        #return score of label class as loss
        return (output[0][corr_label])

    def model_modifier(m):
        m.layers[-1].activation = tf.keras.activations.linear
        return m

    f = open('./Network/net_mod.json')
    data = json.load(f)

    count = np.load('./Data/isLess.npy')
    num_classes = len(count) - sum(count)

    regularizer_type = data[model_name]['regularizer_type']
    regularizer_value = data[model_name]['regularizer_value']
    dropout_prob = data[model_name]['dropout_prob']

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
    i = 0
    grad_result_path = []
    for image_path in paths:
   
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_fromarray = Image.fromarray(image, 'RGB')
        image = image_fromarray.resize((IMG_HEIGHT , IMG_WIDTH))
        image = np.array(image)/255
        image = np.expand_dims(image, axis=0)

        # Create GradCAM++ object
        gradcam = GradcamPlusPlus(model,model_modifier,clone=False)

        # Generate heatmap with GradCAM++
        cam = gradcam(loss,
                    image,
                    penultimate_layer=-1, # model.layers number
                    )

        cam = normalize(cam)
        # f, ax = plt.subplots(**subplot_args)
        # for i, title in enumerate(image_titles):
        heatmap = np.uint8(cm.jet(cam[0])[..., :3] * 255)
        plt.axis("off")
        plt.grid(None)
        plt.imshow(image[0])
        plt.imshow(heatmap, cmap='jet', alpha=0.4)

        grad_result_path.append('./Results/GradCamResults/' + result_name + "_"+str(i)+'.png')
        plt.savefig(grad_result_path[-1],bbox_inches='tight')
        plt.close()

        i += 1

    return grad_result_path





