import json
def getParams(param):
    if param == None:
        param = "exampleParam"
    with open('./specs.json') as paramFile:
        setOfParams = json.load(paramFile)
    data = setOfParams[param]
    return data
