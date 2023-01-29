from random import random
def getObjectiveFunctionValues(objectiveFunction, particlePositionsList):
    objectiveFuncValuesList = []
    for particlePosition in particlePositionsList:
        ObjFuncValue = eval(objectiveFunction, {"x": particlePosition})
        objectiveFuncValuesList.append(ObjFuncValue)
    return objectiveFuncValuesList

def getGBestPositionAndValue(pBestParticles_positions, pBestParticles_funcValues, isMax):
    bestValue = max(pBestParticles_funcValues) if isMax else min(pBestParticles_funcValues)
    bestPosition = pBestParticles_positions[pBestParticles_funcValues.index(bestValue)]
    return bestPosition, bestValue

def velocityUpdate(particleVelocities,particlePositions, pBestParticles_positions, omegaW, 
                            constant1, random1, constant2, random2, gBestParticlePosition):
    updatedVelocities = []
    for i in range(len(particleVelocities)):
        velocity = particleVelocities[i]
        currentParticlePosition = particlePositions[i]
        inertiaComponent = velocity*omegaW
        cognitiveComponent = constant1*random1*(pBestParticles_positions[i] - currentParticlePosition)
        socialComponent = constant2*random2*(gBestParticlePosition - currentParticlePosition)
        newVelocity = inertiaComponent + cognitiveComponent + socialComponent
        updatedVelocities.append(newVelocity)
    return updatedVelocities

def positionUpdate(particleVelocities, particlePositions):
    updatedPositions = []
    for individualParticlePostion, individualParticleVelocity in zip(particlePositions, particleVelocities):
        newPosition = individualParticlePostion + individualParticleVelocity
        updatedPositions.append(newPosition)
    return updatedPositions

def checkIfBest(isMax, val1, val2):
    if isMax:
        return True if val1 >= val2 else False
    else:
        return True if val1 <= val2 else False


def getPBestPositions(currentParticle_objFuncvalues, pBestParticles_funcValues, particlePositions, pBestParticles_positions, isMax):
    for i in range(len(particlePositions)):
        currentVal = currentParticle_objFuncvalues[i]
        bestVal = pBestParticles_funcValues[i]
        currentPosition = particlePositions[i]
        if checkIfBest(isMax, currentVal, bestVal):
            pBestParticles_funcValues[i] = currentVal
            pBestParticles_positions[i] = currentPosition
    return pBestParticles_positions, pBestParticles_funcValues

def velocityBoundCorrection(particleVelocities, lowerBound, upperBound):
    particleVelocities = [lowerBound if velocity <= lowerBound else upperBound if velocity >= upperBound else velocity for velocity in particleVelocities]
    return particleVelocities

def optimizeParticles(particlePositions, particleVelocities, objectiveFunction, iterations, omegaW, 
                                                    constant1, constant2, isMax, lowerBound, upperBound):
    # random1_list = [0.213, 0.113, 0.178]
    # random2_list = [0.876, 0.706, 0.507]
    for batch in range(iterations):
        if batch == 0:
            pBestParticles_positions = particlePositions
            pBestParticles_funcValues = getObjectiveFunctionValues(objectiveFunction, pBestParticles_positions)
        else:
            pBestParticles_positions,  pBestParticles_funcValues = getPBestPositions(currentParticle_objFuncvalues, pBestParticles_funcValues, 
                                                                particlePositions, pBestParticles_positions, isMax)

        gBestParticlePosition, gBestParticleFuncValue = getGBestPositionAndValue(pBestParticles_positions, pBestParticles_funcValues, isMax)
        random1 = random()
        random2 = random()
        # random1 = random1_list[batch]
        # random2 = random2_list[batch]
        particleVelocities = velocityUpdate(particleVelocities, particlePositions, pBestParticles_positions, 
                                                omegaW, constant1, random1, constant2, random2, gBestParticlePosition)
        particleVelocities = velocityBoundCorrection(particleVelocities, lowerBound, upperBound)
        particlePositions = positionUpdate(particleVelocities, particlePositions)
        currentParticle_objFuncvalues = getObjectiveFunctionValues(objectiveFunction, particlePositions)
        print(f'At iteration ==> {batch} \n {particlePositions}')

    return