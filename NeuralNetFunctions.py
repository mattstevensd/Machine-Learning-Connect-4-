from tkinter import Y
import numpy as np

import math as mat


#Initialize neural network structure with random values or fill with desired weights and biases
def initializeinputlayer(neuralnet,depth,height,width,nol,finalpartlist):
  neuralnet['info'] = [nol,finalpartlist]
  for i in range(depth):
    for j in range(height):
      for k in range(width):
        neuralnet['1'+ 'o'+str(i)+str(j)+str(k)] = [0,0]
  neuralnet['1'] = [str(depth),str(height),str(width),'x','x']
  return
def initializeconvlayer(neuralnet,layernumber,cnumber,cheight,cwidth):

  x = layernumber-1

  inputdim = neuralnet[str(x)]

  cdepth = int(inputdim[0])
  
  for i in range(cnumber):
    for j in range(cdepth):
      for k in range(cheight):
        for l in range(cwidth):
          currentkey = str(layernumber)+'c'+str(i)+str(j)+str(k)+str(l)
          neuralnet[currentkey] = [np.random.normal(0,0.1),0,0]

  outputdepth = cnumber

  outputheight = int(inputdim[1])-cheight+1

  outputwidth = int(inputdim[2])-cwidth+1

  for i in range(outputdepth):
    for j in range(outputheight):
      for k in range(outputwidth):
        currentkey = str(layernumber)+'o'+str(i)+str(j)+str(k)
        neuralnet[currentkey] = [0,0]

  neuralnet[str(layernumber)]=[str(outputdepth),str(outputheight),str(outputwidth),'x','x']
  return
def initializebiaslayer(neuralnet,layernumber):
  
  inputdim = neuralnet[str(layernumber)]

  outputdepth = int(inputdim[0])

  outputheight = int(inputdim[1])

  outputwidth = int(inputdim[2])

  for i in range(outputdepth):
    neuralnet[str(layernumber)+'b'+str(i)] = [np.random.uniform(0,0.1),0,0]
    for j in range(outputheight):
      for k in range(outputwidth):
        neuralnet[str(layernumber)+'b'+str(i)+str(j)+str(k)] = [0,0]

  neuralnet[str(layernumber)][3] = 'b'
  return
def initializerelulayer(neuralnet,layernumber):
  
  inputdim = neuralnet[str(layernumber)]

  outputdepth = int(inputdim[0])

  outputheight = int(inputdim[1])

  outputwidth = int(inputdim[2])

  for i in range(outputdepth):
    for j in range(outputheight):
      for k in range(outputwidth):
        neuralnet[str(layernumber)+'r'+str(i)+str(j)+str(k)] = [0,0]

  neuralnet[str(layernumber)][4] = 'r'
  return
def initializeoutputlayer(neuralnet,layernumber,part,size):
  
  x = layernumber - 1
  
  inputdim = neuralnet[str(x)]

  inputdepth = int(inputdim[0])
  inputheight = int(inputdim[1])
  inputwidth = int(inputdim[2])
  
  for y in range(size):
    neuralnet[str(layernumber)+part+'o'+str(y)] = [0,0]
    for i in range(inputdepth):
      for j in range(inputheight):
        for k in range(inputwidth):
          neuralnet[str(layernumber)+part+'w'+str(y)+str(i)+str(j)+str(k)] = [np.random.normal(0,0.1),0,0]

  neuralnet[str(layernumber)+part] = str(size)
  return
def initializeoutputlayerbiases(neuralnet,layernumber,part,size):
  
  for y in range(size):
    neuralnet[str(layernumber)+part+'b'+str(y)] = [np.random.normal(0,0.1),0,0]
    neuralnet[str(layernumber)+part+'p'+str(y)] = [0,0]
def initializeoutputlayersquished(neuralnet,layernumber,part,size):
  for y in range(size):
    neuralnet[str(layernumber)+part+'q'+str(y)] = [0,0]

