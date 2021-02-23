# Data Mining Team #1 Project 1
# Gavin Epperson & Braydon Fort
# Spring 2021, Chen 
# This Project implements the Naive Bayes Classifier on a Wineinformatics testing (and training) dataset

import xlrd
import os

def main():
    # Location of file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # To open Workbook
    trainingWB = xlrd.open_workbook(dir_path + "\\Training dataset.xlsx")
    trainingSheet = trainingWB.sheet_by_index(0)

    testingWB = xlrd.open_workbook(dir_path + "\\Testing dataset.xlsx")
    testingSheet = testingWB.sheet_by_index(0)

    ninetyPlusTotals = [0] * trainingSheet.ncols
    ninetyMinusTotals = [0] *trainingSheet.ncols

    # Training Data
    for i in range(1, trainingSheet.nrows):
        curRow = trainingSheet.row_values(i)
        if (curRow[1] == 1.0):
            tempArr = [ninetyPlusTotals[j]+curRow[j] for j in range(1,len(ninetyPlusTotals))]
            tempArr.insert(0,0)
            ninetyPlusTotals = tempArr
        elif (curRow[1] == 0.0):
            tempArr = [ninetyMinusTotals[j]+curRow[j] for j in range(1,len(ninetyMinusTotals))]
            tempArr.insert(0,0)
            ninetyMinusTotals = tempArr

    # Basic calculations to be used in prediction
    numDataRows = trainingSheet.nrows - 1
    totalNinetyPlus = ninetyPlusTotals[1]
    totalNinetyMinus = (numDataRows-ninetyPlusTotals[1])

    ninetyPlusProb = totalNinetyPlus/numDataRows
    ninetyMinusProb = totalNinetyMinus/numDataRows

    predictions = [None] * (testingSheet.nrows)

    # Testing Data
    # Predict each wine (row)
    for i in range (1, testingSheet.nrows):
        curRow = testingSheet.row_values(i)
        
        nPlusDataProb = [0] * trainingSheet.ncols
        nMinusDataProb = [0] * trainingSheet.ncols

        # Act differently depending on if current data is 0 or 1
        # Use Laplace smoothing (+1 in numerator, +2 in denominator)
        for j in range(2,len(curRow)):
            if curRow[j] == 1.0:
                nPlusDataProb[j] = (ninetyPlusTotals[j]+1)/(totalNinetyPlus+2)
                nMinusDataProb[j] = (ninetyMinusTotals[j]+1)/(totalNinetyMinus+2)
            elif curRow[j] == 0.0:
                nPlusDataProb[j] = (totalNinetyPlus-ninetyPlusTotals[j]+1)/(totalNinetyPlus+2)
                nMinusDataProb[j] = (totalNinetyMinus-ninetyMinusTotals[j]+1)/(totalNinetyMinus+2)
        
        # Multiply all 90+ data and all 90- data
        nPlusProduct = 1
        nMinusProduct = 1
        for j in range(2,len(nPlusDataProb)):
            nPlusProduct *= nPlusDataProb[j]
        for j in range(2,len(nMinusDataProb)):
            nMinusProduct *= nMinusDataProb[j]
        
        nPlusResult = nPlusProduct * ninetyPlusProb
        nMinusResult = nMinusProduct * ninetyMinusProb

        # Predict result
        if (nPlusResult > nMinusResult):
            predictions[i] = 1.0
        else:
            predictions[i] = 0.0

    # Compare predictions with real values
    totalCorrect = 0
    for i in range(1, len(predictions)):
        if (testingSheet.cell_value(i,1) == predictions[i]):
            totalCorrect += 1
            print(predictions[i], True)
        else:
            print(predictions[i], False)
    accuracy = totalCorrect/(testingSheet.nrows-1)
    print("Accuracy:", accuracy)

if __name__ == "__main__":
    main()