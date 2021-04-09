import codecs, json 
from tensorflow.keras.optimizers import Adam
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import datasets, layers, models, losses, Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from models import *
import imblearn
import time
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint
from PIL import Image
import os
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import cv2
#from LayerViz import *
from data import send
from Results.evaluate import *
# from evaluate import *


def start_train(model_name, train_split, smote_factor):

    """
    arguments: 
    1.model_name
    2.train-val split ratio
    3.smote_factor = array containing smote oversampling factor of each class

    trains the model with corresponding model name and other parameters
    """
    f = open('./Network/net_mod.json',)

    data = json.loads(f.read())
    # with open('logfile','w') as f:
    #     f.write("hello")

    # print("hello")
    # lr = 0.01
    # Loss = 'categorical_crossentropy'
    # optimizer = 'Adam'
    # regularizer_type = 'L2'
    # regularizer_value = 0.0001
    # epochs = 5
    # dropout_prob = 0.5
    # layers_to_freeze = 7
    # decay_rate = 1e-6

    # train_augmentations = False #boolean variable
    # rotation_range =  10 #int eg. 10
    # zoom_range = 0.1 #int eg. 0.1
    # width_shift_range = 0.1 #int eg. 0.1
    # height_shift_range = 0.1 #int eg. 0.1
    # shear_range = 0.1 #int eg. 0.1
    data = data[model_name]
  

    lr = data['lr']
    Loss = data['loss']
    optimizer = data['optimizer']

    regularizer_type = data['regularizer_type']
    regularizer_value = data['regularizer_value']
    epochs = data['epochs']
    dropout_prob = data['dropout_prob']
    layers_to_freeze = data['layers_to_freeze']
    decay_rate = data['decay_rate']

    train_augmentations = True #boolean variable
    rotation_range = data['rotation_range'] #int eg. 10
    zoom_range = data['zoom_range'] #int eg. 0.1
    width_shift_range = data['width_shift_range'] #int eg. 0.1
    height_shift_range = data['height_shift_range'] #int eg. 0.1
    shear_range = data['shear_range'] #int eg. 0.1

    if height_shift_range is None:
        height_shift_range = 0
    if width_shift_range is None:
        width_shift_range = 0
    if rotation_range is None:
        rotation_range = 0
    if zoom_range is None:
        zoom_range = 0
    if shear_range is None:
        shear_range =0

    if lr is None:
        lr = 0.001
    if Loss is None:
        Loss = 'categorical_crossentropy'
    if optimizer is None:
        optimizer = 'Adam'
    if regularizer_type is None:
        regularizer_type = 'L2'
    if regularizer_value is None:
        regularizer_value =1e-5
    if epochs is None:
        epochs=10
    if dropout_prob is None:
        dropout_prob=0.4
    if layers_to_freeze is None:
        layers_to_freeze=0
    if decay_rate is None:
        decay_rate=1e-6

    # isLess = np.load('/isless.npy')   #isless array stores 1 for classes with less than 100 images

    # isLess = np.zeros((num_classes))

    count = 0
    directory_labels=[]
    class_labels=[]
    #reading the dataset
    image_data = []
    image_labels = []
    class_size=[]

    for i in range(len(os.listdir('./Data/Train'))):
        path = './Data/Train/' + str(i)
        images = os.listdir(path)
        if len(images) > 75 :                 
            for img in images:
                
                image = cv2.imread(path + '/' + img)
                image_fromarray = Image.fromarray(image, 'RGB')
                resize_image = image_fromarray.resize((48, 48))
                image_data.append(np.array(resize_image))
                image_labels.append(count)
            
            directory_labels.append(str(i))
            class_size.append(len(images))
            class_labels.append(count)
            count = count + 1

    class_map = {directory_labels[j]: [class_labels[j]] for j in range(len(directory_labels))} #dictionary to map directory labels to class ids
    df = pd.DataFrame(class_map) 
    df.to_csv('./Network/class_map.csv') 
    
    num_classes = count


    # Changing the list to numpy array
    image_data = np.array(image_data)
    image_labels = np.array(image_labels)

    shuffle_indexes = np.arange(image_data.shape[0])
    np.random.shuffle(shuffle_indexes)
    image_data = image_data[shuffle_indexes]
    image_labels = image_labels[shuffle_indexes]


    
    X_train, X_val, y_train, y_val = train_test_split(image_data, image_labels, test_size=int(train_split)/100, shuffle=True)

    X_train = X_train/255 
    X_val = X_val/255
    assert X_train.shape == (X_train.shape[0], 48, 48, 3)
    assert X_val.shape == (X_val.shape[0], 48, 48, 3)
    with open('./Data/X_val.npy', 'wb') as f:
        np.save(f, X_val)
    with open('./Data/y_val.npy', 'wb') as f1:
        np.save(f1, y_val)

    # Closing JSON file
    # f.close()

    train_model(model_name, lr, Loss, optimizer, regularizer_value, regularizer_type, epochs, dropout_prob, num_classes, 
        layers_to_freeze, X_train, y_train, X_val, y_val, train_augmentations, rotation_range, zoom_range, 
        width_shift_range, height_shift_range, shear_range, smote_factor, decay_rate, class_size, class_map)

    # train_model('baseline', 0.01, 'categorical_crossentropy', 'Adam', 0.1, 'L1', 20, 0.4, num_classes, 
    #     4, X_train, y_train, X_val, y_val, train_augmentations, rotation_range, zoom_range, 
    #     width_shift_range, height_shift_range, shear_range, smote_factor, decay_rate, class_size, class_map)