#Calculation funcitons (neural net calculates outpus layer values given some input)
def relucalculation(neuralnet,layernumber):

  inputdim = neuralnet[str(layernumber)]

  outputdepth = int(inputdim[0])

  outputheight = int(inputdim[1])

  outputwidth = int(inputdim[2])
  
  if neuralnet[str(layernumber)][3]=='b':
    for i in range(outputdepth):
      for j in range(outputheight):
        for k in range(outputwidth):
          keyb = str(layernumber)+'b'+str(i)+str(j)+str(k)
          keyr = str(layernumber)+'r'+str(i)+str(j)+str(k)
          if neuralnet[keyb][0] >= 0:
            neuralnet[keyr][0]=neuralnet[keyb][0]
          else:
            neuralnet[keyr][0]=0
  else:
    for i in range(outputdepth):
      for j in range(outputheight):
        for k in range(outputwidth):
          keyo = str(layernumber)+'o'+str(i)+str(j)+str(k)
          keyr = str(layernumber)+'r'+str(i)+str(j)+str(k)
          if neuralnet[keyo][0] >= 0:
            neuralnet[keyr][0]=neuralnet[keyo][0]
          else:
            neuralnet[keyr][0]=0
def biascalculation(neuralnet,layernumber):

  inputdim = neuralnet[str(layernumber)]

  outputdepth = int(inputdim[0])

  outputheight = int(inputdim[1])

  outputwidth = int(inputdim[2])

  for i in range(outputdepth):
    currentbias = neuralnet[str(layernumber)+'b'+str(i)][0]
    for j in range(outputheight):
      for k in range(outputwidth):
        currentinput = neuralnet[str(layernumber)+'o'+str(i)+str(j)+str(k)][0]
        currentoutput = currentinput + currentbias
        neuralnet[str(layernumber)+'b'+str(i)+str(j)+str(k)][0] = currentoutput
  return
def convolutioncalculation(neuralnet,layernumber):
  
  inputdim = neuralnet[str(layernumber-1)]

  idepth = int(inputdim[0])

  iheight = int(inputdim[1])

  iwidth = int(inputdim[2])

  outputdim = neuralnet[str(layernumber)]

  odepth = int(outputdim[0])

  oheight = int(outputdim[1])

  owidth = int(outputdim[2])

  cnum = odepth

  cdepth = idepth

  cheight = iheight - oheight + 1

  cwidth = iwidth - owidth + 1

  if inputdim[4] == 'r':
    type = 'r'
  elif inputdim[3]=='b':
    type = 'b'
  else:
    type = 'o'

  for i in range(cnum):
    
    for x in range(oheight):
      for y in range(owidth):
        convcalc = 0
        for j in range(cdepth):
          for k in range(cheight):
            for l in range(cwidth):
              convalue = neuralnet[str(layernumber)+'c'+str(i)+str(j)+str(k)+str(l)][0]
              invalue = neuralnet[str(layernumber-1)+type+str(j)+str(x+k)+str(y+l)][0]
              convcalc = convcalc + convalue*invalue
        neuralnet[str(layernumber)+'o'+str(i)+str(x)+str(y)][0] = convcalc
  return
def outputlayercalculation(neuralnet,layernumber,part):

  inputdim = neuralnet[str(layernumber-1)]
  outputdim = neuralnet[str(layernumber)+part]

  idepth = int(inputdim[0])
  iheight = int(inputdim[1])
  iwidth = int(inputdim[2])

  osize = int(outputdim)

  if inputdim[4] == 'r':
    type = 'r'
  elif inputdim[3]=='b':
    type = 'b'
  else:
    type = 'o'
  

  for x in range(osize):
    calc = 0
    for i in range(idepth):
      for j in range(iheight):
        for k in range(iwidth):
          inputvaluekey = str(layernumber-1)+type+str(i)+str(j)+str(k)
          weightvaluekey = str(layernumber)+part+'w'+str(x)+str(i)+str(j)+str(k)
          inputvalue = neuralnet[inputvaluekey][0]
          weightvalue = neuralnet[weightvaluekey][0]
          calc = calc + inputvalue*weightvalue
    neuralnet[str(layernumber)+part+'o'+str(x)][0] = calc
  return
def outputbiascalculation(neuralnet,layernumber,part):
  
  outputdim = neuralnet[str(layernumber)+part]
  osize = int(outputdim)

  for x in range(osize):
    biaskey = str(layernumber)+part+'b'+str(x)
    inputkey = str(layernumber)+part+'o'+str(x)
    bias = neuralnet[biaskey][0]
    input = neuralnet[inputkey][0]
    calc = input+bias
    neuralnet[str(layernumber)+part+'p'+str(x)][0] = calc
