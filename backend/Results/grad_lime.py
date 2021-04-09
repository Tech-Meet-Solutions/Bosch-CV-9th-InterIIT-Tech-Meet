from Results.Lime import *
from Results.GradCamPlus import *
from Results.explain_acc import *
from Results.explain_loss import *
from Results.explain_confusion_matrix import *
import os

def give_gradcam_and_lime(paths,corr_label,model_name,result_name):
    #paths=["./Data/Train/0/00000_00006_00029.png"]
    files = os.listdir('./Network/weights/' + model_name)
    weight_path = './Network/weights/' + model_name + '/result_'  + str(len(files)) + '.hdf5'
    lime_path = Lime(model_name,weight_path,paths,result_name)
    grad_path = GradCP(corr_label,model_name,weight_path, paths,result_name)

    with open('./Results/res_sugg.json') as json_file:
        data = json.load(json_file)

    temp = data[model_name]

    my_dict = {}

    temp[result_name] = {}

    my_dict["Gradcam"] = grad_path
    my_dict["Lime"] = lime_path

    check_acc(result_name, train_acc = "./Network/train_accuracy.npy", val_acc = "./Network/val_accuracy.npy")
    check_loss(result_name, train_loss = "./Network/train_loss.npy", val_loss = "./Network/val_loss.npy")
    ConfMtrx(result_name)
    my_dict["suggestions"] = "./Results/" + result_name + "_sugg.txt"
    my_dict["explainations"] = "./Results/" + result_name + "_explain.txt" 

    temp[result_name] = my_dict

    with open('./Results/res_sugg.json','w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    give_gradcam_and_lime(paths=["./Data/Train/0/00000_00006_00029.png"],corr_label=0,model_name='baseline',result_name='result_1')