def getJSON(val1, val2):
    return '{' + '"type":' + '"' + val1 + '"'  + ',"value":' +  '"' + val2 + '"'  + '}'

def new_epoch(train_loss, train_accuracy, val_loss, val_accuracy, epoch):

        """
        arguments: 
        1. training loss
        2. training accuracy
        3. validation loss
        4. validation accuracy
        5. epoch number

        called after each epoch and stores the values of given arguments after each epoch 
        """
        #saving the arrays to a dict
        plot_value_dict = {
            "train_accuracy" : list(train_accuracy), 
            "train_loss" : list(train_loss),
            "val_accuracy" : list(val_accuracy), 
            "val_loss" : list(val_loss),
            "epoch": epoch
        }
        train_accuracy_string = ','.join([str(s)[0:4] for s in list(train_accuracy)])
        train_loss_string = ','.join([str(s)[0:4] for s in list(train_loss)])
        val_accuracy_string = ','.join([str(s)[0:4] for s in list(val_accuracy)])
        val_loss_string = ','.join([str(s)[0:4] for s in list(val_loss)])
        #send metrics to UI for plotting graph
        #send(getJSON('train_loss', train_loss_string))
        #send(getJSON('val_loss', val_loss))
        #send(getJSON('train_acc', train_accuracy_string))
        #send(getJSON('val_acc', val_accuracy_string))
        #send(getJSON('epoch', str(epoch)))

        #send metrics to UI for plotting graph
        with open('train_loss','w') as f:
            f.write(getJSON('train_loss', train_loss_string))
        with open('val_loss','w') as f:
            f.write(getJSON('val_loss', val_loss_string))
        with open('train_acc','w') as f:
            f.write(getJSON('train_acc', train_accuracy_string))
        with open('val_acc','w') as f:
            f.write(getJSON('val_acc', val_accuracy_string))
        with open('epoch','w') as f:
            f.write(getJSON('epoch', str(epoch)))

        # send('{"type":"train_loss", "value" : train_loss_string}')
        # send('{"type":"val_loss", "value" : val_loss_string}')
        # send('{"type":"train_acc", "value": train_accuracy_string}')
        # send('{"type":"val_acc", "value":val_accuracy_string}')
        # send('{"type":"epoch", "value":str(epoch)}')


        file_path = "./Network/plot_values.json" 
        json.dump(plot_value_dict, codecs.open(file_path, 'w', encoding='utf-8'))  #saving the arrays in json format
        with open('./Network/train_accuracy.npy', 'wb') as f:
            np.save(f, train_accuracy)

        with open('./Network/train_loss.npy', 'wb') as f:
            np.save(f, train_loss)

        with open('./Network/val_accuracy.npy', 'wb') as f:
            np.save(f, val_accuracy)

        with open('./Network/val_loss.npy', 'wb') as f:
            np.save(f, val_loss)



