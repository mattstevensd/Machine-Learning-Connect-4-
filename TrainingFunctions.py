from tkinter import Y
import numpy as np

import math as mat

class PositionClass:
  def __init__(self, momma, pos):
    self.pos = pos
    self.babies = []
    self.momma = momma
    self.value = 0
    self.visits = 0
    self.UTC = 0
    self.turn = ''


def add_babies(tree, key):

  position = tree[key].pos

  if tree[key].turn == 'R':
    nextturn = 'B'
  elif tree[key].turn == 'B':
    nextturn = 'R'

  for i in range(7):

    position0 = np.zeros((2,6,7))
    position1 = np.zeros((2,6,7))

    for l in range(2):
      for j in range(6):
        for k in range(7):
          position0[l][j][k] = position[l][j][k]
    
    if position0[0][5][i] == 0 and position0[1][5][i] == 0:
      position0[0][5][i] = 1
      position1[0] = position0[1]
      position1[1] = position0[0]
      newkey = key + str(i)
      tree[key].babies.append(newkey)
      tree[newkey] = PositionClass(key, position1)
      tree[newkey].turn = nextturn
    elif position0[0][4][i] == 0 and position0[1][4][i] == 0:
      position0[0][4][i] = 1
      position1[0] = position0[1]
      position1[1] = position0[0]
      newkey = key + str(i)
      tree[key].babies.append(newkey)
      tree[newkey] = PositionClass(key, position1)
      tree[newkey].turn = nextturn
    elif position0[0][3][i] == 0 and position0[1][3][i] == 0:
      position0[0][3][i] = 1
      position1[0] = position0[1]
      position1[1] = position0[0]
      newkey = key + str(i)
      tree[key].babies.append(newkey)
      tree[newkey] = PositionClass(key, position1)
      tree[newkey].turn = nextturn
    elif position0[0][2][i] == 0 and position0[1][2][i] == 0:
      position0[0][2][i] = 1
      position1[0] = position0[1]
      position1[1] = position0[0]
      newkey = key + str(i)
      tree[key].babies.append(newkey)
      tree[newkey] = PositionClass(key, position1)
      tree[newkey].turn = nextturn
    elif position0[0][1][i] == 0 and position0[1][1][i] == 0:
      position0[0][1][i] = 1
      position1[0] = position0[1]
      position1[1] = position0[0]
      newkey = key + str(i)
      tree[key].babies.append(newkey)
      tree[newkey] = PositionClass(key, position1)
      tree[newkey].turn = nextturn
    elif position0[0][0][i] == 0 and position0[1][0][i] == 0:
      position0[0][0][i] = 1
      position1[0] = position0[1]
      position1[1] = position0[0]
      newkey = key + str(i)
      tree[key].babies.append(newkey)
      tree[newkey] = PositionClass(key, position1)
      tree[newkey].turn = nextturn
    else:
      pass
  return tree
def has_player_won(board): 
  test = [1,1,1,1]
  x = 0
  for j in range(6):
    for k in range(4):
      y = test[0]*board[1][j][k] + test[1]*board[1][j][k+1] + test[2]*board[1][j][k+2] + test[3]*board[1][j][k+3]
      if y == 4:
        x = 1
        return x
  for j in range(3):
    for k in range(7):
      y = test[0]*board[1][j][k] + test[1]*board[1][j+1][k] + test[2]*board[1][j+2][k] + test[3]*board[1][j+3][k]
      if y == 4:
        x = 1
        return x
  for j in range(3):
    for k in range(4):
      y = test[0]*board[1][j][k] + test[1]*board[1][j+1][k+1] + test[2]*board[1][j+2][k+2] + test[3]*board[1][j+3][k+3]
      if y == 4:
        x = 1
        return x
  for j in range(3):
    for k in range(4):
      y = test[0]*board[1][j+3][k] + test[1]*board[1][j+2][k+1] + test[2]*board[1][j+1][k+2] + test[3]*board[1][j][k+3]
      if y == 4:
        x = 1
        return x
  return x
def is_board_full(board):
  x = 0
  y = 0
  for l in range(2):
      for j in range(6):
        for k in range(7):
          x = x + board[l][j][k]
  
  if x == 42:
    y = 1

  return y
def AI_value(pos,neuralnet):
  nol = neuralnet['info'][0]
  neuralnetcalculation(neuralnet,pos)
  finallayer = nol
  x = neuralnet[str(finallayer)+'a'+'q'+'0'][0]
  return x
