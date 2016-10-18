### http://neuralnetworksanddeeplearning.com/chap3.html#the_cross-entropy_cost_function
#### Libraries
# Standard library
import json
import random
import sys
from numpy import *
import numpy

class QuadraticCost(object):
    @staticmethod
    def fn(a, y):
        return 0.5*linalg.norm(a-y)**2
    @staticmethod
    def delta(z, a, y):
        return (a-y) * sigmoid_prime(z)


class CrossEntropyCost(object):
    @staticmethod
    def fn(a, y):
        return sum(nan_to_num(-y*log(a)-(1-y)*log(1-a)))
    @staticmethod
    def delta(z, a, y):
        return (a-y)

# ----------- TEST FUNCTIONS --------------
def xor(a):
    if len(a) <= 0:
        return [0]
    x = a[0]
    for i in range(1, len(a)):
        x = (x != a[i])
    return [int(x)]

def example(a):
    if len(a) < 2:
        return [0]
    return [int(a[0] != a[1])]

def add(a):
    mid = int(len(a)/2)
    d = 0
    b = 0
    c = 0
    for i in range(0, int(mid)):
        d += pow(2, i) * a[len(a)-(i+mid)-1]
        b += pow(2, i) * a[len(a)-i-1]
        c += pow(2, i)
    _y = int(d+b)
    _yString = "{0:b}".format(_y)
    _length = len("{0:b}".format(int(c*2+1)))
    ret = []
    for i in range(len(_yString)):
        __y = _yString[i]
        ret.append(int(__y == '1'))
    while len(ret) < _length:
        ret.insert(0, 0)
    #print("{} + {} = {}".format(d, b, _y))
    #print("{} + {} = {}".format(a[:mid], a[mid:], ret))
    return ret
# -----------------------------------------

class TrainingSet:
    def __init__(self, bitLength, function, ignore=None):        
        inputBinarySet = []
        outputBinarySet = []
        xMax = int(pow(2, bitLength))
        for x in range(0, xMax):
            inputBinary = "{0:b}".format(x)
            while len(inputBinary) < bitLength:
                inputBinary = '0' + inputBinary
            inputBinaryList = []
            for character in inputBinary:
                inputBinaryList.append(int(character))

            if ignore is not None:
                skip = False
                for m in ignore:
                    same = True
                    for i in range(0, len(inputBinaryList)):
                        if inputBinaryList[i] != m[i]:
                            same = False
                    if same:
                        skip = True
                        break
                if skip:
                    continue
                
            inputBinarySet.append(inputBinaryList)
            
            y = function(inputBinaryList)
            outputBinarySet.append(y)
        
        self.input = array(inputBinarySet)
        self.output = array(outputBinarySet)
        self.tests = []
        for inputBinaryList, outputBinaryList in zip(inputBinarySet, outputBinarySet):
            self.tests.append((inputBinaryList, outputBinaryList))
        
        #print("-- IGNORE --\n{}".format(ignore))
        #print("-- IN --\n{}".format(self.input))
        #print("-- OUT --\n{}".format(self.output))

