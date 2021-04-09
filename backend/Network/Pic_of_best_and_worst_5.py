from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np
import cv2
import os
from models import *
import json
import seaborn as sns

def classes(y_test,pred):

  """

  :param y_test: true_labels
  :param pred: predicted output
              both will come after running evaluate script
  :return: index of worst and best 5 classes

  """

  report = classification_report(y_test, pred, output_dict=True)

  df = pd.DataFrame(report).transpose()

  new_df = df.drop(['accuracy','macro avg','weighted avg'])
  sort_df = new_df.sort_values('f1-score')

  label = list()
  for id in sort_df.index:
    label.append(id)

  worst_5_classes = label[0:5]
  best_5_classes = label[-5:]

  return worst_5_classes,best_5_classes

def draw_best_3_inception(network, result_number,model,classes,b):

  sns.set_theme(style="whitegrid")
  f = open('Results/pic_class.json','r')
  data = json.load(f)
  plt.axis('on')
  x = np.zeros((1,48,48,3))
  all = []
  for i in classes:
    folder_path = data[network][result_number][str(i)]
    #images = os.listdir(folder_path)
    class_imgs = []
    for j in range(5):
    
      img_folder = random.choice(list(folder_path.items()))
      img = random.choice(img_folder[1])
      img_path = img
      image = cv2.imread(img_path)
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      x[0] = image
      pred1 = model.predict(x/255)
      top_3_idx = np.argsort(pred1[0][0])[-3:]
      top_3_values = [pred1[0][0][k] for k in top_3_idx]
      top_3_labels = []
      for m in top_3_idx:
        top_3_labels.append(str(m))
      plt.xlim([0,1])
      plt.figure(figsize=(1, 1))
      #plt.barh(top_3_labels,top_3_values)
      clrs = ['grey']
      sns.barplot(x=top_3_values,y=np.arange(len(top_3_values)),orient= 'h',palette = clrs)
      count = 0
      for k in top_3_labels:
        plt.text( 0.8,count, r'{}'.format(k), fontsize=30)
        count = count + 1
      plt.savefig('./Data/best_worst/graph.png',bbox_inches='tight')
      graph = cv2.imread('./Data/best_worst/graph.png')
      final_img = np.zeros((max(image.shape[0],graph.shape[0]), image.shape[1] + graph.shape[1], 3))
      final_img[0:image.shape[0],0:image.shape[1]] = image
      final_img[:graph.shape[0],image.shape[1]:] = graph
      cv2.imwrite("./Data/best_worst/{}_{}_{}.png".format(b, i, j), final_img)
      path = "./Data/best_worst/{}_{}_{}.png".format(b, i, j)
      class_imgs.append(path)
      plt.close()
    all.append(class_imgs)

  return all,classes

def draw_best_3(network, result_number,model,classes,b):

  sns.set_theme(style="whitegrid")
  f = open('Results/pic_class.json', 'r')
  data = json.load(f)
  plt.axis('on')
  x = np.zeros((1, 48, 48, 3))
  all = []
  for i in classes:
    print()
    folder_path = data[network]['result{}'.format(result_number)][str(i)]
    # images = os.listdir(folder_path)
    class_imgs = []
    for j in range(5):
      
      img_folder = random.choice(list(folder_path.items()))
      img = random.choice(img_folder[1])
      #img_path = 'Data/Val_Data' + "/" + img
      image = cv2.imread(img)
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      x[0] = image
      pred1 = model.predict(x/255)
      top_3_idx = np.argsort(pred1[0])[-3:]
      top_3_values = [pred1[0][k] for k in top_3_idx]
      top_3_labels = []
      for m in top_3_idx:
        top_3_labels.append(str(m))
      plt.xlim([0,1])
      plt.figure(figsize=(1, 1))
      #plt.barh(top_3_labels,top_3_values)
      clrs = ['grey']
      sns.barplot(x=top_3_values,y=np.arange(len(top_3_values)),orient= 'h',palette = clrs)
      count = 0
      for k in top_3_labels:
        plt.text( 0.8,count, r'{}'.format(k), fontsize=30)
        count = count + 1
      plt.savefig('./Data/best_worst/graph.png',bbox_inches='tight')
      graph = cv2.imread('./Data/best_worst/graph.png')
      final_img = np.zeros((max(image.shape[0],graph.shape[0]), image.shape[1] + graph.shape[1], 3))
      final_img[0:image.shape[0],0:image.shape[1]] = image
      final_img[:graph.shape[0],image.shape[1]:] = graph
      cv2.imwrite("./Data/best_worst/{}_{}_{}.png".format(b, i, j), final_img)
      path = "./Data/best_worst/{}_{}_{}.png".format(b, i, j)
      class_imgs.append(path)
      plt.close()
    all.append(class_imgs)
  return all, classes

'''
#Calling
#Make sure to run the evaluate script

path = 'Test_Dataset_path'
worst,best = classes(y_test,pred)

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

if model == 'googlenet':
    draw_best_3_inception(model,path,worst,'w')
    draw_best_3_inception(model,path,best,'b')

else:
    draw_best_3(model, path, worst, 'w')
    draw_best_3(model, path, best, 'b')
'''
