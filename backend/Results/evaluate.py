import os
import numpy as np
import cv2
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from Network.models import *
import json
from Results.tsne_plots import *
from Results.Pic_of_best_and_worst_5 import *
from collections import defaultdict
from codecs import open as co_open

from json import dump as j_dump
from json import load as j_load

from os.path import dirname as os_dirname
from os.path import exists as os_exists
from os import makedirs as os_makedirs

def write_json(dict_,file_path):
    j_dump(dict_, co_open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

def wrong_pred(result_number_fr, X_val,y_val,dic,model_name,model):

    """
    :param path: Path where test data is saved
    :return: X_test and Y_test
    """
    '''
    df = pd.read_csv('class_map.csv')
    array = df.to_numpy(df)
    test = pd.read_csv(path + '/Test.csv')
    labels = test["ClassId"].values
    imgs = test["Path"].values
    total = len(imgs)
    mapping = dict()
    for i in range(array.shape[0]):
        mapping[array[i,0]] = array[i,1]
    X_test = np.zeros((total,48,48,3))
    y_test = np.zeros(total)
    count = 0
    for img in imgs:
                label = labels[count]
                dict[str(mapping[label])] = {}
                img_path = path + "/" + img
                img_array = cv2.imread(img_path)
                img_array = cv2.resize(img_array,(48,48))
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
                X_test[count] = img_array
                y_test[count] = mapping[label]
                if model_name == 'googlenet':
                    save_label_inception(img_path,model,img,dict[str(mapping[label])])
                else:
                    save_label(img_path,model,img,dict[str(mapping[label])])
                count = count + 1
    return X_test,y_test
    '''
    

    print("In Loop")
    for i in range(X_val.shape[0]):

        label = y_val[i]
        img_path = 'Data/Val_Data/Result_{}_{}.png'.format(result_number_fr,i)
        img = X_val[i]*255
        cv2.imwrite(img_path,img)
        if model_name == 'googlenet':
            print("Saving",i)
            save_label_inception(img_path, model, img, dic[str(label)])
        else:
            save_label(img_path, model, img, dic[str(label)])
            print("Saving",i)


def save_label(path,model,img,dic):

    X_test = np.expand_dims(img,axis = 0)
    pred = np.argmax(model.predict(X_test/255), axis=1)
    pred = pred[0]
    try:
        dic[str(pred)].append(path)
    except:
        dic[str(pred)] = []
        dic[str(pred)].append(path)
    print("Saving done")

def save_label_inception(path, model, img,dic):

    X_test = np.expand_dims(img, axis=0)
    pred1 = np.argmax(model.predict(X_test / 255), axis=-1)
    pred = pred1[0]
    pred[0]
    try:
        dic[str(pred)].append(path)
    except:
        dic[str(pred)] = []
        dic[str(pred)].append(path)

def test_inception(weights_path,model,X_test,y_test,json_list_embd,table_dict):

    """

    :param weights_path: Path of the Weights
    :param model: GoogleNet
    :param X_test: input from test_data
    :param y_test: input from test_data
    :return: Nil, saves .npy array whose
            column1 - precision
            column2 - recall
            column3 - f1-score
            column4 - accuracy per class
    """

    df = pd.read_csv('./Network/class_map.csv')
    df = df.to_dict()
    key_list = list(df.keys())
    val_list = list(df.values())

    model.load_weights(weights_path)
    pred1 = np.argmax(model.predict(X_test), axis=-1)
    pred = pred1[0]
    report = classification_report(y_test, pred, output_dict=True)
    df = pd.DataFrame(report).transpose()
    final_array = df.to_numpy()
    cm = confusion_matrix(y_test, pred)
    print("="*50)
    print(y_test.shape)
    print(pred.shape)
    print("="*50)
    for i in range(cm.shape[0]):
        row = []
        for j in range(cm.shape[0]):
            row.append(str(cm[i,j]))
        json_list_embd.append(row)

    # Save all wrong image
    for i in range(cm.shape[0]):
        num = cm[i, i]
        deno = np.sum(cm[i]) + np.sum(cm[:, i]) - num
        final_array[i, -1] = num / deno

    for i in range(final_array.shape[0]-3):
        row = defaultdict()
        row['class_name'] = str(key_list[val_list.index({0:i})])
        row['precision'] = final_array[i,0]
        row['recall'] = final_array[i,1]
        row['f1'] = final_array[i,2]
        row['accuracy'] = final_array[i,3]
        table_dict.append(row)

    np.save('./Results/metric.npy',cm)
    return pred


def test(weights_path,model,X_test,y_test,json_list_embd,table_dict):
    """

        :param weights_path: Path of the Weights
        :param model: MobileNet,Resnet,baseline
        :param X_test: input from test_data
        :param y_test: input from test_data
        :return: Nil, saves .npy array whose
                column1 - precision
                column2 - recall
                column3 - f1-score
                column4 - accuracy per class
    """

    df = pd.read_csv('./Network/class_map.csv')
    df = df.to_dict()
    key_list = list(df.keys())
    val_list = list(df.values())
    model.load_weights(weights_path)
    pred = np.argmax(model.predict(X_test), axis=1)
    report = classification_report(y_test, pred, output_dict=True)
    df = pd.DataFrame(report).transpose()
    final_array = df.to_numpy()
    cm = confusion_matrix(y_test, pred)
    print(cm)
    
    for i in range(cm.shape[0]):
        row = []
        for j in range(cm.shape[0]):
            row.append(str(cm[i, j]))
        json_list_embd.append(row)
    # Save all wrong image
    classes = set()
    for i in range(len(y_test)):
        classes.add(y_test[i])
    avail_classes = len(classes)
    for i in range(avail_classes):
        num = cm[i, i]
        deno = np.sum(cm[i]) + np.sum(cm[:, i]) - num
        final_array[i, -1] = num / deno


    for i in range(final_array.shape[0]-3):
        row = defaultdict()
        row['class_name'] = str(key_list[val_list.index({0:i})])
        row['precision'] = final_array[i,0]
        row['recall'] = final_array[i,1]
        row['f1'] = final_array[i,2]
        row['accuracy'] = final_array[i,3]
        table_dict.append(row)

    np.save('./Results/metric.npy',cm)
    return pred


def start_eval(model_name):

    files = os.listdir('./Network/weights/' + model_name)
    weights_path = './Network/weights/' + model_name + '/result_'  + str(len(files)) + '.hdf5'

    fr = open('./Results/res_embd.json')
    results = json.load(fr)

    pc = open('./Results/pic_class.json')
    pic = json.load(pc)

    mod = open('./Network/net_mod.json')
    module = json.load(mod)

    table = open('./Results/final_table.json')
    tab = json.load(table)

    tab['table'] = list()


    f = open('./Network/net_mod.json')
    data = json.load(f)[model_name]

    count = np.load('./Data/isLess.npy')
    num_classes = len(count) - sum(count)

    regularizer_type = data['regularizer_type']
    regularizer_value = data['regularizer_value']
    dropout_prob = data['dropout_prob']


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

    print("Model Made")

    network = model_name

    model.load_weights(weights_path)

    result_number_pc = len(pic[network])
    pic[network]["result{}".format(result_number_pc)] = defaultdict(dict)

    #A fixed path where test data would be stored, need to write a correct value
    result_number_fr = len(results[network])

    result_number_fr = result_number_pc

    X_val = np.load('./Data/X_val.npy')
    y_val = np.load('./Data/y_val.npy')

    print("Data Loaded")

    wrong_pred(result_number_fr, X_val, y_val, pic[network]["result{}".format(result_number_pc)],network,model)

    write_json(pic,'./Results/pic_class.json')
    print("Images saved")
    results[network]['result{}'.format(result_number_fr)] = defaultdict(dict)
    #results[network]['result{}'.format(result_number_fr)]['net_name'] = model_name
    results[network]['result{}'.format(result_number_fr)]['embd_imgs'] = []

    for layer in layers:
       path = tsne(model_name,result_number_fr,model, X_val[0:1000], y_val[0:1000], layer)
       results[network]['result{}'.format(result_number_fr)]['embd_imgs'].append(path)

    results[network]['result{}'.format(result_number_fr)]['embd_imgs'].append('./Data/tsne_plots/legends.png')

    results[network]['result{}'.format(result_number_fr)]['best_worst'] = defaultdict(dict)

    results[network]['result{}'.format(result_number_fr)]['conf_mat'] = list()

    df = pd.read_csv('./Network/class_map.csv')
    df = df.to_dict()
    key_list = list(df.keys())
    val_list = list(df.values())
    
    print("tsne done")
    if model_name == 'googlenet':
        pred = test_inception(weights_path, model, X_val, y_val,results[network]['result{}'.format(result_number_fr)]['conf_mat'],tab['table'])
        worst, best = classes(y_val, pred)
        all,classes_ = draw_best_3_inception(network, result_number_fr,model, best, 'b')
        count = 0
        for i in all:
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}'.format(count)] = all[count]
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}_name'.format(count)] = str(key_list[val_list.index({0:int(classes_[count])})])
            count = count + 1
        all,classes_ = draw_best_3_inception(network, result_number_fr,model, worst, 'w')
        for i in all:
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}'.format(count)] = all[count-5]
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}_name'.format(count)] = str(key_list[val_list.index({0:int(classes_[count-5])})])
            count = count + 1
    else:
        pred = test(weights_path,model, X_val, y_val,results[network]['result{}'.format(result_number_fr)]['conf_mat'],tab['table'])
        worst, best = classes(y_val, pred)
        all,classes_ = draw_best_3(network, result_number_fr,model, best, 'b')
    
        count = 0
        for i in all:
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}'.format(count)] = all[count]
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}_name'.format(count)] = str(key_list[val_list.index({0:int(classes_[count])})])
            count = count + 1
        all,classes_ = draw_best_3(network, result_number_fr,model, worst, 'w')
        for i in all:
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}'.format(count)] = all[count-5]
            results[network]['result{}'.format(result_number_pc)]['best_worst']['class{}_name'.format(count)] = str(key_list[val_list.index({0:int(classes_[count-5])})])
            count = count + 1
    results[network]['result{}'.format(result_number_fr)]['conf_dim'] = pred.shape[0]

    results[network]['result{}'.format(result_number_fr)]['loss'] = module[network]['loss']
    results[network]['result{}'.format(result_number_fr)]['optimizer'] = module[network]['optimizer']
    results[network]['result{}'.format(result_number_fr)]['regularization_type'] = module[network]['regularizer_type']
    results[network]['result{}'.format(result_number_fr)]['lr'] = module[network]['lr']
    results[network]['result{}'.format(result_number_fr)]['decay_rate'] = module[network]['decay_rate']
    results[network]['result{}'.format(result_number_fr)]['regularization_value'] = module[network]['regularizer_value']
    results[network]['result{}'.format(result_number_fr)]['epochs'] = module[network]['epochs']
    write_json(results,'./Results/res_embd.json')
    write_json(tab,'./Results/final_table.json')

if __name__ == '__main__':
    start_eval('baseline')
