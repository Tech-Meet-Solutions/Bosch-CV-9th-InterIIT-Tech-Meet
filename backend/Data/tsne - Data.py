"""
Input - X_train - An array of images of size (n,48,48,3) where n is number of images
        y_train - An array of labels of size (n) currently in network
        layer_number - (Can be a list which will depend upon model selected) The number of layer whose t-SNE output is
                        to be visualized form starting,like 0,1,2... Can't take reverse inputs like -1,-2,etc

                        For GoogleNet it is 0 - 95 (10,28,45,72,90)
                        For Resnet it is 0 - 177 (10,43,76,109,150)
                        For mobilenet it is 0 - 92 (10,27,43,69,88)
                        For small it is 0 - 12 (0,3,6,9,12)

Output - t-SNE plot would be saved at the path desired (path_to_save)

How to run - Call the function tsne with input as X_train,y_train
"""
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import tensorflow as tf
import seaborn as sns
import numpy as np
from data_creation_for_tsne import X_train,y_train

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

def tsne(X_train,y_train):

        """
        t-SNE plot will be saved
        Please give correct path where the image would be stored to the variable - path_to_save
        """

        f = open("plots.txt",'w')
        classes = set()
        for i in range(len(y_train)):
            classes.add(y_train[i])
        avail_classes = len(classes)

        palette = sns.color_palette("husl", avail_classes)
        tsne = TSNE(n_components=2)
        X_embedded = tsne.fit_transform(X_train.reshape(X_train.shape[0], -1))
        plt.ioff()
        sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1], hue=y_train, palette=palette, legend=False)
        path_to_save = 'tsne_plots/tsne-data.png'
        f.write(path_to_save)
        plt.savefig(path_to_save)