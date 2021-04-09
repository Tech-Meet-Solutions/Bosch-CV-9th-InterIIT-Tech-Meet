import os
import numpy as np
import random
import json

def class_info(dataset_path = "./Data/Train"):
    '''
    Returns 
        npy file for:
        1. Num of images in each folder
        2. Boolean array, entry is one if no. of images in the class is less than 100

        json file:
        {   num_classes: integer
            classes: [{class_name: string, pics:[‘path1’, ‘path2’, ‘path3’, ‘path4’, ‘path5’], num_imgs: integer}, [{class_name: string, pics:[‘path1’, ‘path2’, ‘path3’, ‘path4’, ‘path5’], num_imgs: integer}], ….}

    '''

    data = {}
    with open('./Data/class_dict.json', 'r') as fp:
        class_map = json.load(fp)

    folders = os.listdir(dataset_path)
    num_classes = len(folders)
    
    num_images = []
    isLess = []
    store = []
    final = {}
    for folder in folders:
        paths = []
        temp = {}  #inside dictionaries

        temp["class_name"] = class_map[folder]
        files = os.listdir(dataset_path + '/' + folder)
        num_images.append(len(files))

        if(num_images[-1]<75):
            isLess.append(1)
    
        else:
            isLess.append(0)

        indices = random.sample(range(0,num_images[-1]),min(5,num_images[-1]))
        for i in indices:
            paths.append('./Data/Train/'+ folder+'/'+files[i])

        temp["pics"] = paths
        temp["num_imgs"] = num_images[-1]

        store.append(temp)
    
    final["num_calsses"] = num_classes
    final["classes"] = store

    num_images = np.asarray(num_images)
    isLess = np.asarray(isLess)
    np.save("./Data/num_images.npy",num_images)
    np.save("./Data/isLess.npy",isLess)
    with open('./Data/data_viz.json', 'w') as fp:
        json.dump(final, fp)

        
if __name__ == '__main__':
    class_info()