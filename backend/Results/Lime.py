import numpy as np
import keras
import skimage.io 
import skimage.segmentation
import copy
import sklearn
import sklearn.metrics
from sklearn.linear_model import LinearRegression
import tensorflow as tf
from tensorflow import keras
import cv2
from PIL import Image
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import imageio

from Network.models import *


def perturb_image(img,perturbation,segments):
    active_pixels = np.where(perturbation == 1)[0]
    mask = np.zeros(segments.shape)
    for active in active_pixels:
        mask[segments == active] = 1 
    perturbed_image = copy.deepcopy(img)
    perturbed_image = perturbed_image*mask[:,:,np.newaxis]
    return perturbed_image


def Lime(model_name,weight_path, paths,result_name):
    '''
    Return lime results on image passed
            Parameters:
                model_name: name of model user passes
                result: str
                weight_path: weights to use
                image_path: path of the image
    '''

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

    lime_result_path = []
    i = 0
    for image_path in paths:

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_fromarray = Image.fromarray(image, 'RGB')
        image = image_fromarray.resize((IMG_HEIGHT , IMG_WIDTH))
        image = np.array(image)/255

        #Generating super pixels
        superpixels = skimage.segmentation.quickshift(image, kernel_size=2,max_dist=20, ratio=0.5)
        num_superpixels = np.unique(superpixels).shape[0]

        #Create Random Perturbations
        num_perturb = 500
        perturbations = np.random.binomial(1, 0.5, size=(num_perturb, num_superpixels))

        predictions = []
        for pert in perturbations:
            perturbed_img = perturb_image(image,pert,superpixels)
            pred = model.predict(perturbed_img[np.newaxis,:,:,:])
            predictions.append(pred)

        #Predicted classes of new generated images
        predictions = np.array(predictions)
        original_image = np.ones(num_superpixels)[np.newaxis,:] #Perturbation with all superpixels enabled 
        distances = sklearn.metrics.pairwise_distances(perturbations,original_image, metric='cosine').ravel()

        kernel_width = 0.25
        weights = np.sqrt(np.exp(-(distances**2)/kernel_width**2)) #Kernel function

        #Get the top class
        preds = np.argmax(model.predict(np.expand_dims(image,axis = 0)), axis=-1)
        class_to_explain = preds[0]
        simpler_model = LinearRegression()
        simpler_model.fit(X=perturbations, y=predictions[:,:,class_to_explain], sample_weight=weights)
        coeff = simpler_model.coef_[0]

        num_top_features = 3
        top_features = np.argsort(coeff)[-num_top_features:]

        mask = np.zeros(num_superpixels) 
        mask[top_features]= True #Activate top superpixels 

        final = (perturb_image(image,mask,superpixels)*255)
        final = final.astype(np.uint8)

        lime_result_path.append('./Results/LimeResults/' + result_name + "_"+str(i)+'.png')
        imageio.imwrite(lime_result_path[-1], final)
        i += 1

    return lime_result_path

    
