from logger import logd
from essentials import getParams, convertToNpArray, buildVisibilityMatrix, buildPheromoneMatrix
import argparse
from calculations import populateAnts
logger = logd()
def main():
    #Fetching data
    try:
        parser = argparse.ArgumentParser(description='Select the params/data from specs.json')
        parser.add_argument('-p', '--paramName', help='params/key name in specs.json file', const="exampleParam", nargs='?', required=False)
        args =  vars(parser.parse_args())
        paramName = args.get("paramName")
        data = getParams(paramName)
        logger.debug("Data Fetched Successfully!!!")
    except Exception as e:
        logger.error(f'Exception occured while fetching data from Specs.json \n ERROR==> {e}')
        return

    #Allocating data
    try:
        distanceMatrix = convertToNpArray(data["distanceMatrix"])
        visibilityMatrix = buildVisibilityMatrix(distanceMatrix)
        pheromoneMatrix = buildPheromoneMatrix(visibilityMatrix.shape)
        alpha = data["alpha"]
        beta = data["beta"]
        population = data["population"]
        generations = data["generations"]
        departure = data["departure"] - 1
        totalNumPlaces = distanceMatrix.shape[0]
        evaporationRate = data["evaporationRate"]
        logger.debug("Data Assigned to Variables Successfully!!!")
    except Exception as e:
        logger.error(f'Exception occured while assigning data to variables \n ERROR ==> {e}')
        return

    populateAnts(distanceMatrix, visibilityMatrix, pheromoneMatrix, alpha, beta, population, generations, departure, totalNumPlaces, evaporationRate, logger)

    return

main()