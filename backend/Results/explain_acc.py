import numpy as np


def check_acc(result_name, train_acc,val_acc):

    '''
        Returns explanations for accuracy plot if the model underfits
    '''
    f = open("./Results/" + result_name+"_sugg.txt","w")
    g = open("./Results/" + result_name+"_explain.txt","w")
    tacc = np.load(train_acc)
    vacc = np.load(val_acc)
    
    length = 3*(len(val_acc)//4)

    res = all(i<0.90 for i in tacc[length:])

    if(res):
        g.write("The model is performing poorly on the training dataset that is having bias and hence in this context it is underfitting.\n")

        f.write("Suggestive measures to reduce underfitting and improve its performance are as follows:\n")
        f.write("If you can change the network then try adding more layers to increase its depth, number of features and complexity.\n")
        f.write("If you can't change the network, but only the dataset, try applying suitable transforms to remove noise from the images, train for a larger number of epochs and perform hyperparamter tuning such as reducing the learning rate, reducing the number of layers freezed.\n")

    f.close()
    g.close()
    return