acc_array = []
val_acc_array = []
loss_array = []
val_loss_array = []

#custom callback class, saves plot and stores metrics at end of each epoch
class CustomCallback1(keras.callbacks.Callback):
    
    """
    custom callback class
    """
    def on_epoch_end(self, epoch, logs=None):
        
        """
        called after each epoch and logs the value of training loss, training accuracy, validation loss, validation accuracy
    
        """
        global acc_array, val_acc_array, loss_array, val_loss_array
        acc_array.append(logs["accuracy"])
        val_acc_array.append(logs["val_accuracy"])  
        loss_array.append(logs["loss"])
        val_loss_array.append(logs["val_loss"])  

        new_epoch(loss_array, acc_array, val_loss_array, val_acc_array, epoch)

class googlenet_CustomCallback1(keras.callbacks.Callback):
    
    """
    custom callback class for googlenet model
    """

    def on_epoch_end(self, epoch, logs=None):
        """
        called after each epoch of googlenet model and logs the value of training loss, training accuracy, validation loss, validation accuracy
    
        """
        with open('callback.txt','a') as f:
          f.write("epoch no. {} ".format(epoch))
          f.write("loss {} ".format(logs["loss"]))
          f.write("accuracy {} ".format(logs["dense_4_accuracy"]))
          f.write("validation loss {} ".format(logs["val_dense_4_loss"]))
          f.write("validation accuracy {}\n".format(logs["val_dense_4_accuracy"]))
          f.close()
        global acc_array, val_acc_array, loss_array, val_loss_array
        acc_array.append(logs["dense_4_accuracy"])
        val_acc_array.append(logs["val_dense_4_accuracy"])  
        loss_array.append(logs["loss"])
        val_loss_array.append(logs["val_dense_4_loss"])  

        new_epoch(loss_array, acc_array, val_loss_array, val_acc_array, epoch)