def AI_policy(pos,neuralnet):
  nol = neuralnet['info'][0]
  neuralnetcalculation(neuralnet,pos)
  finallayer = nol
  y = [1,1,1,1,1,1,1]
  for i in range(7):
    y[i] = neuralnet[str(finallayer)+'b'+'q'+str(i)][0]
  return y
def one_tree_search(tree, treetopkey, neuralnet):

  parentkey = treetopkey

  if tree[treetopkey].babies == []:
    add_babies(tree,treetopkey)

  y=0

  while y == 0:

    bestUTC = 'x'
    childvisits = 0
    for i in tree[parentkey].babies:
      childvisits = childvisits + tree[i].visits
    for i in tree[parentkey].babies:
      tree[i].UTC = -tree[i].value + 2*AI_policy(tree[parentkey].pos,neuralnet)[int(i[-1])]*mat.sqrt(childvisits)/(tree[i].visits+0.000001)
      if bestUTC == 'x':
        bestUTC = i
      elif tree[bestUTC].UTC<tree[i].UTC:
        bestUTC = i
    if tree[bestUTC].visits == 0:
      y = 1
    elif has_player_won(tree[bestUTC].pos) == 1:
      y = 1
    elif is_board_full(tree[bestUTC].pos) == 1:
      y = 1
    elif tree[bestUTC].babies == []:
      add_babies(tree, bestUTC)
      parentkey = bestUTC
    else:
      parentkey = bestUTC

  if has_player_won(tree[bestUTC].pos) == 1:
    propvalue = -1
  elif is_board_full(tree[bestUTC].pos) == 1:
    propvalue = 0
  else:
    propvalue = AI_value(tree[bestUTC].pos,neuralnet)

  tree[bestUTC].value = tree[bestUTC].value + propvalue
  tree[bestUTC].visits = tree[bestUTC].visits + 1

  x = 0
  update = tree[bestUTC].momma

  while x == 0:
    if update == treetopkey:
      x = 1
    else:
      if tree[bestUTC].turn == tree[update].turn:
        tree[update].value = tree[update].value + propvalue
      else:
        tree[update].value = tree[update].value - propvalue
      
      tree[update].visits = tree[update].visits + 1
      update = tree[update].momma
def donde_move(tree, treetopkey,neuralnet):

  print('AAAAA')
  
  z = 0

  while z < 50:
    one_tree_search(tree, treetopkey,neuralnet)
    #print([tree['00'].visits,tree['01'].visits,tree['02'].visits,tree['03'].visits,tree['04'].visits,tree['05'].visits,tree['06'].visits])
    z = z + 1
  
  totalvisits = 0

  for i in tree[treetopkey].babies:
    totalvisits = totalvisits + tree[i].visits
  
  policy = np.zeros((7))

  for i in tree[treetopkey].babies:
    x = tree[i].visits/totalvisits
    policy[int(i[-1])] = x

  return policy
def training_game(tree,neuralnet):

  print('WOW')

  singlegamedata = []

  currentposition = '0'

  z = 0

  while z == 0:
    
    if has_player_won(tree[currentposition].pos) == 1:
      singlegamedata.append([ currentposition , [0,0,0,0,0,0,0] , 0 ])
      z = 1
    elif is_board_full(tree[currentposition].pos) == 1:
      singlegamedata.append([ currentposition , [0,0,0,0,0,0,0] , 0 ])
      z = 1
    else:
      currentpolicy = donde_move(tree, currentposition,neuralnet)
      singlegamedata.append([ currentposition , currentpolicy , 0 ])

      x = ''
      y = -1

      for i in range(7):
        if currentpolicy[i] > y:
          y = currentpolicy[i]
          x = str(i)
  
      currentposition = currentposition + x
  if has_player_won(tree[currentposition].pos) == 1:

    for i in singlegamedata:
      if tree[i[0]].turn == tree[currentposition].turn:
        i[2] = -1
      else:
        i[2] = 1
  
  return singlegamedata
def training_series(tree,neuralnet,nog):
  x = 0
  seriesdata = []

  print(1)
  
  while x < nog:
    print(0)
    currentdata = training_game(tree,neuralnet)
    for i in currentdata:
      seriesdata.append(i)
    x = x+1
  
  return seriesdata


