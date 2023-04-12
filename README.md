# CS6910_Assignment2

## Part A:
### To run the code:
- **Usage** 
```
cs6910_dl_2_partA.py
       [-h]
       [-wp WANDB_PROJECT]
       [-we WANDB_ENTITY]
       [-e EPOCHS]
       [-b BATCH_SIZE]
       [-o OPTIMIZER]
       [-lr LEARNING_RATE]
       [-a ACTIVATION]
       [-fm FILTER_MULTIPLIER]
       [-dp DROPOUT]
       [-fc DENSE_NEURONS]
       [-nf NO_FILTERS]
       [-bn BATCH_NORMALIZATION]
       [-da DATA_AUGMENTATION]
       -ks
       KERNEL_SIZE
       [KERNEL_SIZE ...]
 
```
 - To run code in cloab :
    - first Load dataset using :
     ```
     !wget 'https://storage.googleapis.com/wandb_datasets/nature_12K.zip'
     !unzip -q nature_12K.zip
     ```
     - After loading the dataset and mounting the .py file in colab run:
      ```
      !python3 "/content/drive/My Drive/Colab Notebooks/cs6910_dl_2_partA.py" -ks 3 3 3 3 3 ```
- This will run code for default parameters:
 ```config={'activation': 'LeakyRelu'
'batch_norm': false
'batch_size': 64
'data_aug':true
'dropout': 0
'fc_neurons':128
'filter_multiplier': 2
'kernel_sizes':[3,3,3,3,3]
'learning_rate': 0.0005
'num_filters':16
'optimizer': 'nadam'
 ```
 
 ## Part B:
### To run the code:
- To run code in cloab :
    - first Load dataset using :
     ```
     !wget 'https://storage.googleapis.com/wandb_datasets/nature_12K.zip'
     !unzip -q nature_12K.zip
     ```
     - After loading the dataset and mounting the .py file in colab run:
      ```
      !python3 "/content/drive/My Drive/Colab Notebooks/cs6910_dl_2_partB.py" ```