def outputsquishcalculationa(neuralnet,layernumber,part):
  outputdim = neuralnet[str(layernumber)+part]
  osize = int(outputdim)

  for x in range(osize):
    inputkey = str(layernumber)+part+'p'+str(x)
    input = neuralnet[inputkey][0]
    calc = ((2*mat.exp(4*input))/(1+mat.exp(4*input)))-1
    neuralnet[str(layernumber)+part+'q'+str(x)][0] = calc
def outputsquishcalculationb(neuralnet,layernumber,part):
  
  outputdim = neuralnet[str(layernumber)+part]
  osize = int(outputdim)

  for x in range(osize):
    inputkey = str(layernumber)+part+'p'+str(x)
    input = neuralnet[inputkey][0]
    calc = ((mat.exp(4*input))/(1+mat.exp(4*input)))
    neuralnet[str(layernumber)+part+'q'+str(x)][0] = calc
def neuralnetcalculation(neuralnet,inputarray):
  nol = neuralnet['info'][0]
  finalpartlist = neuralnet['info'][1]

  inputdepth = int(neuralnet['1'][0])
  inputheight = int(neuralnet['1'][1])
  inputwidth = int(neuralnet['1'][2])

  for i in range(inputdepth):
    for j in range(inputheight):
      for k in range(inputwidth):
        neuralnet['1'+'o'+str(i)+str(j)+str(k)][0] = inputarray[i][j][k]

  noml = nol - 2

  for z in range(noml):
    
    layernumber = z+2
    
    convolutioncalculation(neuralnet,layernumber)
    if neuralnet[str(layernumber)][3] == 'b':
      biascalculation(neuralnet,layernumber)
    if neuralnet[str(layernumber)][4] == 'r':
      relucalculation(neuralnet,layernumber)

  finallayer = nol

  for q in finalpartlist:
    outputlayercalculation(neuralnet, finallayer,q)
    outputbiascalculation(neuralnet,finallayer,q)
    if q == 'a':
      outputsquishcalculationa(neuralnet,finallayer,q)
    elif q == 'b':
      outputsquishcalculationb(neuralnet,finallayer,q)

#backprop functions (given some desired output, this will back propoagte all partial derivates and store them in neural net)
def dLd_firstconvlayer(neuralnet,layernumber):
  outputdepth = int(neuralnet[str(layernumber)][0])
  outputheight = int(neuralnet[str(layernumber)][1])
  outputwidth = int(neuralnet[str(layernumber)][2])
  
  inputdepth = int(neuralnet[str(layernumber-1)][0])
  inputheight = int(neuralnet[str(layernumber-1)][1])
  inputwidth = int(neuralnet[str(layernumber-1)][2])

  convdepth = inputdepth
  convheight = inputheight - outputheight + 1
  convwidth = inputwidth - outputwidth + 1

  if neuralnet[str(layernumber-1)][4] == 'r':
    inputtype = 'r'
  elif neuralnet[str(layernumber-1)][3] == 'b':
    inputtype = 'b'
  else:
    inputtype = 'o'
  
  for i in range(outputdepth):
    convnumber = i
    for j in range(outputheight):
      for k in range(outputwidth):
        dL_dCurrentoutput = neuralnet[str(layernumber)+'o'+str(i)+str(j)+str(k)][1]
        for l in range(convdepth):
          for m in range(convheight):
            for n in range(convwidth):
              dCurrentoutput_dCurrentconv = neuralnet[str(layernumber-1) + inputtype + str(l)+str(j+m)+str(k+n)][0]
              currentconvkey = str(layernumber)+'c'+str(convnumber)+str(l)+str(m)+str(n)
              dL_dCurrentconv = neuralnet[currentconvkey][1]
              neuralnet[currentconvkey][1] = dL_dCurrentconv + dL_dCurrentoutput * dCurrentoutput_dCurrentconv
  return
