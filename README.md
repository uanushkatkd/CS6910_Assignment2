# CS6910_Assignment2

## Question 1: a)
- Filter size is $k$ x $k$ and there are $m$ filters per convolutional layer.
Each filter has ($d$× $k$ <sup>2</sup>)−1 computations per convolution where d represents depth of input to the convolutional layer.
- For MaxPooling I'm taking kernel size $2$ x $2$ with stride 2.
- Input size is $300$ x $300$ with in_channels or depth $d$ =3.
-  **Conv1 layer Computation** : ($m$ x (3 ×  $k$ <sup>2</sup>)−1) x (300 - $k$ +1)<sup>2</sup>
    Now , after applying maxpooling output will be
    $${(300 -k +3) \over 2 } \frac {(300 -k +3)}{ 2 }&times; m$$

-  **Conv2 layer Computation** : $$m &times; {(m ×  k^2)−1}) &times; \frac{(300 -k +3)}{ 2 }^2 $$
    Now , after applying maxpooling output will be
    $${((300 -k +3) / 2  - k +3) \over (2 -k +3)} \times {((300 -k +3) / 2  - k +1) \over (2 -k +3)} \times m $$

-  **Conv3 layer Computation** : $$m &times; {(m ×  k^2)−1} &times;{ \bigg ({(300 -k +3) / 2  - k +1) \over 2} -k +1 \bigg )}^2 $$
    Now , after applying maxpooling output will be
    $$\bigg ({{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\bigg )\times  \bigg  ({{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\bigg )\times m $$
    

-  **Conv4 layer Computation** : $$m &times; {(m ×  k^2)−1} &times;\bigg ({{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\bigg )^2 $$
    Now , after applying maxpooling output will be
    $$\bigg ({{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\bigg )^2\times m $$

-  **Conv5 layer Computation** : $$m &times; {(m ×  k^2)−1} &times;\bigg ({{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\bigg )^2 $$
    Now , after applying maxpooling output will be
    $$\bigg ({{{{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\over 2}-k +3}\bigg )^2\times m $$

-  **Dense layer Computation** : Given dense layer has $n$ neurons, no. of computations are
    $$\bigg(n \times \bigg ({{{{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\over 2}-k +3}\bigg )^2\times m \bigg) $$

-  **output layer Computation** : Given 10 classes, no. of computations are
    $$10 \times (2 \times n +1) $$


## Question 1: b)
- Here input size is $$300 \times 300 \times 3$$.
- number of classes is $10$.
- One thing to note that Max-pooling layers have 0 parameters.


| Layer | Inputs | Number of Parameters |
| --- | --- |--- |
| Conv1 | $$300 \times 300 \times 3$$| $$(3 \times k \times k+1) \times m $$|
| Conv2 | $${(300 -k +3) \over 2 } \frac {(300 -k +3)}{ 2 }&times; m$$| $$(m \times k \times k+1) \times m$$ |
| Conv3 | $$ (300-k+3) \times (300-k+3) \times m $$|  $$(m \times k \times k+1) \times m$$ |
| Conv4 | $$\bigg ({{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\bigg )\times  \bigg  ({{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\bigg )\times m $$ |  $$(m \times k \times k+1) \times m$$ |
| Conv5 |  $$\bigg ({{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\bigg )^2\times m $$|  $$(m \times k \times k+1) \times m$$  |
| Dense layer | $$\bigg ({{{{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\over 2}-k +3}\bigg )^2\times m $$ |$$\bigg(\bigg ({{{{{{{{{{{(300 -k +3)} \over 2}  - k +3 }\over 2} -k +3}\over 2}- k +3}\over 2} -k +3}\over 2}-k +3}\bigg )^2\times m + 1 \bigg) \times n $$|
| Output Layer | n|  $$(10 \times n \times k+ 10)  $$  |

- Total number of parameters =
