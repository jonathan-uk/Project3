# Project(III) - Image Classification Using AWS Sagemaker
This is a full project of imageclassification using a resnet18 pretrained model with sagemaker as Udacity's ML Nanodegree Project. The project was completed by making good use of the tools available to a machine learning engineer. the tools used are the Pytorch framework, a pretrained model, debgger, together with the model to train and deploy and endpoint. 

The Python script used as entry points include:
hpo.py script was used for hperparameter tuning after which the best sets of hypermaters were used in training

train_model.py script was used to perform model profiling and debugging. The function required for debugging was stated

reference.py script used as entry point for model deployment makes it possible for data(image) to be passed to the endpoint for testing

## Dataset
We use the provided Dog Breed Dataset to use as data for the training jobs

## Project pipeline
The notebook environment is prepared by installing all the required dependencies, the dataset is downloaded, unziped and loaded to S3 Training

## Hyperparamter tuning
For this project, I used ResNet18 model. Among other pre-trained models, ResNet(18) model is popularly used and it is suitable for the system i am using. It provides a fair balance between the model accuracy to the number of operations needed to excecute. Though ResNet18 model might tend to have a lower accuracy, It is comparably faster to train with than ResNet 34 completed training job. i also used epoch 50.
![pytorch](https://user-images.githubusercontent.com/86266982/153577404-22796787-a4af-452f-8fc9-f6b635f1852c.JPG)

Log metrics of the training process
![logs](https://user-images.githubusercontent.com/86266982/153577696-a98071cd-f792-43ee-9971-4f53c4d1b4a2.JPG)

The two parameters tuned where the batch size and learning rate
![hyper tuning](https://user-images.githubusercontent.com/86266982/153577863-b081a384-fac5-4df8-9b62-4a3847110cf5.JPG)

## Debugging and Profiling
The Debugger Hook was set to record the Loss Criterion of the process in both training and validation/testing. 

## Result
![train](https://user-images.githubusercontent.com/86266982/153578222-601c9b5c-b60e-4924-aafe-d1197aa311b0.JPG)

## Model Deployment
![end pointtt](https://user-images.githubusercontent.com/86266982/153578794-1acc5e41-f81c-4280-9d32-85f5335e76ef.JPG)

After successfully carrying out the training job with the best hyperparameter available, I called for deployment with pytorch_model.deploy(). I also run a prediction on the endpoint.