def dLd_middleconvlayer(neuralnet,layernumber):
  
  outputdepth = int(neuralnet[str(layernumber)][0])
  outputheight = int(neuralnet[str(layernumber)][1])
  outputwidth = int(neuralnet[str(layernumber)][2])
  
  inputdepth = int(neuralnet[str(layernumber-1)][0])
  inputheight = int(neuralnet[str(layernumber-1)][1])
  inputwidth = int(neuralnet[str(layernumber-1)][2])

  convdepth = inputdepth
  convheight = inputheight - outputheight + 1
  convwidth = inputwidth - outputwidth + 1

  if neuralnet[str(layernumber-1)][4] == 'r':
    inputtype = 'r'
  elif neuralnet[str(layernumber-1)][3] == 'b':
    inputtype = 'b'
  else:
    inputtype = 'o'
  
  for i in range(outputdepth):
    convnumber = i
    for j in range(outputheight):
      for k in range(outputwidth):
        dL_dCurrentoutput = neuralnet[str(layernumber)+'o'+str(i)+str(j)+str(k)][1]
        for l in range(convdepth):
          for m in range(convheight):
            for n in range(convwidth):
              dCurrentoutput_dCurrentconv = neuralnet[str(layernumber-1) + inputtype + str(l)+str(j+m)+str(k+n)][0]
              dCurrentoutput_dCurrentinput = neuralnet[str(layernumber)+'c'+str(convnumber)+str(l)+str(m)+str(n)][0]
              currentconvkey = str(layernumber)+'c'+str(convnumber)+str(l)+str(m)+str(n)
              currentinputkey = str(layernumber-1) + inputtype + str(l)+str(j+m)+str(k+n)
              dL_dCurrentconv = neuralnet[currentconvkey][1]
              dL_dCurrentinput = neuralnet[currentinputkey][1]
              neuralnet[currentconvkey][1] = dL_dCurrentconv + dL_dCurrentoutput * dCurrentoutput_dCurrentconv
              neuralnet[currentinputkey][1] = dL_dCurrentinput + dL_dCurrentoutput * dCurrentoutput_dCurrentinput
  return
def dLd_biaslayer(neuralnet,layernumber):
  
  outputdepth = int(neuralnet[str(layernumber)][0])
  outputheight = int(neuralnet[str(layernumber)][1])
  outputwidth = int(neuralnet[str(layernumber)][2])

  for i in range(outputdepth):
    
    for j in range(outputheight):
      for k in range(outputwidth):
        ##derivative for input matrix
        dL_dCurrentoutput = neuralnet[str(layernumber) + 'b' + str(i)+str(j)+str(k)][1]
        dCurrentoutput_dCurrentinput = 1
        currentinputkey = str(layernumber) + 'o' + str(i)+str(j)+str(k)
        neuralnet[currentinputkey][1] = dL_dCurrentoutput *dCurrentoutput_dCurrentinput
        ##derivative for bias
        dCurrentoutput_dCurrentbias = 1
        currentbiaskey = str(layernumber)+'b'+str(i)
        dL_dCurrentbias = neuralnet[currentbiaskey][1]
        neuralnet[currentbiaskey][1] = dL_dCurrentbias + dL_dCurrentoutput*dCurrentoutput_dCurrentbias
def dLd_relulayer(neuralnet,layernumber):
  
  outputdepth = int(neuralnet[str(layernumber)][0])
  outputheight = int(neuralnet[str(layernumber)][1])
  outputwidth = int(neuralnet[str(layernumber)][2])

  if neuralnet[str(layernumber-1)][3] == 'b':
    inputtype = 'b'
  else:
    inputtype = 'o'
  
  for i in range(outputdepth):
    for j in range(outputheight):
      for k in range(outputwidth):
        dL_dCurrentoutput = neuralnet[str(layernumber)+'r'+str(i)+str(j)+str(k)][1]
        currentinputkey = str(layernumber)+inputtype+str(i)+str(j)+str(k)
        if neuralnet[currentinputkey][0]>=0:
          dCurrentoutput_dCurrentinput = 1
        else:
          dCurrentoutput_dCurrentinput = 0
        neuralnet[currentinputkey][1] = dL_dCurrentoutput * dCurrentoutput_dCurrentinput
def dLd_finalweightlayer(neuralnet,layernumber,part):
  
  inputdim = neuralnet[str(layernumber-1)]
  
  outputsize = int(neuralnet[str(layernumber)+part])
  
  inputdepth = int(inputdim[0])
  inputheight = int(inputdim[1])
  inputwidth = int(inputdim[2])

  if inputdim[4] == 'r':
    type = 'r'
  elif inputdim[3] == 'b':
    type = 'b'
  else:
    type = 'o'

  for y in range(outputsize):
    dL_dCurrentoutput = neuralnet[str(layernumber)+part+'o'+str(y)][1]
    for i in range(inputdepth):
      for j in range(inputheight):
        for k in range(inputwidth):
          currentweightkey = str(layernumber)+part+'w'+str(y)+str(i)+str(j)+str(k)
          currentinputkey = str(layernumber-1)+type+str(i)+str(j)+str(k)
          dCurrentoutput_dCurrentweight = neuralnet[currentinputkey][0]
          dCurrentoutput_dCurrentinput = neuralnet[currentweightkey][0]
          dL_dCurrentinput = neuralnet[currentinputkey][1]
          neuralnet[currentinputkey][1] = dL_dCurrentinput + dL_dCurrentoutput*dCurrentoutput_dCurrentinput
          neuralnet[currentweightkey][1] = dL_dCurrentoutput*dCurrentoutput_dCurrentweight
