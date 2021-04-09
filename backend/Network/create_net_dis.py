import json
from models import *
import os

def baseline(path = ""):
    """
    returns info of each layer of the baseline model with layer image path
    """
    model = create_baseline(48, 0.5, None, None)
    layer_name=[]
    files = os.listdir(path)

    for layer in model.layers:
        check = path + "/" + layer.name + ".png"
        if check in [path+'/'+f for f in files]:
            if 'conv' in layer.name and (not 'bn' in layer.name) and (not 'pad' in layer.name) and (not 'relu' in layer.name):
                layer_name.append([check,[layer.name ,str(layer.kernel_size[0]) + ' x ' + str(layer.kernel_size[1]), '-']])
            else:
                layer_name.append([check,[layer.name,'-', '-']])
    return layer_name

def googlenet(path = ""):
    """
    returns info of each layer of the googlenet model with layer image path
    """
    lr='0.001'
    model = create_googlenet(48, 0.5)
    files = os.listdir(path)
    layer_name=[]
    for layer in model.layers:
        check = path + "/" + layer.name + ".png"
        if check in [path+'/'+f for f in files]:
            if 'conv' in layer.name and (not 'bn' in layer.name) and (not 'pad' in layer.name) and (not 'relu' in layer.name):
                layer_name.append([check,[layer.name ,str(layer.kernel_size[0]) + ' x ' + str(layer.kernel_size[1]), '-']])
            elif layer.name[:2] != "tf":
                layer_name.append([check,[layer.name,'-', '-']])

        elif layer.name[:2] == "tf":
            layer_name.append([path+"/"+layer.name[3:]+".png",[layer.name, '-', '-']])
    return layer_name

def mobilenet(path = ""):
    """
    returns info of each layer of the mobilenet model with layer image path
    """
    lr='0.0005'
    model = create_mobilenet(48, 0.5)
    layer_name=[]
    files = os.listdir(path)
    for layer in model.layers:
        check = path + "/" + layer.name + ".png"
        if check in [path+'/'+f for f in files]:
            if 'conv' in layer.name and (not 'bn' in layer.name) and (not 'pad' in layer.name) and (not 'relu' in layer.name):
                layer_name.append([check,[layer.name ,str(layer.kernel_size[0]) + ' x ' + str(layer.kernel_size[1]), '-']])
            else:
                layer_name.append([check,[layer.name,'-', '-']])
    return layer_name


def resnet(path = ""):
    """
    returns info of each layer of the resnet model with layer image path
    """
    lr='0.0001'
    model = create_resnet(48, 0.5)
    layer_name=[]
    files = os.listdir(path)
    for layer in model.layers:
        check = path + "/" + layer.name + ".png"
        if check in [path+'/'+f for f in files]:
            if 'conv' in layer.name and (not 'bn' in layer.name) and (not 'out' in layer.name) and (not 'add' in layer.name) and (not 'pad' in layer.name) and (not 'relu' in layer.name):
                layer_name.append([check,[layer.name ,str(layer.kernel_size[0]) + ' x ' + str(layer.kernel_size[1]), '-']])
            else:
                layer_name.append([check,[layer.name,'-', '-']])
    return layer_name


if __name__ == "__main__":
    
    



    net_dis = {
        'baseline' : {
                    'net_img': './Network/net_images/baseline.png', 
                    'learning_rate': '0.001', 
                    'decay_rate':  '6.67e-5', 
                    'optimizer': 'adam',
                    'loss': 'categorical_crossentropy',
                    'layers': baseline('./Network/LayerImages/baseline48')
                    } ,
        'mobilenet' : {
                    'net_img': './Network/net_images/mobilenet.png',
                    'learning_rate': '0.0005', 
                    'decay_rate':  '2.86e-5', 
                    'optimizer': 'adam',
                    'loss': 'categorical_crossentropy',
                    'layers': mobilenet('./Network/LayerImages/mobilenet48')
                    } ,
        'googlenet' : {
                    'net_img': './Network/net_images/googlenet.png',
                    'learning_rate': '0.001', 
                    'decay_rate':  '5.71e-5', 
                    'optimizer': 'adam',
                    'loss': 'categorical_crossentropy',
                    'layers': googlenet('./Network/LayerImages/googlenet48')
                    } ,
        'resnet' : {
                    'net_img': './Network/net_images/resnet.png',
                    'learning_rate': '0.0001', 
                    'decay_rate':  '5e-6', 
                    'optimizer': 'adam',
                    'loss': 'categorical_crossentropy',
                    'layers': resnet('./Network/LayerImages/resnet48')
                    } 
        }

    with open('./Network/net_dis.json', 'w') as json_file:
        json.dump(net_dis, json_file)