#### Main Network class
class Network(object):

    def __init__(self, sizes, cost=CrossEntropyCost):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.weight_initializer()
        self.cost=cost

    def weight_initializer(self):
        self.biases = [random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [random.randn(y, x)/sqrt(x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            lmbda = 0.0,
            evaluation_data=None,
            monitor_evaluation_cost=False,
            monitor_evaluation_accuracy=False,
            monitor_training_cost=False,
            monitor_training_accuracy=False):
        """Train the neural network using mini-batch stochastic gradient
        descent.  The ``training_data`` is a list of tuples ``(x, y)``
        representing the training inputs and the desired outputs.  The
        other non-optional parameters are self-explanatory, as is the
        regularization parameter ``lmbda``.  The method also accepts
        ``evaluation_data``, usually either the validation or test
        data.  We can monitor the cost and accuracy on either the
        evaluation data or the training data, by setting the
        appropriate flags.  The method returns a tuple containing four
        lists: the (per-epoch) costs on the evaluation data, the
        accuracies on the evaluation data, the costs on the training
        data, and the accuracies on the training data.  All values are
        evaluated at the end of each training epoch.  So, for example,
        if we train for 30 epochs, then the first element of the tuple
        will be a 30-element list containing the cost on the
        evaluation data at the end of each epoch. Note that the lists
        are empty if the corresponding flag is not set.

        """
        if evaluation_data:
            n_data = len(evaluation_data)
        n = len(training_data)
        evaluation_cost = []
        evaluation_accuracy = []
        training_cost = []
        training_accuracy = []
        
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta, lmbda, len(training_data))
            print("Epoch %s training complete" % j)
            if monitor_training_cost:
                cost = self.total_cost(training_data, lmbda)
                training_cost.append(cost)
                print("Cost on training data: {}".format(cost))
            if monitor_training_accuracy:
                accuracy = self.accuracy(training_data, convert=True)
                training_accuracy.append(accuracy)
                print("Accuracy on training data: {} / {}".format(accuracy, n))
            if monitor_evaluation_cost:
                cost = self.total_cost(evaluation_data, lmbda, convert=True)
                evaluation_cost.append(cost)
                print("Cost on evaluation data: {}".format(cost))
            if monitor_evaluation_accuracy:
                accuracy = self.accuracy(evaluation_data)
                evaluation_accuracy.append(accuracy)
                print("Accuracy on evaluation data: {} / {}".format(self.accuracy(evaluation_data), n_data))
            print("")
        return evaluation_cost, evaluation_accuracy, training_cost, training_accuracy

    def update_mini_batch(self, mini_batch, eta, lmbda, n):
        """Update the network's weights and biases by applying gradient
        descent using backpropagation to a single mini batch.  The
        ``mini_batch`` is a list of tuples ``(x, y)``, ``eta`` is the
        learning rate, ``lmbda`` is the regularization parameter, and
        ``n`` is the total size of the training data set.

        """
        nabla_b = [zeros(b.shape) for b in self.biases]
        nabla_w = [zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [(1-eta*(lmbda/n))*w-(eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [zeros(b.shape) for b in self.biases]
        nabla_w = [zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = (self.cost).delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = dot(delta, activations[-2].T)
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = dot(self.weights[-l+1].T, delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = dot(delta, array(activations[-l-1]).T)
        return (nabla_b, nabla_w)

    def accuracy(self, data, convert=False):
        """Return the number of inputs in ``data`` for which the neural
        network outputs the correct result. The neural network's
        output is assumed to be the index of whichever neuron in the
        final layer has the highest activation.

        The flag ``convert`` should be set to False if the data set is
        validation or test data (the usual case), and to True if the
        data set is the training data. The need for this flag arises
        due to differences in the way the results ``y`` are
        represented in the different data sets.  In particular, it
        flags whether we need to convert between the different
        representations.  It may seem strange to use different
        representations for the different data sets.  Why not use the
        same representation for all three data sets?  It's done for
        efficiency reasons -- the program usually evaluates the cost
        on the training data and the accuracy on other data sets.
        These are different types of computations, and using different
        representations speeds things up.  More details on the
        representations can be found in
        mnist_loader.load_data_wrapper.

        """
        if convert:
            results = [(argmax(self.feedforward(x)), argmax(y)) for (x, y) in data]
        else:
            results = [(argmax(self.feedforward(x)), y) for (x, y) in data]
        return sum(int(x == y) for (x, y) in results)

    def total_cost(self, data, lmbda, convert=False):
        cost = 0.0
        for x, y in data:
            a = self.feedforward(x)
            if convert:
                y = vectorized_result(y)
            cost += self.cost.fn(a, y)/len(data)
        cost += 0.5*(lmbda/len(data))*sum(linalg.norm(w)**2 for w in self.weights)
        return cost

    def save(self, filename):
        """Save the neural network to the file ``filename``."""
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()

#### Loading a Network
def load(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["sizes"], cost=cost)
    net.weights = [array(w) for w in data["weights"]]
    net.biases = [array(b) for b in data["biases"]]
    return net

#### Miscellaneous functions
def vectorized_result(j):
    e = zeros((10, 1))
    e[j] = 1.0
    return e

def sigmoid(z):
    return 1.0/(1.0+exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

def Test():
    net = Network([3, 3, 16, 14, 1], CrossEntropyCost)
    net.SGD(TrainingSet(3, example).tests, 10, 300, 0.05)
    print(net.feedforward([1, 0, 0]))

a = [1, 2, 3, 4, 5, 6]
for l in range(2, len(a)):
    print(a[-l])
input("waiting")
Test()
