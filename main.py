import os.path
import tkinter as tk
import pickle

PMAXLV = 50
PBASICEFF = 10
PBASICSTA = 85
avEff = 0


class Worker():
    def __init__(self, curLv, maxLv, curEff, curSta):
        self.curLv = curLv
        self.maxLv = maxLv
        self.curEff = curEff
        self.curSta = curSta
        self.maxEff = 0
        self.maxSta = 0
        self.curIncome = 0
        self.maxIncome = 0
        self.curIncomeText = tk.StringVar()
        self.maxIncomeText = tk.StringVar()

        self.updateStat(curLv, maxLv, curEff, curSta)

    def updateStat(self, curLv=0, maxLv=0, curEff=0, curSta=0):
        #print("update working")
        self.curLv = curLv
        self.maxLv = maxLv
        self.curEff = curEff
        self.curSta = curSta
        self.calMaxStat()
        #print(f'eff={self.maxEff} sta={self.maxSta}')
        #print(f'cur {self.curEff}     {self.curSta}')
        self.calIncome()
        #print(f'income={self.maxIncome} cur={self.curIncome}')
        self.updateText()

    def calIncome(self):
        curFoodEff = self.curSta // 5
        self.curIncome = self.curEff * curFoodEff * 3.33
        maxFoodEff = self.maxSta // 5
        self.maxIncome = self.maxEff * maxFoodEff * 3.33

    def calMaxStat(self):
        deltaLv = self.maxLv - self.curLv
        if deltaLv <= 0:
            self.maxEff = self.curEff
            self.maxSta = self.curSta
            return
        self.maxEff = self.curEff + deltaLv
        self.maxSta = self.curSta + (deltaLv * 2)
        return

    def updateText(self):
        self.curIncomeText.set(f'Current Income/feed: {round(self.curIncome, 2)}')
        self.maxIncomeText.set(f'Max Income/feed: {round(self.maxIncome, 2)}')


    #etc ...

class TKWorkerInputFrame():
    def __init__(self, name):
        global root
        self.name = name
        self.curLv = tk.IntVar(master=root, value=0)
        self.maxLv = tk.IntVar(value=0)
        self.curEff = tk.IntVar(value=0)
        self.curSta = tk.IntVar(value=0)
        self.frame = tk.Frame(root, relief='solid', bd=2)
        tk.Label(self.frame, text=f'Worker #{self.name}').grid(row=0)
        tk.Label(self.frame, text='Current Lv:').grid(row=1, column=0)
        self.curLvEntry = tk.Entry(self.frame, textvariable=self.curLv, width=5)
        tk.Label(self.frame, text='Max Lv:').grid(row=1, column=2)
        self.maxLvEntry = tk.Entry(self.frame, textvariable=self.maxLv, width=5)
        tk.Label(self.frame, text='Efficiency:').grid(row=2, column=0)
        self.curEffEntry = tk.Entry(self.frame, textvariable=self.curEff, width=5)
        tk.Label(self.frame, text='Stamina:').grid(row=2, column=2)
        self.curStaEntry = tk.Entry(self.frame, textvariable=self.curSta, width=5)
        tk.Button(self.frame, text='▲', command=self.levelUpWorker).grid(row=0, column=1)
        tk.Button(self.frame, text='▼', command=self.levelDownWorker).grid(row=0, column=2)
        tk.Button(self.frame, text='X', command=self.retireWorker).grid(row=0, column=3)
        self.worker = Worker(self.curLv.get(), self.maxLv.get(), self.curEff.get(), self.curSta.get())

        '''
        workerLabel.grid(row=0, columnspan=5)
        curLvLabel.grid(row=1, column=0)
        '''
        self.curLvEntry.grid(row=1, column=1)
        self.maxLvEntry.grid(row=1, column=3)
        self.curEffEntry.grid(row=2, column=1)
        self.curStaEntry.grid(row=2, column=3)
        #testLabel.grid(row=3)

    def levelUpWorker(self):
        if self.curLv.get() < self.maxLv.get():
            self.curLv.set(self.curLv.get()+1)
            self.curEff.set(self.curEff.get()+1)
            self.curSta.set(self.curSta.get()+2)
            self.updateWorker()
            self.updateEntry()

    def levelDownWorker(self):
        if self.curLv.get() > 1:
            self.curLv.set(self.curLv.get()-1)
            self.curEff.set(self.curEff.get()-1)
            self.curSta.set(self.curSta.get()-2)
            self.updateWorker()
            self.updateEntry()

    def retireWorker(self):
        for i in range(self.name, len(inputFrameList)-1):
            print(f'retire:{i}')
            print(f'former cLv: {self.worker.curLv}')
            print(f'esti cLv: {inputFrameList[i+1].worker.curLv}')
            inputFrameList[i].curLv.set(inputFrameList[i + 1].curLv.get())
            inputFrameList[i].maxLv.set(inputFrameList[i + 1].maxLv.get())
            inputFrameList[i].curEff.set(inputFrameList[i + 1].curEff.get())
            inputFrameList[i].curSta.set(inputFrameList[i + 1].curSta.get())
            print(f'cur cLv: {self.worker.curLv}')
        inputFrameList[len(inputFrameList)-1].worker.updateStat()
        for i in range(len(inputFrameList)):
            inputFrameList[i].updateWorker()
            inputFrameList[i].updateEntry()
        updateOverallText()
        #refreshData()



    def updateWorker(self):
        self.worker.updateStat(self.curLv.get(), self.maxLv.get(), self.curEff.get(), self.curSta.get())

    def updateEntry(self):
        self.curLvEntry.delete(0, tk.END)
        self.curLvEntry.insert(0, str(self.worker.curLv))
        self.maxLvEntry.delete(0, tk.END)
        self.maxLvEntry.insert(0, str(self.worker.maxLv))
        self.curEffEntry.delete(0, tk.END)
        self.curEffEntry.insert(0, str(self.worker.curEff))
        self.curStaEntry.delete(0, tk.END)
        self.curStaEntry.insert(0, str(self.worker.curSta))

