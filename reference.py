import json
import logging
import sys
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
import requests
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
JSON_CONTENT_TYPE = 'application/json'
JPEG_CONTENT_TYPE = 'image/jpeg'


# inspired from https://github.com/pytorch/examples/blob/master/mnist/main.py
def Net():
    model = models.resnet18(pretrained=True, num_classes=1000) 

    for param in model.parameters():
        param.requires_grad = False # freeze the model
        nfeatures = model.fc.in_features
        #model.fc = nn.Linear(num_ftrs, 4)
    model.fc = nn.Sequential(
                   nn.Linear(nfeatures, 512),
                   nn.ReLU(inplace = True),
                   nn.Linear(512, 256), # adding own NN layers to the output of the pretrained model
                   nn.ReLU(inplace=True),
                   nn.Linear(256, 133)) # output should be 133 as we have 133 classes of dog breeds
    return model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # calling gpu



def model_fn(model_dir):
    print("In model_fn. Model directory is -")
    print(model_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Net().to(device)
    
    with open(os.path.join(model_dir, "model.pth"), "rb") as f:
        print("Loading the dog-classifier model")
        checkpoint = torch.load(f , map_location =device)
        model.load_state_dict(checkpoint)
        print('MODEL-LOADED')
        logger.info('model loaded successfully')
    model.eval()
    return model




def input_fn(request_body, content_type=JPEG_CONTENT_TYPE):
    logger.info('Deserializing the input data.')
    logger.debug(f'Request body CONTENT-TYPE is: {content_type}')
    logger.debug(f'Request body TYPE is: {type(request_body)}')
    if content_type == JPEG_CONTENT_TYPE: return Image.open(io.BytesIO(request_body))
    logger.debug('SO loded JPEG content')
    # process a URL submitted to the endpoint
    
    if content_type == JSON_CONTENT_TYPE:
        #img_request = requests.get(url)
        logger.debug(f'Request body is: {request_body}')
        request = json.loads(request_body)
        logger.debug(f'Loaded JSON object: {request}')
        url = request['url']
        img_content = requests.get(url).content
        return Image.open(io.BytesIO(img_content))
    
    raise Exception('Requested unsupported ContentType in content_type: {}'.format(content_type))

# inference
def predict_fn(input_object, model):
    
    logger.info('In predict fn')
    test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    ])
    logger.info("transforming input")
    input_object=test_transform(input_object)
    input_object = input_object.cuda() #put data into GPU
    with torch.no_grad():
        logger.info("Calling model")
        prediction = model(input_object.unsqueeze(0))
    return prediction