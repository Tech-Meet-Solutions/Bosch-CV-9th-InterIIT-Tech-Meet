import numpy as np

def ConfMtrx(result_name,filepath = "./Results/metric.npy"):
    '''
    Returns the explaination for confusion matrix if any

        Parameters: 
            filepath: path to .npy file containing, precision, recall, f1 score and support
    '''
    f=open("./Results/" + result_name+"_sugg.txt","a+")
    g = open("./Results/" + result_name+"_explain.txt","a+")
    arr = np.load(filepath)
    num_images = np.load('./Data/num_images.npy')
    dont_take = np.load('./Data/isLess.npy')
    total_images = np.sum(num_images)
    precision = arr[:,0]
    recall = arr[:,1]
    
    flag = False
    skew_arr = ""
    for i in range(len(dont_take)):

        if (precision[i]<0.75 or recall[i]<0.75):
            if(checkskew(num_images[i],total_images)):
                flag = True
                skew_arr+=str(i)+', '
    if flag:
        f.write("Try adding more images to these ("+ skew_arr +") class(es) or oversample it using SMOTE\n")
        g.write("The class: " + skew_arr +"seems skewed\n")
    if not flag:
        g.write("The precision and recall of the model are good.")
    f.close()
    g.close

def checkskew(num_image,total):

    '''
        Returns if the class i is skewed or not
    '''
    expected = 100/48
    actual = (num_image/total)*100
    threshold = 0.85

    if((actual/expected) < 0.85):
        return True

    return False

