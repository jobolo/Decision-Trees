from math import log
import operator

def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    lableCounts={}
    for featVec in dataSet:
        currentLable=featVec[-1]
        if currentLable not in lableCounts.keys():
            lableCounts[currentLable]=0
        lableCounts[currentLable]+=1
    shannonEnt=0.0
    for key in lableCounts:
        prob=float(lableCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt



def creatDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    lables=['no surfacing','flippers']
    return dataSet,lables



def splitDataSet(dataSet,axis,value):
	retDataSet=[]
	for featVec in dataSet:
		if featVec[axis]==value:
			reduceFeatVec= featVec[:axis]
			reduceFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reduceFeatVec)
	return retDataSet


def chooseBestFeatureSplit(dataSet):
	numFeatures=len(dataSet[0])-1
	baseEntropy=calcShannonEnt(dataSet)
	bestInfoGain=0.0;bestFeature=-1
	for i in range(numFeatures):
		#
		featList=[example[i] for example in dataSet]
		uniqueVals=set(featList)
		newEntropy=0.0
		for value in uniqueVals:
			subDataSet=splitDataSet(dataSet,i, value)
			prob=len(subDataSet)/float(len(dataSet))
			newEntropy+=prob*calcShannonEnt(subDataSet)
			infoGain=baseEntropy - newEntropy
			if(infoGain>bestInfoGain):
				bestInfoGain=infoGain
				bestFeature=i
	return bestFeature


def majorityCnt(classList):
	classCount={}
	for vote in classList:
		if vote not in classCount.key():
		classCount[vote]=0
		classCount[vote]+=1
	sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reversed=True)
	return sortedClassCount[0][0]


def creatTree(dataSet,lables):
	classList=[example[-1] for example in dataSet]
	if classList.count(classList[0])==len(classList):
		return classList[0]
	if len(dataSet[0])==1:
		return majorityCnt(classList)
	bestFeat=chooseBestFeatureSplit(dataSet)
	bestFeatLable=lables[bestFeat]
	myTree={bestFeatLable:{}}
	del(lables[bestFeat])
	featValues=[example[bestFeat] for example in dataSet]
	uniqueVals=set(featValues)
	for value in uniqueVals:
		subLables=lables[:]
		myTree[bestFeatLable][value]=creatTree(splitDataSet(dataSet,bestFeat,value),subLables)
	return myTree


	def classfy(inputTree,featLables,testVec):
		firstStr=inputTree.keys()[0]
		secondDict=inputTree[firstStr]
		featIndex=featLables.index(firstStr)
		for key in secondDict.keys():
			if testVec[featIndex]==key:
				if type(secondDict[key])._name_=='dict':
					classLable=classfy(secondDict[key],featLables,testVec)
				else:
					classLable=secondDict[key]
		return classLable