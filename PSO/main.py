from logger import logd
from esssentials import getParams
from calculations import optimizeParticles
import argparse

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

    #Allocating Data
    try:
        objectiveFunction = data['objectiveFunction']
        particlePositions = data['particlePositions']
        constant1 = data['constant1']
        constant2 = data['constant2']
        omegaW = data['omegaW']
        iterations = data['iterations']
        isMax = data['isMax']
        lowerBound = data['lowerBound']
        upperBound = data['upperBound']
        particleVelocties = [0 for i in range(len(particlePositions))]
        logger.info(f'Data Assigned to variables successfully!!!')
    except Exception as e:
        logger.error(f'Exception occured while allocating data to variables \n ERROR==> {e}')
        return

    optimizeParticles(particlePositions, particleVelocties, objectiveFunction, iterations, 
                                    omegaW, constant1, constant2, isMax, lowerBound, upperBound)

    return

main()