import os
import numpy as np
import random
import cv2
from sklearn.model_selection import train_test_split
import pandas as pd

def create_data(path):

  """
  :param path: The folder where data is stored
  :return: X_train and y_train, which will act as input to t-SNE function
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
      dir_path = path + '/' + str(dir)
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

#A fixed path where train data would be stored
#Need to write according to website

path = '/content/dataset/Train'
X_train,y_train = create_data(path)