class TKWorkerOutputFrame():
    def __init__(self, name, worker):
        global root
        self.name = name
        self.maxEff = worker.maxEff
        self.worker = worker
        self.frame = tk.Frame(root, relief='solid', bd=2)
        maxStar = '★' if round(worker.maxIncome, 2) == round(MAXWORKER.maxIncome, 2) else ''
        print(maxStar)
        #print(f'cur: {round(worker.maxIncome, 2)}  max: {round(MAXWORKER.maxIncome, 2)}')
        self.workerLabel = tk.Label(self.frame, text=f'Worker #{self.name}{maxStar}')
        tk.Label(self.frame, textvariable=worker.curIncomeText).grid(row=1, column=0)
        tk.Label(self.frame, textvariable=worker.maxIncomeText).grid(row=2, column=0)
        self.workerLabel.grid(row=0, columnspan=5)

    def updateText(self):
        maxStar = '★' if round(self.worker.maxIncome, 2) == round(MAXWORKER.maxIncome, 2) else ''
        self.workerLabel.config(text=f'Worker #{self.name}{maxStar}')

def refreshData():
    for i in range(len(inputFrameList)):
        inputFrameList[i].updateWorker()
        outputFrameList[i].updateText()
    updateOverallText()
    return

def getAvgEff():
    curSum = 0
    maxSum = 0
    for i in range(len(inputFrameList)):
        curSum += inputFrameList[i].worker.curEff
        maxSum += inputFrameList[i].worker.maxEff
    curSum *= 10
    maxSum *= 10
    return (curSum, maxSum)

def getMaxMinWorker():
    incomeList = []
    maximum = 0
    maxInd = 0
    for i in range(len(inputFrameList)):
        incomeList.append(inputFrameList[i].worker.maxIncome)
    for i in range(len(incomeList)):
        if maximum <= incomeList[i]:
            maximum = incomeList[i]
            maxInd = i
    minimum = maximum
    minInd = 0
    for i in range(len(incomeList)):
        if minimum >= incomeList[i] and incomeList[i] != 0:
            minimum = incomeList[i]
            minInd = i
    return (maxInd, maximum, minInd, minimum)

