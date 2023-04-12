# -*- coding: utf-8 -*-
"""cs6910-dl-2 (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14gnedyX5vX0HIJQly_LX7n_b--CwaX4A
"""

import torch
import torch.nn as nn
print(torch.device('cuda:0'))
print(torch.__version__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)


# imports
import math
import torch
import torchvision
import torch.nn.functional as F  # Parameterless functions, like (some) activation functions
import torchvision.datasets as datasets  # Standard datasets
import torchvision.transforms as transforms  # Transformations we can perform on our dataset for augmentation
from torch import optim  # For optimizers like SGD, Adam, etc.
from torch import nn  # All neural network modules
from torch.utils.data import (
    DataLoader, random_split
)  # Gives easier dataset managment by creating mini batches etc.
from tqdm import tqdm  # For nice progress bar!

from torchvision.datasets import ImageFolder
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import argparse
torch.manual_seed(1) 
np.random.seed(1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Dataset Augmentation 
def load_data(bs,augment_data=False):
    # define the transforms to be applied to the training data
    if augment_data:
        train_transforms = transforms.Compose([
          transforms.Resize((300,300)),
          transforms.RandomHorizontalFlip(),
          transforms.RandomRotation(10),
          transforms.ToTensor(),
          transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
      ])
    else:
        train_transforms = transforms.Compose([
          transforms.Resize((300,300)),
          transforms.ToTensor(),
          transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
      ])
    
    test_transforms = transforms.Compose([
      transforms.Resize((300,300)),
      transforms.ToTensor(),
      transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
  ])


    home_path = "/content/inaturalist_12K"

    train_path = os.path.join(home_path,'train')
    test_path = os.path.join(home_path,'val')
    # define the dataset and apply the transforms
    train_dataset = ImageFolder(train_path, transform=train_transforms)
    test_dataset = ImageFolder(test_path, transform=test_transforms)

    # split training dataset into train and validation sets
    train_size = int(0.8 * len(train_dataset))
    print(train_size)
    val_size = len(train_dataset) - train_size
    print(val_size)

    train_dataset, val_dataset = random_split(train_dataset, [train_size, val_size])

    # create a data loader for the training data
    train_loader = torch.utils.data.DataLoader(train_dataset,bs, shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, bs, shuffle=False)
    test_loader = torch.utils.data.DataLoader(test_dataset, bs, shuffle=False)

    #categories
    root=pathlib.Path(train_path)

    classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])

    return train_loader,val_loader,test_loader,classes

#Simple CNN
def flatten(k=[11,9,7,5,3],w=300, s=1, p=1):
    r=w
    for i in  range(len(k)):
        print("r",r)
        r= (r+2*p-k[i])+1
        r= int(r/2)+1
    return r 


