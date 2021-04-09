from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from .models import *
from .serializers import FileSerializer
import numpy as np
import cv2
from base64 import b64decode,b64encode
from .transforms2 import *
import os
import json
from PIL import Image
from io import BytesIO
from background_task import background
from Data.class_info import class_info
from Network.modify import start_train as StartTrain
from Results.grad_lime import give_gradcam_and_lime as GiveGradLime
from data import send


def from_base64(base64_data):
    nparr = np.fromstring(b64decode(base64_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

def to_base64(image_data,type):
  if "png" in type:
    retval, buffer_img = cv2.imencode('.png', image_data)
  elif "jpeg" in type:
    retval, buffer_img = cv2.imencode('.jpeg', image_data)
  return b64encode(buffer_img)

class FileUploadViewSet(viewsets.ModelViewSet):
  queryset = File.objects.all()
  serializer_class = FileSerializer

  def create(self, request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      ext = serializer.data["b64"].split(",")[0].split('/')[-1].split(';')[0]
      img = serializer.data["b64"].split(",")[1]
      class_dict_path = os.path.join(settings.BASE_DIR, "Data", "class_dict.json")
      class_to_num = {}
      with open(class_dict_path) as fh:
        temp = json.load(fh)
        for i in temp:
          class_to_num[temp[i]] = i
      path = os.path.join(settings.BASE_DIR,"Data", "Train", class_to_num[serializer.data['image_class']])
      if not os.path.isdir(path):
        os.mkdir(path)
      im = Image.open(BytesIO(b64decode(img)))
      im.save(f"{path}/{serializer.data['id']}.{ext}", ext.capitalize())
      return Response("Hello")



class TransformView(APIView):

  def post(self, request):
    data = request.data
    print(data)
    transforms = data["transforms"]
    ids = data["ids"]
    imgs = {
      "images" : []
    }
    for id in ids:
      image = File.objects.get(pk=id)
      arr = from_base64(image.b64.split(",")[1])
      arr = applyTransforms(arr, transforms)
      b64 = to_base64(arr,image.b64.split(",")[0])
      imgs["images"].append({
        "id" : id,
        "b64" :image.b64.split(",")[0] + "," + b64.decode("utf-8"),
        "labels" : " ".join([image.labels] + [a for a in transforms.keys() if transforms[a] != 0]),
        "image_class" : image.image_class
      })
    return Response(imgs)
  
@api_view(['GET'])
def pipeline(request, filename = None):
  if filename == None:
    return Response({"error": "Invalid Filename"}, status = 404)
  
  file_path = os.path.join(settings.FILES_DIR, filename)
  with open(file_path, "rb") as file:
    encoded_string = b64encode(file.read())
  type = filename.split(",")[-1]
  print(type)

  return Response({"data": f"data:image/{type};base64, {encoded_string.decode()}"})
  

@api_view(['GET','POST'])
def labels(request):
  if request.method == "GET":
    file_path = os.path.join(settings.BASE_DIR, "Data", 'class_dict.json')
    with open(file_path, "r") as f:
      try:
        labels = json.load(f)
        labels = [labels[k] for k in labels]
      except:
        labels = []
    return Response({"data":labels})
  
  elif request.method == "POST":
    data = request.data['label']
    file_path = os.path.join(settings.BASE_DIR, "Data", 'class_dict.json')
    with open(file_path, "r") as f:
      labels = json.load(f)
      labels[str(len(labels))] = data
    with open(file_path, "w") as f:
      json.dump(labels, f)
    class_info()
    return Response({"data":[labels[k] for k in labels]})

class NetworkView(APIView):

  def get(self, request):
    file_path = os.path.join(settings.BASE_DIR,'Network','net_mod.json')
  
    with open(file_path,'r') as f:
      try: 
        data = json.loads(f.read())
      except:
        data = {}
    
    return Response(data[request.query_params.get('network')])
  
  def post(self,request):
    file_path = os.path.join(settings.BASE_DIR,'Network','net_mod.json')
    print(request.data)
    with open(file_path,'r') as f:
      try: 
        data = json.loads(f.read())
      except:
        data = {}
    
    with open(file_path,'w') as f:
      try:
        for key in request.data['data']:
          data[request.data['network']][key] = request.data['data'][key]
      except:
        data[request.data['network']] = {}
        for key in request.data['data']:
          data[request.data['network']][key] = request.data['data'][key] 
      f.write(json.dumps(data))
    
    return Response({"msg" : "Success"})
  
@api_view(['GET','POST'])
def train(request):
  if request.method == "GET":
    print(request.query_params)
    with open(f"pipeline/{request.query_params['filename']}",'r') as fh:
      l = fh.read()
    l = json.loads(l)
    print(l)
    return Response({"data":l})
  
  elif request.method == "POST":
    with open(f"pipeline/{request.data['filename']}",'w') as fh:
      fh.write(request.data['value'])
    return Response({"message":"success"})

def get_file_data(file_path):
  with open(file_path, "rb") as file:
    encoded_string = b64encode(file.read())
  type = file_path.split(".")[-1]
  return f"data:image/{type};base64,{encoded_string.decode()}"

@api_view(['GET'])
def data_viz(request):
  Class = request.query_params.get('class')
  num = int(request.query_params.get('num'))
  if Class == "__all__":
    class_info()
  file_path = os.path.join(settings.BASE_DIR,'Data','data_viz.json')
  with open(file_path,'r') as f:
    data = json.loads(f.read())
  #print(data["classes"][0])
  try:
    del data["num_classes"]
  except:
      pass
  #print(data)
  print(Class)
  if Class == '__all__':
    for obj in data["classes"]:
      length = len(obj["pics"])
      obj["pics"] = [get_file_data(img) for img in obj["pics"][0:min(num,length)]]
    print(len(data["classes"]),data["classes"][0])
    return Response(data)
  else:
    dataToSend = {"classes":[]} 
    for obj in data["classes"]:
      if obj["class_name"] == Class:
        obj["pics"] = [get_file_data(img) for img in obj["pics"]]
        dataToSend["classes"].append(obj)
        return Response(dataToSend)
    return Response({})  
  

@api_view(['GET'])
def net_dis(request):
  network = request.query_params.get("network")
  file_path = os.path.join(settings.BASE_DIR,'Network','net_dis.json')
  with open(file_path,'r') as f:
    data = json.loads(f.read())
  data[network]["net_img"] = get_file_data(data[network]["net_img"])
  for layer in data[network]["layers"]:
    layer[0] = get_file_data(layer[0])
  return Response(data[network])


@api_view(['GET'])
def net_mod(request):
  file_path = os.path.join(settings.BASE_DIR,'network','net_mod.json')
  with open(file_path,'r') as f:
    data = json.loads(f.read())
  for i in data:
    if i in request.GET:
      data[i] = request.GET[i]
  with open(file_path,'w') as f:
    json.dump(data, f)
  return Response("Success")


@api_view(['GET'])
def start_training(request):
  data = request.GET
  if str(data["autogen"]) == "1":
    smote_factor = None
  else:
    smote_factor =  list(json.loads(data["smote_factor"]).values())
  #print(data["smote_factor"],type(json.loads(data["smote_factor"])))
  start_train(model_name=data["model_name"], train_split=data["train_split"], smote_factor= smote_factor, schedule=1)
  return Response("Done")


@api_view(['GET'])
def start_evaluation(request):
  data = request.GET
  start_eval(model_name=data["model_name"], schedule=1)
  return Response("Done")


@api_view(['GET'])
def get_eval_results(request):
  file_path = os.path.join(settings.BASE_DIR,'Results','res_embd.json')
  with open(file_path,'r') as f:
    data = json.loads(f.read())
  print(request.GET)
  response = data[request.GET["model_name"]].keys()
  return Response(response)

@api_view(['GET'])
def get_eval(request):
  file_path = os.path.join(settings.BASE_DIR,'Results','res_embd.json')
  with open(file_path,'r') as f:
    data = json.loads(f.read())
  response = data[request.GET["net_name"]][request.GET["result_name"]]
  response["embd_imgs"] = [get_file_data(f) for f in response["embd_imgs"]]
  # response["best_worst"] = {row: [get_file_data(f) for f in response["best_worst"][row]] if len(row) < 8 for row in response["best_worst"]}
  for row in response["best_worst"]:
    if len(row) < 8:
      response["best_worst"][row] = [get_file_data(f) for f in response["best_worst"][row]]
  return Response(response)

###################### Wrong Results###################################
@api_view(["GET"])
def getConfMatWithLabels(request):
  network, result = request.query_params.get('network'), request.query_params.get('result')
  conf_path = os.path.join(settings.BASE_DIR,'Results','res_embd.json')
  labels_path = os.path.join(settings.BASE_DIR,'Data','class_dict.json')

  data = {}
  print(network,result)
  with open(labels_path,'r') as f:
    data["labels"] = json.loads(f.read())
  
  with open(conf_path,'r') as f:
    data["conf"] = json.loads(f.read())[network][result]["conf_mat"]
  
  return Response(data)
    

@api_view(['GET'])
def get_wrong_results(request):
  file_path = os.path.join(settings.BASE_DIR,'Results','pic_class.json')
  labels_path = os.path.join(settings.BASE_DIR,'Data','class_dict.json')
  with open(labels_path,'r') as f:
    labels = json.loads(f.read())
    labels = {v: k for k, v in labels.items()}

  with open(file_path,'r') as f:
    data = json.loads(f.read())
  try:
    imgs = data[request.GET["net_name"]][request.GET["result_name"]][labels[request.GET["corr_class"]]][labels[request.GET["pred_class"]]]
  except:
    imgs = data[request.GET["net_name"]][request.GET["result_name"]][labels[request.GET["corr_class"]]]['['+labels[request.GET["pred_class"]]+']']
  response = {
    "imgs": [get_file_data(f) for f in imgs],
    "paths": imgs,
    }
  return Response(response)

@api_view(['GET'])
def start_gradcam_lime(request):
  data = request.query_params
  # delete existing suggestions
  labels_path = os.path.join(settings.BASE_DIR,'Data','class_dict.json')
  with open(labels_path,'r') as f:
    labels = json.loads(f.read())
    labels = {v: k for k, v in labels.items()}
  print(data["paths"])
  Paths = ["./"+path for  path in data.getlist('paths')]
  print(Paths)
  GiveGradLime(
    paths=Paths,
    corr_label=int(labels[data["corr_label"]]),
    model_name=data["model_name"],
    result_name=data["result_name"],
  )
  return Response("Done")

####################################################################
@api_view(['GET'])
def get_suggestions(request):
  file_path = os.path.join(settings.BASE_DIR,'Results','res_sugg.json')
  file_path2 = os.path.join(settings.BASE_DIR,'Results','final_table.json')
  with open(file_path,'r') as f:
    data = json.loads(f.read())
  with open(file_path2,'r') as f:
    data2 = json.loads(f.read())
  response = data[request.GET["net_name"]][request.GET["result_name"]]
  response["gradcam"] = [get_file_data(f) for f in response["Gradcam"]]
  response["lime"] = [get_file_data(f) for f in response["Lime"]]
  response["final_table"] = data2["table"]
  sug_file = response["suggestions"]
  with open(sug_file,'r') as f:
    response["suggestions"] = f.read()
  exp_file = response["explainations"]
  with open(exp_file,'r') as f:
    response["explainations"] = f.read()
  return Response(response)



# CV functions
@background(schedule=1)
def start_train(model_name="", train_split=0, smote_factor=[]):
  print('Hello')
  StartTrain(model_name,train_split,smote_factor)


@background(schedule=1)
def start_eval(model_name=""):
  import time
  time.sleep(10)
  print("Sleep over")
  # Call front end with data for new evaluation with embeddings data

@background(schedule=1)
def give_gradcam_and_lime(paths=[""], corr_label=0, model_name="", result_name=""):
  GiveGradLime(paths,corr_label,model_name,result_name)
  # Call front end with data and also save it in json file

# Polling
@api_view(['GET'])
def get_train_data(request):
  file = request.GET['type']
  with open(file, 'r') as fh:
    resp = fh.read()
  return Response(resp.strip())