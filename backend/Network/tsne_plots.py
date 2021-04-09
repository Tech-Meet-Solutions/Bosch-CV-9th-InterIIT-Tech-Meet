"""
Input - model - (Can be a list from which user will choose one) Choose between Small, Resnet, GoogleNet and mobilenet
        X_train - An array of images of size (n,48,48,3) where n is number of images
        y_train - An array of labels of size (n) currently in network
        layer_number - The number of layer whose t-SNE output is to be visualized
                        For Resnet it is 0 - 177 (10,43,76,109,150)

Output - t-SNE plot would be saved at the path desired (path_to_save)

How to run - Call the function tsne with input as model,X_train,y_train,layer_number
"""
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import tensorflow as tf
import seaborn as sns
import numpy as np
import os
import random
from sklearn.model_selection import train_test_split
import cv2
import pandas as pd
#from models import *
import matplotlib
matplotlib.use('Agg')
#The height and width of the t-SNE plot
width = 11.7
height = 8.27
sns.set(rc={'figure.figsize':(width,height)})

#Obtain intermediate outputs
def visualize_conv_layer(model,layer_name, x_train):

    layer_output = model.get_layer(layer_name).output
    intermediate_model = tf.keras.models.Model(inputs=model.input, outputs=layer_output)

    return intermediate_model.predict(x_train).reshape(x_train.shape[0], -1)

#Name the layers so that they can be called
def naming(model,no_of_lyrs):

    for i in range(no_of_lyrs):
        model.layers[i]._name = 'layer' + '_' + str(i)

#t-SNE plot will be saved
#Please give correct path where the image would be stored to the varaible - path_to_save

def tsne(model_name,result_number,model,X_train,y_train,layer_number):

    """
    t-SNE plot will be saved
    Please give correct path where the image would be stored to the variable - path_to_save
    """

    count = 0
    classes = set()
    for i in range(len(y_train)):
        classes.add(y_train[i])
    avail_classes = len(classes)

    no_of_lyrs = len(model.layers)

    naming(model,no_of_lyrs)

    layer_name = 'layer' + '_' + str(layer_number)

    model_output = visualize_conv_layer(model,layer_name,X_train)

    palette = sns.color_palette("husl", avail_classes)
    tsne = TSNE(n_components=2)
    X_embedded = tsne.fit_transform(model_output)
    plt.ioff()
    sns.scatterplot(X_embedded[:,0], X_embedded[:,1], hue=y_train,palette=palette,legend=False)
    path_to_save = './Results/tsne_plots/{}_{}_{}.png'.format(model_name,result_number,layer_number)
    count = count + 1
    print(count)
    plt.savefig(path_to_save)
    plt.close()
    return path_to_save

def create_data(path):

  """
  :param path: The folder where data is stored
  :return: X_train and y_train, which will act as input to t-SNE function

  An assumption is made that the folder name is same as label
  """

  df = pd.read_csv('class_map.csv')
  array = df.to_numpy(df)
  mapping = dict()
  for i in range(array.shape[0]):
      mapping[array[i, 0]] = array[i, 1]
  classes = len(os.listdir(path))
  X_train = np.zeros((classes*20,48,48,3))
  y_train = np.zeros((classes*20))
  count = 0
  for _,dirs,_ in os.walk(path):
    dirs.sort()
    for dir in dirs:
      dir_path = path + '/'+ str(dir)
      all = os.listdir(dir_path)
      for i in range(20):
        img = random.choice(all)
        img_path = dir_path + "/" + img
        img_array = cv2.imread(img_path)
        img_array = cv2.resize(img_array,(48,48))
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        X_train[count] = img_array
        label = int(dir)
        y_train[count] = mapping[label]
        count = count + 1
  X_train, _, y_train, _ = train_test_split(X_train, y_train, test_size=0.0000000001,random_state=42, shuffle=True)

  return X_train,y_train

'''
path = '/content/dataset/Train'
X_train,y_train = create_data(path)

f = open('data.json')
data = json.load(f)
model_name = data['model_name']

if model_name == 'baseline':
    layers = ['0', '3', '6', '9', '11']
    model = create_baseline(num_classes, dropout_prob, regularizer_type, regularizer_value)
elif model_name == 'mobilenet':
    layers = ['10', '27', '43', '69', '88']
    model = create_mobilenet(num_classes, dropout_prob)
elif model_name == 'resnet':
    layers = ['10', '43', '76', '109', '150']
    model = create_resnet(num_classes, dropout_prob)
elif model_name == 'googlenet':
    layers = ['10', '28', '45', '72', '90']
    model = create_googlenet(num_classes, dropout_prob)

weight_path = data['weight_path']
model.load_weights(weight_path)

for layer in layers:
    tsne(model_name,result_number,model, X_train, y_train, layer)

final_image = np.zeros((200,1000,3))

for i in range(5):
    path = 'tsne_plots' + '/' + str(i)
    img = cv2.imread(path)
    img = cv2.resize(img, (200,200))
    final_image[:,i*200:(i+1)*200] = img

cv2.imwrite("all_layers_tsne.png",final_image)

f = open('layer_tsne.txt', 'w')
f.write("all_layers_tsne.png")
'''