class CNN(nn.Module):
    def __init__(self, in_channels=3, num_class=10,num_filters=4,kernel_sizes=[11,9,7,5,3],fc_neurons=64,batch_norm=True,dropout=0.3,filter_multiplier=2,activation='LeakyRelu'):

        super(CNN, self).__init__()
        self.in_channels=in_channels
        self.num_class=num_class
        self.num_filters=num_filters
        self.kernel_sizes=kernel_sizes
        self.fc_neurons=fc_neurons
        self.activation=activation
        self.batch_norm=batch_norm
        self.dropout=dropout
        self.filter_multiplier=filter_multiplier
        
        #print("in1")
        self.conv1 = nn.Conv2d(3, num_filters, kernel_size=kernel_sizes[0],stride=1, padding=1).to(device)
        #print("in2")
        self.bn1=nn.BatchNorm2d(num_features=num_filters)
        self.relu1 = nn.LeakyReLU()

        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.conv2 = nn.Conv2d(num_filters,filter_multiplier*num_filters,  kernel_size=kernel_sizes[1],stride=1, padding=1).to(device)
        self.bn2=nn.BatchNorm2d(num_features=filter_multiplier*num_filters)
        self.relu2 = nn.LeakyReLU()

        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.conv3 = nn.Conv2d(filter_multiplier*num_filters, int(math.pow(filter_multiplier, 2))*num_filters, kernel_size=kernel_sizes[2],stride=1, padding=1).to(device)
        self.bn3=nn.BatchNorm2d(num_features=int(math.pow(filter_multiplier, 2))*num_filters)
        self.relu3 = nn.LeakyReLU()


        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.conv4 = nn.Conv2d(int(math.pow(filter_multiplier, 2))*num_filters, int(math.pow(filter_multiplier, 3))*num_filters, kernel_size=kernel_sizes[3],stride=1, padding=1).to(device)
        self.bn4=nn.BatchNorm2d(num_features=int(math.pow(filter_multiplier, 3))*num_filters)
        self.relu4 = nn.LeakyReLU()

        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.conv5 = nn.Conv2d(int(math.pow(filter_multiplier, 3))*num_filters, int(math.pow(filter_multiplier, 4))*num_filters, kernel_size=kernel_sizes[4],stride=1, padding=1).to(device)
        self.bn5=nn.BatchNorm2d(num_features=int(math.pow(filter_multiplier, 4))*num_filters)
        self.relu5 = nn.LeakyReLU()


        self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)
        print("ok pool5")
        self.r=flatten(kernel_sizes)
        print("ok flatten")
        print(self.r)
        self.fc1 = nn.Linear(in_features=int(math.pow(filter_multiplier, 4))*num_filters*self.r*self.r, out_features=fc_neurons)
        self.relu6 = nn.LeakyReLU()

        self.drop = nn.Dropout(dropout)
        
        self.fc2 = nn.Linear(in_features=fc_neurons, out_features=num_class)
      
    
    def forward(self, x):
        x = self.conv1(x)
        if self.batch_norm:
            x = self.bn1(x)
        x = self.relu1(x)
        
        x = self.pool1(x)
        
        x = self.conv2(x)
        if self.batch_norm:
            x = self.bn2(x)
        x = self.relu2(x)

        x = self.pool2(x)

        x = self.conv3(x)
        if self.batch_norm:
            x = self.bn3(x)
        x = self.relu3(x)
        
        x = self.pool3(x)
        
        x = self.conv4(x)
        if self.batch_norm:
            x = self.bn4(x)
        x = self.relu4(x)
       
        x = self.pool4(x)
     
        x = self.conv5(x)
        if self.batch_norm:
            x = self.bn5(x)
        x = self.relu5(x)

        x = self.pool5(x)
        x = x.view(x.size(0),-1)

        x = self.fc1(x)
        x = self.relu6(x)
        x = self.drop(x)
        
        x = self.fc2(x)
        
        return x


parser = argparse.ArgumentParser()
parser.add_argument('-wp' , '--wandb_project', help='Project name used to track experiments in Weights & Biases dashboard' , type=str, default='CS6910_Assignment_2__Q2')
parser.add_argument('-we', '--wandb_entity' , help='Wandb Entity used to track experiments in the Weights & Biases dashboard.' , type=str, default='cs22s015')
parser.add_argument('-e', '--epochs', help="Number of epochs to train neural network.", type=int, default=15)
parser.add_argument('-b', '--batch_size', help="Batch size used to train neural network.", type=int, default=64)
parser.add_argument('-o', '--optimizer', help = 'choices: ["sgd", "adam", "nadam"]', type=str, default = 'nadam')
parser.add_argument('-lr', '--learning_rate', help = 'Learning rate used to optimize model parameters', type=float, default=0.0005)
parser.add_argument('-a', '--activation', help='choices: ["LeakyRelu","Gelu","Selu","Relu"]', type=str, default="LeakyRelu")
parser.add_argument('-fm', '--filter_multiplier', help='choices:[0.5,2,1]',type=float, default=2)
parser.add_argument('-dp', '--dropout', help='choices:[0,0.2,0.3]',type=float, default=0)
parser.add_argument('-fc', '--dense_neurons', help='Number of neurons in dense layer ',type=int, default=128)
parser.add_argument('-nf', '--no_filters', help='Number of filters in each layer',type=int, default=16)
parser.add_argument('-bn', '--batch_normalization', help='Choices:["True","False"]',type=bool, default=False)
parser.add_argument('-da', '--data_augmentation', help='Choices:["True","False"]',type=bool, default=True)
parser.add_argument('-ks','--kernel_size', nargs='+', help='list containing size of kernel', type=int,default=[3,3,3,3,3],required=True)


