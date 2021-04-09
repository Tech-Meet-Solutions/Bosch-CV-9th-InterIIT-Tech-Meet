import json
def baseline():
	"""
	returns the hyperparameters on which the baseline model was trained 
	"""
    lr='0.001'
    decay_rate='6.67e-5'
    loss='categorical_crossentropy'
    optimizer='adam'
    return [lr,decay_rate,loss,optimizer]

def googlenet():
	"""
	returns the hyperparameters on which the googlenet model was trained 
	"""
    lr='0.001'
    decay_rate='5.71e-5'
    loss='categorical_crossentropy'
    optimizer='adam'
    return [lr,decay_rate,loss,optimizer]

def mobilenet():
	"""
	returns the hyperparameters on which the mobilenet model was trained 
	"""
    lr='0.0005'
    decay_rate='2.86e-5'
    loss='categorical_crossentropy'
    optimizer='adam'
    return [lr,decay_rate,loss,optimizer]

def resnet():
	"""
	returns the hyperparameters on which the resnet model was trained 
	"""
    lr='0.0001'
    decay_rate='5e-6'
    loss='categorical_crossentropy'
    optimizer='adam'
    return [lr,decay_rate,loss,optimizer]

if __name__ == "__main__":
    
    # reading model_name from JSON file
    f = open('data.json',)

	data = json.load(f)
  
	model_name = data['model_name']

	# Closing JSON file
	f.close()
	if model_name == 'baseline':
		baseline()
	elif model_name == 'mobilenet':
		mobilenet()
	elif model_name == 'resnet':
		resnet()
	elif model_name == 'googlenet':
		googlenet()
