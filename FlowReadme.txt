Data:
    -class_info.py
        def class_info()
            -generate json for class name, number of images in the class, paths to 5 images
    1) Upload
        -user uploads images
        -can apply transformations
    
    2) Visualise
        -generate data_viz.json
        -visualise the dataset and few images

Network:
    1)Display:
        -already generated net_mod.json
        -display the user selected network and layer wise image visualisations
           
    2) Modify:
       -take data from user, hyperameters to train the network on

    3) Train:
        -modify.py
            def start_train(model_name, train_split, smote_facto)
                -train the user chosen model, on specified hyper params
            def new_epoch(train_loss, train_accuracy, val_loss, val_accuracy, epoch)
                -saving the arrays to a dict

Results:
    evaluate.py
        -def start_eval(model_name,model,weights_path)
            -evaluate on validation dataset
    grad_lime.py
        -def give_gradcam_and_lime(paths,corr_label,model_name,result_name)
            -generate lime, grad cam results

    1) Embeddigs
        -Embedding of clustered images with predicted labels 
        -Predicted vs labels of best 5 classes and worst 5 classes
    2) Wrong results
        -Confusion matrix
        -wrong images display

    3)Suggestions
        -Display Lime, Gradcam results
        -Display explaination and suggestions why the model is failing
        
        