def train_model(model_name, lr, Loss, optimizer, regularizer_value, regularizer_type, epochs, dropout_prob, num_classes, 
        layers_to_freeze, X_train, y_train, X_val, y_val, train_augmentations, rotation_range, zoom_range, 
        width_shift_range, height_shift_range, shear_range, smote_factor, decay_rate, class_size, class_map):
    """
    trains the model with given hyperparameters
    """
    global acc_array, val_acc_array, loss_array, val_loss_array
    acc_array = []
    val_acc_array = []
    loss_array = []
    val_loss_array = []

    if model_name == 'baseline':
        model = create_baseline(num_classes, dropout_prob, regularizer_type, regularizer_value)
        eta = str(epochs*22/60)

    elif model_name == 'mobilenet':
        model = create_mobilenet(num_classes, dropout_prob)
        eta = str(epochs*28/60)

    elif model_name == 'resnet':
        model = create_resnet(num_classes, dropout_prob)
        eta = str(epochs*95/60)

    elif model_name == 'googlenet':
        model = create_googlenet(num_classes, dropout_prob)
        eta = str(epochs*92/60)

    #send(getJSON('ETA', str(eta)))
    #saving eta to json file
    with open('ETA','w') as fh:
        with open('Logfile','w') as f:
            f.write('hello'+eta)
        fh.write(getJSON('ETA', str(eta)[0:4]))

    #eta_dict = {'eta': eta}
    #f_path = "./Network/eta_dict.json" 
    #json.dump(eta_dict, codecs.open(f_path, 'w', encoding='utf-8'))


    for layer in model.layers[0:layers_to_freeze]:
        layer.trainable = False


    #defining optimizer
    if optimizer == 'Adam':
        optim = keras.optimizers.Adam(lr=lr, decay= decay_rate, name='Adam')
    if optimizer == 'Adagrad':
        optim = keras.optimizers.Adagrad(learning_rate= lr, decay=decay_rate, name='Adagrad')
    if optimizer == 'RMSprop':
        optim = keras.optimizers.RMSprop(learning_rate= lr, decay=decay_rate, name='RMSprop')
    if optimizer == 'SGD':
        optim = keras.optimizers.SGD(learning_rate= lr , decay=decay_rate, name='SGD')
    

    #loss function options: categorical_crossentropy, kullback_leibler_divergence


    #compiling the model
    if model_name == 'googlenet':
        model.compile(optimizer=optim, loss=[Loss, Loss, Loss], loss_weights=[1, 0.3, 0.3], metrics=['accuracy'])
    else:
        model.compile(loss=Loss, optimizer=optim, metrics=['accuracy'])



    #SMOTE suggestions:
    with open('smote_explanation.txt','w') as f:
        f.write('SMOTE is a statistical technique used for increasing the number of samples of the minority classes in a balanced way to counter class imbalace problem\n') 
        f.write('This approach generates new examples that combine features of the target case with features of its neighbors and makes the samples more general\n')
        f.write('The minority classes in our dataset are: 0, 6, 14, 15, 16, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47\n')
        f.write('if the Oversampling factor for a class is x the no. of samples in that class will be scaled to x times the no. of samples in the majority class\n')
        f.write('The Auto_SMOTE option will set the oversampling factor as 0.6 for all the minority classes ')
        f.close()

    

    if smote_factor == None:
        oversampling_factor = 0.6
        oversampling_num = oversampling_factor * 1595
        minor_class_array = [0, 6, 14, 15, 16, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40, 41, 42]
        oversample_array=[]
        for i in range(len(minor_class_array)):
            oversample_array.append(int(oversampling_num))
        strategy = dict(zip(minor_class_array, oversample_array)) # dictionary with keys as class index and values equal to no. of samples

    else:
        class_array=[]
        oversample_array=[]
        for j in range(num_classes):
            if smote_factor[j]!=0:
                class_array.append(class_map[str(j)][0])
                num = smote_factor[j]*1595
                if num > class_size[class_map[str(j)][0]]:
                    oversample_array.append(int(num))
                else:
                    oversample_array.append(int(class_size[class_map[str(j)][0]]))

        strategy = dict(zip(class_array, oversample_array ))

    X_dataForSmote = X_train.reshape(X_train.shape[0], 48 * 48 * 3)

    # applying smote

    y = LabelEncoder().fit_transform(y_train)  #shape of y_train = (total no. of train images, None)
    oversample = SMOTE(sampling_strategy=strategy)
    X_oversampled, y = oversample.fit_resample(X_dataForSmote, y)
    X_train = X_oversampled.reshape(X_oversampled.shape[0], 48, 48, 3)
    y_train = y
    y_train = keras.utils.to_categorical(y_train, num_classes) #converting to one hot labels
    y_val = keras.utils.to_categorical(y_val, num_classes)

    

    #storing weights of each model
    if model_name == 'baseline':
        model_1 = create_baseline(48, dropout_prob, regularizer_type, regularizer_value)
        model_1.load_weights('./Network/weights/baseline/result_1.hdf5')      #result_1.hdf - weights of the model trained on 48 classes

        if layers_to_freeze >= len(model_1.layers):
            layers_to_freeze = len(model_1.layers)-1
        for i in range(layers_to_freeze):
            model.layers[i].set_weights(model_1.layers[i].get_weights()) 

        for layer in model.layers[0:layers_to_freeze]:
            layer.trainable = False


        w = len(os.listdir('./Network/weights/baseline/')) + 1
        filepath = './Network/weights/baseline/result_'+str(w)+'.hdf5'

    elif model_name == 'mobilenet':
        model_1 = create_mobilenet(48, dropout_prob)
        model_1.load_weights('./Network/weights/mobilenet/result_1.hdf5')

        if layers_to_freeze >= len(model_1.layers):
            layers_to_freeze = len(model_1.layers)-1
        for i in range(layers_to_freeze):
            model.layers[i].set_weights(model_1.layers[i].get_weights()) 

        for layer in model.layers[0:layers_to_freeze]:
            layer.trainable = False


        w = len(os.listdir('./Network/weights/mobilenet/')) + 1
        filepath = './Network/weights/mobilenet/result_'+str(w)+'.hdf5'

    elif model_name == 'resnet':
        model_1 = create_resnet(48, dropout_prob)
        model_1.load_weights('./Network/weights/resnet/result_1.hdf5')

        if layers_to_freeze >= len(model_1.layers):
            layers_to_freeze = len(model_1.layers)-1
        for i in range(layers_to_freeze):
            model.layers[i].set_weights(model_1.layers[i].get_weights()) 

        for layer in model.layers[0:layers_to_freeze]:
            layer.trainable = False

        w = len(os.listdir('./Network/weights/resnet/')) + 1
        filepath = './Network/weights/resnet/result_'+str(w)+'.hdf5'

    elif model_name == 'googlenet':
        model_1 = create_googlenet(48, dropout_prob)
        model_1.load_weights('./Network/weights/googlenet/result_1.hdf5')

        if layers_to_freeze  >= len(model_1.layers):
            layers_to_freeze = len(model_1.layers) - 1
            
        for i in range(layers_to_freeze):
            model.layers[i].set_weights(model_1.layers[i].get_weights()) 

        for layer in model.layers[0:layers_to_freeze]:
            layer.trainable = False

        w = len(os.listdir('./Network/weights/googlenet/')) + 1
        filepath = './Network/weights/googlenet/result_'+str(w)+'.hdf5'

    checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    googlenet_checkpoint = ModelCheckpoint(filepath, monitor='val_dense_4_accuracy', verbose=1, save_best_only=True, mode='max')
    if train_augmentations == True:
        aug = ImageDataGenerator(
                rotation_range = rotation_range,
                zoom_range = zoom_range,
                width_shift_range = width_shift_range,
                height_shift_range = height_shift_range,
                shear_range = shear_range,
                fill_mode="nearest")

        if model_name == 'googlenet':
            history = model.fit(aug.flow(X_train, y_train), batch_size=32, epochs=epochs, validation_data=(X_val, [y_val, y_val, y_val]), callbacks = [googlenet_CustomCallback1(), googlenet_checkpoint])
        else:
            history = model.fit(aug.flow(X_train, y_train), batch_size=32, epochs=epochs, validation_data=(X_val, y_val), callbacks = [CustomCallback1(), checkpoint])
    else:
        if model_name == 'googlenet':
            history = model.fit(X_train, [y_train, y_train, y_train], batch_size=32, epochs=epochs, validation_data=(X_val, [y_val, y_val, y_val]), callbacks = [googlenet_CustomCallback1(), googlenet_checkpoint])
        else:

            history = model.fit(X_train, y_train, batch_size=32, epochs=epochs, validation_data=(X_val, y_val), callbacks = [CustomCallback1(), checkpoint])

    start_eval(model_name)
    #send('{"type": "end", "value" : "anything"}')
    with open('end','w') as fh:
        fh.write('{"type": "end", "value" : "anything"}')
    # LayerVisualise(model_name,image_path = "../Data/Train/00000_00006_00029.png")
    # start_eval(model_name,model,filepath)
    time.sleep(10)
    open('val_loss','w').close()
    open('train_loss','w').close()
    open('val_acc','w').close()
    open('train_acc','w').close()
    open('epoch','w').close()
    open('ETA','w').close()
    open('end','w').close()

    
if __name__ == "__main__":
    # reading hyperparams from JSON file
    # print('hi')
    start_train(model_name, train_split, smote_factor)
    # smote_f = [0 for i in range(48)]
    # start_train('baseline', 0.2, smote_f)
