import NeuralNetFunctions as fn

import TrainingFunctions as tf

import numpy as np

import math as mat

import json

class PositionClass:
  def __init__(self, momma, pos):
    self.pos = pos
    self.babies = []
    self.momma = momma
    self.value = 0
    self.visits = 0
    self.UTC = 0
    self.turn = ''

neuralnet = {}

#initialize neural network

fn.initializeinputlayer(neuralnet,2,6,7,4,['a','b'])
fn.initializeconvlayer(neuralnet,2,9,3,3)
fn.initializebiaslayer(neuralnet,2)
fn.initializerelulayer(neuralnet,2)
fn.initializeconvlayer(neuralnet,3,9,3,3)
fn.initializebiaslayer(neuralnet,3)
fn.initializerelulayer(neuralnet,3)
fn.initializeoutputlayer(neuralnet,4,'a',1)
fn.initializeoutputlayerbiases(neuralnet,4,'a',1)
fn.initializeoutputlayersquished(neuralnet,4,'a',1)
fn.initializeoutputlayer(neuralnet,4,'b',7)
fn.initializeoutputlayerbiases(neuralnet,4,'b',7)
fn.initializeoutputlayersquished(neuralnet,4,'b',7)

counter = 0

#Example training session with initialized net below

while counter < 5:

  tree = {}

  og = np.zeros((2,6,7))

  daddio = PositionClass('', og)

  daddio.turn = 'R'

  tree['0'] = daddio

  trainingdata = tf.training_series(tree,neuralnet,20)

  fn.multtrainingdata(neuralnet,trainingdata,tree)

  counter = counter + 1

with open("neuralnet.json", "w") as outfile:
    json.dump(neuralnet, outfile)