args = parser.parse_args()


# if __name__=='__main__':

def opti(model,opt='adam',lr=0.0005):
    print("in opti")
    if opt == "sgd":
        opt= optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    elif opt == "adam":
        opt = optim.Adam(model.parameters(),lr=lr,weight_decay=0.0001)
    elif opt == "nadam":
        opt = optim.NAdam(model.parameters(),lr=lr,weight_decay=0.0001)
    print('exit opti')    
    return opt


# Hyperparameters
in_channels = 3
num_class = 10
learning_rate = args.learning_rate
batch_size = args.batch_size
epochs = args.epochs
data_aug=args.data_augmentation

# Load data
train_loader,val_loader,test_loader,classes=load_data(batch_size,data_aug)
#print(classes)
trainfeature, trainlabel = next(iter(train_loader))
print(f"Feature Batch Shape: {trainfeature.size()}")
print(f"Label Batch Shape: {trainlabel.size()}")



# Initialize network
model = CNN(3,10,args.no_filters,args.kernel_size,args.dense_neurons,args.batch_normalization,args.dropout,args.filter_multiplier,args.activation).to(device)
# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer=optimizer=opti(model,args.optimizer,learning_rate)
# Train Network
for epoch in range(epochs):
    # Set the model to training mode
    model.train()

    for batch_idx, (data, targets) in enumerate(train_loader):
        # Get data to cuda if possible
        data = data.to(device=device)
        targets = targets.to(device=device)
        
        optimizer.zero_grad()
        # forward
        scores = model(data)
        loss = criterion(scores, targets)

        # backward
        
        loss.backward()

        # gradient descent or adam step
        optimizer.step()
        
    # Set the model to evaluation mode
    model.eval()

    # Track the total loss and number of correct predictions
    val_loss = 0
    num_correct = 0
    num_samples = 0

    # Evaluate the model on the validation set
    with torch.no_grad():
        for data, targets in val_loader:
            data = data.to(device=device)
            targets = targets.to(device=device)

            scores = model(data)
            val_loss += criterion(scores, targets).item()

            _, predictions = scores.max(1)
            num_correct += (predictions == targets).sum()
            num_samples += predictions.size(0)

    # Calculate the average validation loss and accuracy
    val_loss /= len(val_loader)
    val_acc = float(num_correct) / num_samples

    # Print the epoch number, loss, and accuracy
    print('Epoch [{}/{}], Train Loss: {:.4f}, val Loss: {:.4f}, val Acc: {:.2f}%'
          .format(epoch+1, epochs, loss.item(), val_loss, val_acc*100))

# Check accuracy on training & test to see how good our model
# Save best model
best_model_path = 'best_model.pth'
torch.save(model.state_dict(), best_model_path)
print(f"Best model saved to {best_model_path}")



