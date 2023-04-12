# -*- coding: utf-8 -*-
"""Dl2_B.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a4qam-j-eC3IW1JxBXgz7cRn2FeyOnUQ
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
torch.manual_seed(1) 
np.random.seed(1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Dataset Augmentation 
def load_data(bs):
    # define the transforms to be applied to the training data
    transform = transforms.Compose(
    [transforms.Resize(256),
     transforms.CenterCrop(224),
     transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    home_path = "/content/inaturalist_12K"

    train_path = os.path.join(home_path,'train')
    test_path = os.path.join(home_path,'val')
    # define the dataset and apply the transforms
    train_dataset = ImageFolder(train_path, transform=transform)
    test_dataset = ImageFolder(test_path, transform=transform)

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

train_loader,val_loader,test_loader,classes=load_data(4)

# Load the pre-trained ResNet-50 model
PATH = './resnet50_finetuned.pth'

model = torchvision.models.resnet50(pretrained=True)

# Freeze all the layers except the last fully connected layer
for param in model.parameters():
    param.requires_grad = False

# Modify the last fully connected layer to have 10 output nodes
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 10)
model.to(device=device)

# Define the loss function and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)

# Train the modified model for a few epochs
for epoch in range(5):  # loop over the dataset multiple times

    running_loss = 0.0
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

        running_loss += loss.item()
        if batch_idx % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, batch_idx + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')

model.load_state_dict(torch.load(PATH))
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
loss,acc=calculate_accuracy(model,test_loader,nn.CrossEntropyLoss())
print(loss,acc)