def dLd_finalbiaslayer(neuralnet,layernumber,part):
  
  inputsize = int(neuralnet[str(layernumber)+part])
  
  for y in range(inputsize):
    dL_dCurrentoutput = neuralnet[str(layernumber)+part+'p'+str(y)][1]
    
    dCurrentoutput_dCurrentinput = 1
    dCurrentoutput_dCurrentbias = 1
    
    currentinputkey = str(layernumber) + part + 'o' +str(y)
    currentbiaskey = str(layernumber) + part + 'b' + str(y)

    neuralnet[currentinputkey][1] = dL_dCurrentoutput*dCurrentoutput_dCurrentinput
    neuralnet[currentbiaskey][1] = dL_dCurrentoutput*dCurrentoutput_dCurrentbias
def dLd_finalsquishlayera(neuralnet,layernumber,part): 
  inputsize = int(neuralnet[str(layernumber)+part])

  for y in range(inputsize):
    dL_dCurrentoutput = neuralnet[str(layernumber)+part+'q'+str(y)][1]
    
    currentinputkey = str(layernumber)+part+'p'+str(y)
    currentinput = neuralnet[currentinputkey][0]

    dCurrentoutput_dCurrentinput = ((8*mat.exp(4*currentinput))/((1+mat.exp(4*currentinput))**2))

    neuralnet[currentinputkey][1] = dL_dCurrentoutput*dCurrentoutput_dCurrentinput
def dLd_finalsquishlayerb(neuralnet,layernumber,part): 
  
  inputsize = int(neuralnet[str(layernumber)+part])

  for y in range(inputsize):
    dL_dCurrentoutput = neuralnet[str(layernumber)+part+'q'+str(y)][1]
    
    currentinputkey = str(layernumber)+part+'p'+str(y)
    currentinput = neuralnet[currentinputkey][0]

    dCurrentoutput_dCurrentinput = ((4*mat.exp(4*currentinput))/((1+mat.exp(4*currentinput))**2))

    neuralnet[currentinputkey][1] = dL_dCurrentoutput*dCurrentoutput_dCurrentinput
def neuralnetbackprop(neuralnet,inputarray):
  
  nol = neuralnet['info'][0]

  finalpartlist = neuralnet['info'][1]
  
  neuralnet['4'+'a'+'q'+'0'][1] = inputarray[0]

  for x in range(7):
    neuralnet['4'+'b'+'q'+str(x)][1] = inputarray[1][x]

  finallayer = nol

  for y in finalpartlist:
    if y == 'a':
      dLd_finalsquishlayera(neuralnet,finallayer,y)
    elif y == 'b':
      dLd_finalsquishlayerb(neuralnet,finallayer,y)
    dLd_finalbiaslayer(neuralnet,finallayer,y)
    dLd_finalweightlayer(neuralnet,finallayer,y)

  noml = nol - 2

  for z in range(noml):
    currentlayer = finallayer-z-1
    dLd_relulayer(neuralnet,currentlayer)
    dLd_biaslayer(neuralnet,currentlayer)
    if currentlayer == 2:
      dLd_firstconvlayer(neuralnet,currentlayer)
    else:
      dLd_middleconvlayer(neuralnet,currentlayer)

#training and backpropfunctions (Given a list of training data, these fucntions will conduct all backpropogations for all training data)
def singletrainingdata(neuralnet,trainingposition,positionvalue,moveprobability):

  neuralnetcalculation(neuralnet,trainingposition)

  dL_dO = []

  dL_dO_move = []

  npositionvalue = neuralnet['4aq0'][0]

  dL_dO.append(2*(npositionvalue-positionvalue))

  for i in range(7):
    nmoveprobabililty = neuralnet['4bq'+str(i)][0]
    currmoveprobability = moveprobability[i]

    dL_dO_move.append(2*(nmoveprobabililty-currmoveprobability))

  dL_dO.append(dL_dO_move)

  neuralnetbackprop(neuralnet,dL_dO)
