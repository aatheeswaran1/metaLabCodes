import numpy as np
import json
def getParams(param):
    if param == None:
        param = "exampleParam"
    with open('./specs.json') as paramFile:
        setOfParams = json.load(paramFile)
    data = setOfParams[param]
    return data

def convertToNpArray(matrix):
    return np.array(matrix)

def buildVisibilityMatrix(matrix):
    visibilityMatrix = []
    for row in matrix:
        rowList = [1/element if element !=0 else 0 for element in row]
        visibilityMatrix.append(rowList)
    return convertToNpArray(visibilityMatrix)

def buildPheromoneMatrix(shape):
    return np.ones(shape)

def buildSetOfPaths(departure, totalNumPlaces):
    possiblePaths = []
    for destination in range(totalNumPlaces):
        singlePath = [departure, destination]
        possiblePaths.append(singlePath)
    return possiblePaths