'''# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters
in_channels = 3
num_class = 10
learning_rate = 0.0001
batch_size = 32
epochs = 15
data_aug=False

# Load data
train_loader,val_loader,test_loader,classes=load_data(batch_size,data_aug)
print(classes)
trainfeature, trainlabel = next(iter(train_loader))
print(f"Feature Batch Shape: {trainfeature.size()}")
print(f"Label Batch Shape: {trainlabel.size()}")



# Initialize network
model = CNN(3,10,16,[7,5,5,3,3],64,True,0.2,2,'Mish').to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer=optim.NAdam(model.parameters(),lr=learning_rate,weight_decay=0.0001)

# Train Network
for epoch in range(epochs):
    # Set the model to training mode
    model.train()

    for batch_idx, (data, targets) in enumerate(train_loader):
        # Get data to cuda if possible
        data = data.to(device=device)
        targets = targets.to(device=device)
        
        optimizer.zero_grad()
        # forward
        scores = model(data)
        loss = criterion(scores, targets)

        # backward
        
        loss.backward()

        # gradient descent or adam step
        optimizer.step()
        
    # Set the model to evaluation mode
    model.eval()

    # Track the total loss and number of correct predictions
    test_loss = 0
    num_correct = 0
    num_samples = 0

    # Evaluate the model on the validation set
    with torch.no_grad():
        for data, targets in test_loader:
            data = data.to(device=device)
            targets = targets.to(device=device)

            scores = model(data)
            test_loss += criterion(scores, targets).item()

            _, predictions = scores.max(1)
            num_correct += (predictions == targets).sum()
            num_samples += predictions.size(0)

    # Calculate the average validation loss and accuracy
    test_loss /= len(test_loader)
    test_acc = float(num_correct) / num_samples

    # Print the epoch number, loss, and accuracy
    print('Epoch [{}/{}], Train Loss: {:.4f}, Test Loss: {:.4f}, Test Acc: {:.2f}%'
          .format(epoch+1, epochs, loss.item(), test_loss, test_acc*100))

# Check accuracy on training & test to see how good our model
# Save best model
best_model_path = 'best_model.pth'
torch.save(model.state_dict(), best_model_path)
print(f"Best model saved to {best_model_path}")

best_model_path = 'best_model.pth'

loaded_model = CNN(3,10,16,[7,5,5,3,3],64,True,0.2,2,'Mish').to(device)
loaded_model.load_state_dict(torch.load(best_model_path)) # it takes the loaded dictionary, not the path file itself

def calculate_accuracy(model, test_loader,criterion):
    model.eval()
    total = 0
    correct = 0
    cost=0
    acc=0
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            cost +=criterion(outputs,labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            del images
            del labels
    acc=100 * correct / total
    cost/=len(test_loader)
        
    return cost,acc
loss,acc=calculate_accuracy(loaded_model,test_loader,nn.CrossEntropyLoss())
print(loss,acc)

print(loaded_model.state_dict())

best_model_path = 'best_model.pth'

loaded_model = CNN(3,10,16,[7,5,5,3,3],64,True,0.2,2,'Mish')
loaded_model.load_state_dict(torch.load(best_model_path)) # it takes the loaded dictionary, not the path file itself
'''
'''# Initialize wandb
wandb.init(project="CS6910_Assignment_2_Q2")


# Define a function to generate predictions and sample images from the test data
def generate_predictions(model, data_loader):
    # Set the model to evaluation mode
    model.eval()
    
    # Create a list to store the predictions and sample images
    predictions = []
    sample_images = []
    
    # Generate predictions and sample images
    with torch.no_grad():
        for batch, _ in data_loader:
            # Forward pass through the model
            output = model(batch)
            
            # Get the predicted class labels
            _, predicted = torch.max(output, 1)
            
            # Convert the predicted labels to image tensors
            predicted_images = torchvision.utils.make_grid(batch[predicted])
            
            # Append the predictions and sample images to the lists
            predictions.append(predicted_images)
            sample_images.append(torchvision.utils.make_grid(batch))
    
    # Concatenate the predictions and sample images into grids
    prediction_grid = torchvision.utils.make_grid(predictions, nrow=3)
    sample_grid = torchvision.utils.make_grid(sample_images, nrow=3)
    
    # Return the grids
    return prediction_grid, sample_grid

# Generate the prediction and sample image grids
prediction_grid, sample_grid = generate_predictions(loaded_model, test_loader)

# Log the grids to wandb
wandb.log({
    'Predictions': wandb.Image(prediction_grid),
    'Sample Images': wandb.Image(sample_grid)
})

# Finish the run
wandb.finish()

from signal import signal,SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
!pip install wandb -qU
import wandb
!wandb login --relogin da816d14625ef44d200ee4acaa517646962e6f9a

sweep_config = {
    "name" : "CS6910_Assignment_2_Q2",
    "method" : "bayes",
    'metric': {
        'name': 'val_acc',
        'goal': 'maximize'
    },
    "parameters" : {
        "optimizer" : {
            "values" : ['adam','nadam','sgd']
        },
        "activation" : {
            "values" : ['LeakyRelu','Selu','Gelu','Mish']
        },
        "batch_size": {
            "values": [32, 64, 128]
        },
        'learning_rate':{
            "values": [0.001,0.0001,0.0003,0.0005]
        },
        "dropout": {
            "values": [0,0.2,0.3]
        },
        "batch_norm": {
              "values": [True,False]
        },
        "data_aug": {
              "values": [True,False]
        },
        'kernel_sizes':{
            'values': [[3,3,3,3,3],[5,5,5,5,5],[7,5,5,3,3], [11,9,7,5,3]]
        },
        'filter_multiplier': {
            'values': [1, 2, 0.5]
        },
        'num_filters': {
            'values': [4,8,16]
        },
        "fc_neurons": {
              "values": [32, 64, 128]
          }        
    }
}
def opti(model,opt='adam',lr=0.0005):
    print("in opti")
    if opt == "sgd":
        opt= optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    elif opt == "adam":
        opt = optim.Adam(model.parameters(),lr=lr,weight_decay=0.0001)
    elif opt == "nadam":
        opt = optim.NAdam(model.parameters(),lr=lr,weight_decay=0.0001)
    print('exit opti')    
    return opt

def calculate_accuracy(model, test_loader,criterion):
    model.eval()
    total = 0
    correct = 0
    cost=0
    acc=0
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            cost +=criterion(outputs,labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            del images
            del labels
    acc=100 * correct / total
    cost/=len(test_loader)
        
    return cost,acc
def train():
    config_default={
      'epochs':15,
      'batch_size':32,
      'learning_rate':0.001,
      'dropout':0.3,
      'batch_norm':True,
      'data_aug':True,
      'kernel_sizes':[5,5,5,5,5],
      'filter_multiplier': 2,
      'num_filters': 16,
      "fc_neurons": 64
  }
    wandb.init(config=config_default)
    c= wandb.config
    name = "nfliter_"+str(c.num_filters)+"op_"+str(c.optimizer)+"_ac_"+str(c.activation)+"_n_"+str(c.learning_rate)+"_bs_"+str(c.batch_size)+"_dp_"+str(c.dropout)+"_bn_"+str(c.batch_norm)

    wandb.init(name=name)

    # Retrieve the hyperparameters from the config
    lr = c.learning_rate
    bs = c.batch_size
    epochs = 15
    act= c.activation
    opt= c.optimizer

    dp = c.dropout
    bn = c.batch_norm
    da=c.data_aug
    ks=c.kernel_sizes
    fm=c.filter_multiplier
    nf=c.num_filters
    fc=c.fc_neurons


    # Load the dataset
    train_loader,val_loader,test_loader,classes=load_data(bs,da)
    
    print("data loaded ====================================================")

    # Initialize network
    model= CNN(in_channels=3, num_class=10,num_filters=nf,kernel_sizes=ks,fc_neurons=fc,batch_norm=bn,dropout=dp,filter_multiplier=fm,activation=act).to(device)
    print("model ini==============================================================")
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer=opti(model,opt,lr)
    print("done")
    # Train Network
    for epoch in range(epochs):
        print('epoch enter')
        # Set the model to training mode
        model.train()

        for batch_idx, (data, targets) in enumerate(train_loader):
            # Get data to cuda if possible
            data = data.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()
            # forward
            scores = model(data)
            loss = criterion(scores, targets)

            # backward

            loss.backward()

            # gradient descent or adam step
            optimizer.step()  
            del data
            del targets
            
        # Calculate the test accuracy
        train_loss,train_acc = calculate_accuracy(model, train_loader,criterion)
        val_loss,val_acc = calculate_accuracy(model, val_loader,criterion)
        test_loss,test_acc = calculate_accuracy(model, test_loader,criterion)

        torch.cuda.empty_cache()
        # Log the metrics to WandB
        wandb.log({'epoch': epoch+1,'loss':loss.item(), 'train_loss': loss.item(),'test_loss':test_loss,'val_loss':val_loss,'test_acc': test_acc,'train_acc': train_acc,'val_acc': val_acc})


    # Save the best model
    wandb.save('model.h5')
    return

# Initialize the WandB sweep
sweep_id = wandb.sweep(sweep_config, project='CS6910_Assignment_2_Q2')
wandb.agent(sweep_id, function=train,count=5)
'''