def multtrainingdata(neuralnet,trainingdatalist,tree):

    notd = 0

    for i in trainingdatalist:
        notd = notd + 1
        trainingposition = i[0]
        positionvalue = i[2]
        moveprobability = i[1]

        trainingposarray = tree[trainingposition].pos

        singletrainingdata(neuralnet,trainingposarray,positionvalue,moveprobability)

        weightbiasupdatezero(neuralnet)

        activationzero(neuralnet)

    changeweights(neuralnet,notd)

    return

    
def initializeupdatelist(neuralnet):
     

    updatelist = []

    nol = neuralnet['info'][0]
    finalpartlist = neuralnet['info'][1]

    noul = nol - 1

    for i in range(noul):
        updatelist.append([])
    
    noml = nol - 2

    for i in range(noml):
        updatelist[i].append([])
        updatelist[i].append([])

        currentlayer = 2 + i
        prevlayer = currentlayer - 1

        inputdepth = int(neuralnet[str(prevlayer)][0])
        inputheight = int(neuralnet[str(prevlayer)][1])
        inputwidth = int(neuralnet[str(prevlayer)][2])

        outputdepth = int(neuralnet[str(currentlayer)][0])
        outputheight = int(neuralnet[str(currentlayer)][1])
        outputwidth = int(neuralnet[str(currentlayer)][2])

        convnum = outputdepth
        convdepth = inputdepth
        convheight = inputheight - outputheight + 1
        convwidth = inputwidth - outputwidth + 1

        biasnum = convnum

        for z in range(convnum):
            updatelist[i][0].append([])
            updatelist[i][1].append(0)
            for k in range(convdepth):
                updatelist[i][0][z].append([])
                for j in range(convheight):
                    updatelist[i][0][z][k].append([])
                    for l in range(convwidth):
                        updatelist[i][0][z][k][j].append(0)
        
    finallayer = nol

    inputdepth = int(neuralnet[str(finallayer-1)][0])
    inputheight = int(neuralnet[str(finallayer-1)][1])
    inputwidth = int(neuralnet[str(finallayer-1)][2])

    blep = 0

    for i in finalpartlist:
        blep = blep + 1
        updatelist[finallayer - 2].append([])

        updatelist[finallayer-2][blep-1].append([])
        updatelist[finallayer-2][blep-1].append([])

        outputnumber = int(neuralnet[str(finallayer)+i])

        for j in range(outputnumber):
            updatelist[finallayer - 2][blep-1][1].append(0)
            updatelist[finallayer - 2][blep-1][0].append([])
            for k in range(inputdepth):
                updatelist[finallayer - 2][blep-1][0][j].append([])
                for l in range(inputheight):
                    updatelist[finallayer - 2][blep-1][0][j][k].append([])
                    for m in range(inputwidth):
                        updatelist[finallayer - 2][blep-1][0][j][k][l].append(0)
    
    return updatelist
