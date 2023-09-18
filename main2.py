def holocureMangerCal(eff, sta):
    foodEff = sta // 5
    result = eff * foodEff * 3.33
    return result

def holocureManagerGetMaxStat(curLevel, maxLevel, curEff, curSta):
    deltaLevel = maxLevel - curLevel
    if deltaLevel <= 0:
        return (curEff, curSta)
    maxEff = curEff + deltaLevel
    maxSta = curSta + (deltaLevel * 2)
    return (maxEff, maxSta)

def holocureMangerListCal(arr):
    print("\n----The Most/Least Efficient Worker----")
    resultArr = []
    effSum = 0
    for i in range(len(arr)):
        maxStat = holocureManagerGetMaxStat(arr[i][0], arr[i][1], arr[i][2], arr[i][3])
        eff = holocureMangerCal(maxStat[0], maxStat[1])
        effSum += maxStat[0]
        resultArr.append(eff)
    #print(resultArr)
    #print(effSum)
    maximal = 0
    maxNum = 0
    for i in range(len(resultArr)):
        if resultArr[i] >= maximal:
            maximal = resultArr[i]
            maxNum = i
    minimal = maximal
    minNum = 0
    for i in range(len(resultArr)):
        if resultArr[i] <= minimal:
            minimal = resultArr[i]
            minNum = i
    incomePerMin = effSum * 10
    print("maximal: ", maxNum+1, ", value: ", maximal)
    print("minimal: ", minNum+1, ", value: ", minimal)
    print("average income per minutes: ", incomePerMin)
    return

def holocureManagerListShow(arr):
    print("\n----Worker Efficiency List----")
    resultArr = []
    maxArr = []
    pMax = getPossibleMaxStat()
    global avEff
    for i in range(len(arr)):
        maxStat = holocureManagerGetMaxStat(arr[i][0], arr[i][1], arr[i][2], arr[i][3])
        eff = holocureMangerCal(maxStat[0], maxStat[1])
        maxArr.append(maxStat)
        resultArr.append(eff)
        avEff += eff
    avEff /= len(resultArr)
    print("number\tincome\tstamina\tincome/feed")
    for i in range(len(resultArr)):
        print(f"{i+1}\t\t{maxArr[i][0]}\t\t{maxArr[i][1]}\t\t{resultArr[i]} (curL:{arr[i][0]}, curS:{arr[i][3]})",
              "★" if resultArr[i] == pMax[4] else "")

def holocureMangerHirePotenCal(arr):
    pMax = getPossibleMaxStat()
    print("\n----Hire Worker Potency----")
    print("\n--Notice: Possible Max Stat(Currently Known, May be changed later.)--")
    print(f"Max Level Possible: {pMax[0]}"
          f"\nMax Basic Efficiency Stat: {pMax[1]}"
          f"\nMax Basic Stamina Stat: {pMax[2]}")
    print(f"Possible Most Efficient Worker: {pMax[4]} (Eff: {pMax[3][0]}, Sta: {pMax[3][1]})")
    print(f"Current Average Efficient: {avEff}")
    result = []
    maxArr = []
    for i in range(len(arr)):
        maxStat = holocureManagerGetMaxStat(1, arr[i][0], arr[i][1], arr[i][2])
        eff = holocureMangerCal(maxStat[0], maxStat[1])
        maxArr.append(maxStat)
        result.append(eff)
    #print(result)
    print("\nnumber\tincome\tstamina\tincome/feed")
    for i in range(len(result)):
        print(f"{i + 1}\t\t{maxArr[i][0]}\t\t{maxArr[i][1]}\t\t{result[i]} (curE:{arr[i][1]}, curS:{arr[i][2]})")
    maximal = 0
    maxNum = 0
    for i in range(len(result)):
        if result[i] >= maximal:
            maximal = result[i]
            maxNum = i
    print("maximal: ", maxNum+1, ", value: ", maximal)
    return

def getPossibleMaxStat():
    possibleMaxStat = holocureManagerGetMaxStat(1, PMAXLV, PBASICEFF, PBASICSTA)
    possibleMaxWorker = holocureMangerCal(possibleMaxStat[0], possibleMaxStat[1])
    return (PMAXLV, PBASICEFF, PBASICSTA, possibleMaxStat, possibleMaxWorker)

PMAXLV = 50
PBASICEFF = 10
PBASICSTA = 85
avEff = 0

workerArr = [(2, 48, 8, 73), (1, 46, 7, 79), (1, 49, 10, 59), (1, 49, 10, 83),
             (1, 47, 10, 79), (1, 49, 8, 75), (1, 46, 10, 83), (1, 47, 9, 83), (1, 50, 9, 83), (1, 50, 10, 85)]
hireArr = [(50, 9, 83)]
holocureManagerListShow(workerArr)
holocureMangerListCal(workerArr)
holocureMangerHirePotenCal(hireArr)