from data import send
from numpy.random import randint
import time
def getJSON(val1, val2):
	return '{' + '"type":' + '"' + val1 + '"'  + ',"value":' +  '"' + val2 + '"'  + '}'

items = [
			'{"type":"train_loss", "value":"10,2,3,4"}',
			'{"type":"train_acc", "value":"0.87,1,0.99,0.2"}',
			'{"type":"val_acc", "value":"1.2,1.67,0.1,-0.2"}',
			'{"type":"val_loss", "value":"-.9, 2, 11, 0"}',
		]

params = ["train_loss", "val_loss", "train_acc", "val_acc"]
l = [[], [], [], []]
for j in range(10):
	for i in range(len(l)):
		l[i].append(randint(-10,100))
		# print(getJSON(params[i], ','.join([str(x) for x in l[i]])))
		send(getJSON(params[i], ','.join([str(x) for x in l[i]])))
		send(getJSON("ETA", str(10-j)))
		send(getJSON("epoch", str(j)))