def populateupdatelist(neuralnet,updatelist):

    nol = neuralnet['info'][0]
    finalpartlist = neuralnet['info'][1]

    noml = nol - 2

    for i in range(noml):
        currentlayer = i + 2
        prevlayer = currentlayer - 1

        inputdepth = int(neuralnet[str(prevlayer)][0])
        inputheight = int(neuralnet[str(prevlayer)][1])
        inputwidth = int(neuralnet[str(prevlayer)][2])

        outputdepth = int(neuralnet[str(currentlayer)][0])
        outputheight = int(neuralnet[str(currentlayer)][1])
        outputwidth = int(neuralnet[str(currentlayer)][2])

        convnum = outputdepth
        convdepth = inputdepth
        convheight = inputheight - outputheight + 1
        convwidth = inputwidth - outputwidth + 1

        for j in range(convnum):
            corrbiaskey = str(currentlayer) + 'b' + str(j)
            corrbiasupdatevalue = updatelist[currentlayer-2][1][j]
            updatelist[currentlayer-2][1][j] = corrbiasupdatevalue + neuralnet[corrbiaskey][1]
            for k in range(convdepth):
                for l in range(convheight):
                    for m in range(convwidth):
                        corrconvkey = str(currentlayer) + 'c' + str(j) + str(k) + str(l) + str(m)
                        corrupdatevalue = updatelist[currentlayer-2][0][j][k][l][m]
                        updatelist[currentlayer-2][0][j][k][l][m] = corrupdatevalue + neuralnet[corrconvkey][1]
    
    finallayer = nol

    inputdepth = int(neuralnet[str(finallayer-1)][0])
    inputheight = int(neuralnet[str(finallayer-1)][1])
    inputwidth = int(neuralnet[str(finallayer-1)][2])

    blep = 0

    for i in finalpartlist:

        blep = blep + 1
        outputsize = int(neuralnet[str(finallayer) + i])

        for j in range(outputsize):
            corrbiaskey = str(finallayer) + i + 'b' + str(j)
            corrbiasupdatevalue = updatelist[finallayer-2][blep-1][1][j]
            updatelist[finallayer-2][blep-1][1][j] = corrbiasupdatevalue + neuralnet[corrbiaskey][1]
            for k in range(inputdepth):
                for l in range(inputheight):
                    for m in range(inputwidth):
                        corrweightkey = str(finallayer) + i + 'w' + str(j)+str(k)+str(l)+str(m)
                        corrupdatevalue = updatelist[finallayer-2][blep-1][0][j][k][l][m]
                        updatelist[finallayer-2][blep-1][0][j][k][l][m] = corrupdatevalue + neuralnet[corrweightkey][1]
    return

#cleanupfunctions
def weightbiasupdatezero(neuralnet):
    nol = neuralnet['info'][0]
    finalpartlist = neuralnet['info'][1]

    noml = nol - 2

    for x in range(noml):
        currentlayer = 2 + x
        prevlayer = currentlayer - 1

        inputdepth = int(neuralnet[str(prevlayer)][0])
        inputheight = int(neuralnet[str(prevlayer)][1])
        inputwidth = int(neuralnet[str(prevlayer)][2])

        outputdepth = int(neuralnet[str(currentlayer)][0])
        outputheight = int(neuralnet[str(currentlayer)][1])
        outputwidth = int(neuralnet[str(currentlayer)][2])

        convnum = outputdepth
        convdepth = inputdepth
        convheight = inputheight - outputheight + 1
        convwidth = inputwidth - outputwidth + 1

        for n in range(convnum):
            currentbiaskey = str(currentlayer)+'b'+str(n)
            currentbiasderiv = neuralnet[currentbiaskey][1]
            currentsumbiasderiv = neuralnet[currentbiaskey][2]
            neuralnet[currentbiaskey][2] = currentsumbiasderiv + currentbiasderiv
            neuralnet[currentbiaskey][1] = 0
            for i in range(convdepth):
                for j in range(convheight):
                    for k in range(convwidth):
                        currentconvkey = str(currentlayer)+'c'+str(n)+str(i)+str(j)+str(k)
                        currentderiv = neuralnet[currentconvkey][1]
                        currentsumderiv = neuralnet[currentconvkey][2]
                        neuralnet[currentconvkey][2] = currentsumderiv + currentderiv
                        neuralnet[currentconvkey][1] = 0

    finallayer = nol

    inputdepth = int(neuralnet[str(finallayer-1)][0])
    inputheight = int(neuralnet[str(finallayer-1)][1])
    inputwidth = int(neuralnet[str(finallayer-1)][2])

    for x in finalpartlist:
        outputsize = int(neuralnet[str(finallayer)+x])

        for n in range(outputsize):
            currentbiaskeyf = str(finallayer) + x + 'b' + str(n)
            currentbiasderivf = neuralnet[currentbiaskeyf][1]
            currentsumbiasderivf = neuralnet[currentbiaskeyf][2]
            neuralnet[currentbiaskeyf][2] = currentbiasderivf + currentsumbiasderivf
            neuralnet[currentbiaskeyf][1] = 0
            for i in range(inputdepth):
                for j in range(inputheight):
                    for k in range(inputwidth):
                        currentweightkey = str(finallayer)+ x + 'w' + str(n) + str(i) + str(j) + str(k)
                        currentweightderiv = neuralnet[currentweightkey][1]
                        currentweightsumderiv = neuralnet[currentweightkey][2] 
                        neuralnet[currentweightkey][2] = currentweightderiv + currentweightsumderiv
                        neuralnet[currentweightkey][1] = 0
    return