def updateOverallText():
    global curAvgEffText
    global maxAvgEffText
    global maxWorkerText
    global minWorkerText
    income = getAvgEff()
    maxMinWorker = getMaxMinWorker()
    curAvgEffText.set(f'Current Average Efficiency: {income[0]}')
    maxAvgEffText.set(f'Max Average Efficiency: {income[1]}')
    maxWorkerText.set(f'Most Efficient Worker: {maxMinWorker[0]}, {round(maxMinWorker[1], 2)}')
    minWorkerText.set(f'Least Efficient Worker: {maxMinWorker[2]}, {round(maxMinWorker[3], 2)}')


def saveData():
    for i in range(len(currentWorkerList)):
        inputFrameList[i].updateWorker()
    with open('data.p', 'wb') as f:
        dataList = []
        for i in range(len(currentWorkerList)):
            print(f'save: cLv: {currentWorkerList[i].curLv} mLv: {currentWorkerList[i].maxLv} cEf: {currentWorkerList[i].curEff} cSt: {currentWorkerList[i].curSta}')
            data = [currentWorkerList[i].curLv, currentWorkerList[i].maxLv, currentWorkerList[i].curEff, currentWorkerList[i].curSta]
            dataList.append(data)
        pickle.dump(dataList, f)

def loadData():
    if os.path.isfile('data.p'):
        with open('data.p', 'rb') as f:
            dataList = pickle.load(f)
            for i in range(len(dataList)):
                currentWorkerList[i].updateStat(dataList[i][0], dataList[i][1], dataList[i][2], dataList[i][3])
                inputFrameList[i].updateEntry()
                print(f'loadRaw: cLv: {dataList[i][0]} mLv: {dataList[i][1]} cEf: {dataList[i][2]} cSt: {dataList[i][3]}')
                print(
                    f'load: cLv: {currentWorkerList[i].curLv} mLv: {currentWorkerList[i].maxLv} cEf: {currentWorkerList[i].curEff} cSt: {currentWorkerList[i].curSta}')
        refreshData()

root = tk.Tk()
MAXWORKER = Worker(1, PMAXLV, PBASICEFF, PBASICSTA)
#print(f"maxworker:{round(MAXWORKER.maxIncome, 2)}")
root.title('HoloCure Worker Calculator')
root.geometry("1000x500+100+100")
root.resizable(True, True)
currentWorkerList = []
inputFrameList = []
outputFrameList = []
curAvgEffText = tk.StringVar()
maxAvgEffText = tk.StringVar()
maxWorkerText = tk.StringVar()
minWorkerText = tk.StringVar()

for i in range(10):
    workerFrame = TKWorkerInputFrame(i+1)
    workerFrame.frame.grid(row=i % 5, column=2 + (i//5) * 2)
    currentWorkerList.append(workerFrame.worker)
    inputFrameList.append(workerFrame)
    outputFrame = TKWorkerOutputFrame(i+1, workerFrame.worker)
    outputFrame.frame.grid(row=i % 5, column=3 + (i//5) * 2)
    outputFrameList.append(outputFrame)

overallFrame = tk.Frame(root, relief='solid', bd=2)
tk.Label(overallFrame, text='-- Overall --').grid(row=0, columnspan=5)
tk.Label(overallFrame, textvariable=curAvgEffText).grid(row=1)
tk.Label(overallFrame, textvariable=maxAvgEffText).grid(row=2)
tk.Label(overallFrame, textvariable=maxWorkerText).grid(row=3)
tk.Label(overallFrame, textvariable=minWorkerText).grid(row=4)
updateOverallText()
overallFrame.grid(row=0, column=0)

button = tk.Button(root, text='Calculate', command=refreshData)
button.grid(row=0, column=1)
saveButton = tk.Button(root, text='Save', command=saveData)
saveButton.grid(row=1, column=0)
loadButton = tk.Button(root, text='Load', command=loadData)
loadButton.grid(row=1, column=1)

manualFrame = tk.Frame(root, relief='solid', bd=2)
tk.Label(manualFrame, text='▲: Level up Worker by 1.').grid(row=0)
tk.Label(manualFrame, text='▼: Level down Worker by 1.').grid(row=1)
tk.Label(manualFrame, text='X: Retire the worker.').grid(row=2)
manualFrame.grid(row=2, column=0)

root.mainloop()