from math import pow as power
from essentials import buildSetOfPaths
from random import random
import copy

def setZeroVisibility(matrix, currentLocation):
    matrix[:, currentLocation] = 0
    return matrix

def phermoneVisibilityProduct(visibilityArray, pheromoneArray, alpha, beta):
    productList = [power(pheromoneArray[i], alpha) * power(visibilityArray[i], beta) for i in range(len(visibilityArray))]
    return productList

def calculateProbability(productList, sum):
    probabilityList = [product/sum for product in productList]
    return probabilityList

def cumulativeSum(probabilityList):
    lastElement = probabilityList.pop()
    if len(probabilityList):
        cumulativeList = cumulativeSum(probabilityList)
        newElement = cumulativeList[-1] + lastElement
        cumulativeList.append(newElement)
        return cumulativeList
    else:
        return [lastElement]

def zeroIndices(probabilityList):
    itemIndexTODelete = []
    for i in range(len(probabilityList)):
        if not probabilityList[i]:
            itemIndexTODelete.append(i)
    return itemIndexTODelete

def deleteListItems(list_, indexTODelete):
    newList = []
    for i in range(len(list_)):
        if i not in indexTODelete:
            newList.append(list_[i])
    return newList

def checkProbability(randomNum, cumulativeSumList):
    for i in range(len(cumulativeSumList)):
        if randomNum <= cumulativeSumList[i]:
            return i

def getPath(visibilityMatrix, pheromoneMatrix, alpha, beta, departure, totalNumPlaces, visited):
    if visited == totalNumPlaces:
        return []
    possiblePaths = buildSetOfPaths(departure, totalNumPlaces)
    visibilityMatrix = setZeroVisibility(visibilityMatrix, departure)
    visibilityArray = visibilityMatrix[departure][:]
    pheromoneArray = pheromoneMatrix[departure][:]
    pheromoneVisibilityProductList = phermoneVisibilityProduct(visibilityArray, pheromoneArray, alpha, beta)
    sum_PhermononeVisibilityProduct = sum(pheromoneVisibilityProductList)
    probabilityList = calculateProbability(pheromoneVisibilityProductList, sum_PhermononeVisibilityProduct)
    itemIndexToDelete = zeroIndices(probabilityList)
    zeroCorrectedProbabilityList = deleteListItems(probabilityList, itemIndexToDelete)
    correctedPossiblePaths = deleteListItems(possiblePaths, itemIndexToDelete)
    cumulativeSumList = cumulativeSum(zeroCorrectedProbabilityList)
    randomNum = random()
    possibleRange = checkProbability(randomNum, cumulativeSumList)
    nextPossibleLocation = correctedPossiblePaths[possibleRange][1]
    visited += 1
    pathList = getPath(visibilityMatrix, pheromoneMatrix, alpha, beta, nextPossibleLocation, totalNumPlaces, visited)
    pathList.append(nextPossibleLocation)
    return pathList

def calculateDistance(distanceMatrix, pathList):
    distanceList = []
    for path in pathList:
        distance = 0
        for i in range(len(path)-1):
            source = path[i]
            destination = path[i+1]
            distance += distanceMatrix[source][destination]
        distanceList.append(distance)
    return distanceList
 
def evaporationRate_pheromoneMatUpdate(pheromoneMatrix, evaporationRate):
    evaporationFactor = 1-evaporationRate
    for i in range(pheromoneMatrix.shape[0]):
        for j in range(pheromoneMatrix.shape[1]):
            pheromoneMatrix[i][j] = pheromoneMatrix[i][j] * evaporationFactor
    return

def inverseDistance_pheromoneUpdate(pheromoneMatrix, distanceList, pathList):
    for i in range(len(distanceList)):
        inverseDistance = 1/distanceList[i]
        path = pathList[i]
        for j in range(len(path)-1):
            source = path[j]
            destination = path[j+1]
            pheromoneMatrix[source][destination] = pheromoneMatrix[source][destination] + inverseDistance
    return

def updatePheromoneMatrix(pheromoneMatrix, distanceList, pathList, evaporationRate):
    evaporationRate_pheromoneMatUpdate(pheromoneMatrix, evaporationRate)
    inverseDistance_pheromoneUpdate(pheromoneMatrix, distanceList, pathList)
    return

def populateAnts(distanceMatrix, visibilityMatrix, pheromoneMatrix, alpha, beta, population, generations, departure, totalNumPlaces, evaporationRate, logger):
    for gen in range(generations):
        pathInGeneration = []
        logger.info(f'GENERATION ==> {gen+1}')
        for ant in range(population):
            logger.info(f'ANT ==> {ant+1}')
            visited = 1
            visibilityMatrixDeepCopy = copy.deepcopy(visibilityMatrix)
            try:
                path = getPath(visibilityMatrixDeepCopy, pheromoneMatrix, alpha, beta, departure, totalNumPlaces, visited)
                path.append(departure)
                path.reverse()
                pathInGeneration.append(path)
                logger.debug(f'PATH : {path}')
            except Exception as e:
                logger.error(f'Exception Occured while finding Path\n ERROR ==> {e}')
                return
            
        try:
            distanceList = calculateDistance(distanceMatrix, pathInGeneration)
            updatePheromoneMatrix(pheromoneMatrix, distanceList, pathInGeneration, evaporationRate)
            logger.info(f'PHEROMONE MATRIX UPDATED SUCCESSFULLY!!!')
        except Exception as e:
            logger.error(f'Exception Occured While Updating Pheromone Matrix\n ERROR ==> {e}')        
    return