def activationzero(neuralnet):
    nol = neuralnet['info'][0]
    finalpartlist = neuralnet['info'][1]

    noml = nol - 2

    for x in range(noml):
        currentlayer = 2 + x

        outputdepth = int(neuralnet[str(currentlayer)][0])
        outputheight = int(neuralnet[str(currentlayer)][1])
        outputwidth = int(neuralnet[str(currentlayer)][2])

        for i in range(outputdepth):
            for j in range(outputheight):
                for k in range(outputwidth):
                    currokey = str(currentlayer) + 'o' + str(i) + str(j) + str(k)
                    currbkey = str(currentlayer) + 'b' + str(i) + str(j) + str(k)
                    currrkey = str(currentlayer) + 'r' + str(i) + str(j) + str(k)
                    neuralnet[currokey][1] = 0
                    neuralnet[currbkey][1] = 0
                    neuralnet[currrkey][1] = 0
    
    finallayer = nol

    for y in finalpartlist:
        outputsize = int(neuralnet[str(finallayer) + y])

        for z in range(outputsize):
            currfokey = str(finallayer) + y + 'o' + str(z)
            currfpkey = str(finallayer) + y + 'p' + str(z)
            currfqkey = str(finallayer) + y + 'q' + str(z)
            neuralnet[currfokey][1] = 0
            neuralnet[currfpkey][1] = 0
            neuralnet[currfqkey][1] = 0
    return
def changeweights(neuralnet,divisor):
    nol = neuralnet['info'][0]
    finalpartlist = neuralnet['info'][1]

    noml = nol - 2

    for x in range(noml):
        currentlayer = 2 + x
        prevlayer = currentlayer - 1

        inputdepth = int(neuralnet[str(prevlayer)][0])
        inputheight = int(neuralnet[str(prevlayer)][1])
        inputwidth = int(neuralnet[str(prevlayer)][2])

        outputdepth = int(neuralnet[str(currentlayer)][0])
        outputheight = int(neuralnet[str(currentlayer)][1])
        outputwidth = int(neuralnet[str(currentlayer)][2])

        convnum = outputdepth
        convdepth = inputdepth
        convheight = inputheight - outputheight + 1
        convwidth = inputwidth - outputwidth + 1

        for n in range(convnum):
            currentbiaskey = str(currentlayer)+'b'+str(n)
            finalbiasderivsum = neuralnet[currentbiaskey][2]
            currenteditbias = (finalbiasderivsum/divisor)*-1*0.1
            neuralnet[currentbiaskey][2] = 0
            neuralnet[currentbiaskey][0] = neuralnet[currentbiaskey][0] + currenteditbias
            for i in range(convdepth):
                for j in range(convheight):
                    for k in range(convwidth):
                        currentconvkey = str(currentlayer)+'c'+str(n)+str(i)+str(j)+str(k)
                        finalconvderivsum = neuralnet[currentconvkey][2]
                        currenteditconv = (finalconvderivsum/divisor)*-1*0.1
                        neuralnet[currentconvkey][2] = 0
                        neuralnet[currentconvkey][0] = neuralnet[currentconvkey][0] + currenteditconv
                        

    finallayer = nol

    inputdepth = int(neuralnet[str(finallayer-1)][0])
    inputheight = int(neuralnet[str(finallayer-1)][1])
    inputwidth = int(neuralnet[str(finallayer-1)][2])

    for x in finalpartlist:
        outputsize = int(neuralnet[str(finallayer)+x])

        for n in range(outputsize):
            currentbiaskeyf = str(finallayer) + x + 'b' + str(n)
            finalbiasderivsumf = neuralnet[currentbiaskeyf][2]
            currenteditbiasf = (finalbiasderivsumf/divisor)*-1*0.1
            neuralnet[currentbiaskeyf][2] = 0
            neuralnet[currentbiaskeyf][0] = neuralnet[currentbiaskeyf][0] + currenteditbiasf
            for i in range(inputdepth):
                for j in range(inputheight):
                    for k in range(inputwidth):
                        currentweightkey = str(finallayer)+ x + 'w' + str(n) + str(i) + str(j) + str(k)
                        finalweightderivsum = neuralnet[currentweightkey][2]
                        currenteditweight = (finalweightderivsum/divisor)*-1*0.1
                        neuralnet[currentweightkey][2] = 0
                        neuralnet[currentweightkey][0] = neuralnet[currentweightkey][0] + currenteditweight
