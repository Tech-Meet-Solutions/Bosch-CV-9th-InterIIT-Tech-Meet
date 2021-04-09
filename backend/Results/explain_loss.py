import numpy as np



def check_loss(result_name,train_loss,val_loss):

    '''
        Returns explanations for loss plot if the model overfits
    '''
    f = open("./Results/" + result_name+"_sugg.txt","a+")
    g = open("./Results/" + result_name+"_explain.txt","a+")
    tloss = np.load(train_loss)
    vloss = np.load(val_loss)
    
    a = vloss - tloss
    length = len(vloss)//2

    flag = 0

    res = all(j>i for i, j in zip(a[length:], a[length+1:])) and (vloss[-1] > 1.05*tloss[length])


    if(res):
        flag = 1
        g.write("The model is having poor generalisation on the validation dataset that is having variance and hence in this context it is overfitting.\n")
        f.write("Measures to reduce overfitting and improve its performance are as follows:\n")
        f.write("If you can change the network then try using weight regularisation and/or dropouts to reduce the variance of the model thereby reducing its complexity.\n")
        f.write("If you can't change the network, but only the dataset, try applying augmentations to artificially increase the size of the dataset or use SMOTE. This would decrease the generalisation error by adding diversity to the dataset.\n")

    if not flag:
        g.write("The validaiton and training losses are improving with epochs\n")
    g.close()
    f.close()
    return

