import numpy as np
import itertools

minsup = 490
def getTransactions(fileName):
    file = open(fileName, "r")
    data = file.read().splitlines()
    file.close()
    return data

def getF1Itemsets(minsup,transactions):
    f1Itemsets = np.empty([0, 2], object)
    prunedf1Itemsets = np.empty([0, 2], object)
    # iterate all transactions, count each movie's support and save in numpy array.
    # example of an element in the array : ['A Star Is Born' '1013']
    for transaction in transactions:
        for movie in transaction.split(";"):
            if movie not in f1Itemsets:
                f1Itemsets = np.append(f1Itemsets, np.array([[movie, 1]]), axis=0)
            else:
                arr = np.where(f1Itemsets == movie)
                f1Itemsets[arr[0][0]][1] = int(f1Itemsets[arr[0][0]][1]) + 1

    #remove infrequent items
    for movie, support in f1Itemsets:
        if(int(support) >= minsup):
            prunedf1Itemsets = np.append(prunedf1Itemsets, np.array([[movie,support]]), axis=0)

    # sort itemsets lexicographically
    prunedf1Itemsets = prunedf1Itemsets[np.lexsort(np.rot90(prunedf1Itemsets))]
    return prunedf1Itemsets


#part a
transactions = getTransactions("movies.txt")
f1Itemsets = getF1Itemsets(minsup, transactions)
#output frequent-1 itemsets
file = open("oneItems.txt", "w+")
for movie, support in f1Itemsets:
    file.write(str(support) + ":" + movie + "\n")

def generateCandidates(frequentItemsets,k):
    # candidates array is created with k+1 columns, where the last column is for the support count to use later
    # example of an element in the array: ['A Star Is Born' 'Alita: Battle Angel' 0]
    candidates = np.empty([0, k+1], object)
    rowCount = frequentItemsets.shape[0]
    for i in range(0, rowCount - 1):
        for j in range(i + 1, rowCount):
            if (frequentItemsets[i][:k - 2] == frequentItemsets[j][:k - 2]).all():
                length = len(frequentItemsets[i]) - 1
                mergedArray = np.concatenate((frequentItemsets[i][:length], frequentItemsets[j][:length]))
                mergedArray = np.unique(mergedArray)
                mergedArray = np.append(mergedArray, 0)
                candidates = np.append(candidates, np.array([mergedArray]), axis=0)
    return candidates;

def pruneCandidates(candidates,transactions,minsup):
    rowCount = candidates.shape[0]
    colCount = candidates.shape[1]
    frequentItemset = np.empty([0, colCount], object)

    for transaction in transactions:
        transactionArr = transaction.split(";")
        for i in range(0, rowCount):
            isFoundInTransaction=True;
            for j in range(colCount-1):
                if(candidates[i][j] not in transactionArr):
                    isFoundInTransaction = False
                    break
            if isFoundInTransaction:
                candidates[i][colCount-1] = int(candidates[i][colCount-1])+1

    for candidate in candidates:
        if(int(candidate[colCount-1]) >= minsup):
            frequentItemset = np.append(frequentItemset, np.array([candidate]), axis=0)
    return frequentItemset

def generateFrequentItemsets(transactions, minsup):
    setList = []
    k =1
    frequentSet = getF1Itemsets(minsup, transactions)
    frequentItemsetsExist = True

    while frequentItemsetsExist:
        setList.append([list(i) for i in frequentSet])
        k += 1
        candidates = generateCandidates(frequentSet, k)
        frequentSet = pruneCandidates(candidates, transactions, minsup)
        if frequentSet.shape[0] == 0:
            frequentItemsetsExist = False

    return setList

sets = generateFrequentItemsets(transactions, 490)

def outputItemsets(itemset, fileName, mode):
    file = open(fileName, mode)
    line = str(itemset[len(itemset)-1]) + ":"
    for i in range(0, len(itemset)-1):
        line += itemset[i]
        if(i!=len(itemset)-2):
            line += ";"
    file.write(line + "\n")

# part b
open("patterns.txt", 'w').close()
for kSet in sets:
    for itemset in kSet:
        outputItemsets(itemset, "patterns.txt", "a")

def getMovieRecommendation(movieList,sets):
    support = 0
    recSupport = 0
    recItemset = 0
    recMovie=''
    for kSet in sets:
        for itemset in kSet:

            # get movieList support count
            if itemset[0:len(itemset)-1]==movieList:
                support = itemset[len(itemset)-1]
            #
            if len(itemset)==len(movieList)+2:
                itemsetContainsMovieList = False
                possibleRecMovie = ''
                for movie in movieList:
                    itemsetContainsMovieList = False
                    for item in itemset:
                        if movie == item:
                            itemsetContainsMovieList = True
                            break
                        else:
                            possibleRecMovie = item
                    if not(itemsetContainsMovieList):
                        break
                if itemsetContainsMovieList:
                    if itemset[len(itemset)-1] > recSupport:
                        recSupport = int(itemset[len(itemset)-1])
                        recItemset = itemset
                        recMovie = possibleRecMovie

    confidence = recSupport / support
    return recItemset, recMovie, confidence

rec1, recmov, conf = getMovieRecommendation(["Guardians of the Galaxy", "Spider-Man: No Way Home"], sets)
print(f"Recommended movie: {recmov}, Confidence: {conf}")






































