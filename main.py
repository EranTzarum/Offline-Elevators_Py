import subprocess
import sys
import json
import csv
from Elevator import Elevator
from Call import Call



"this function initializes the array in second from source floor to maxFloor in up mode"
"so if the elevator took a given call we will know now the elevator floor/time in any given time/floor"
def up(call, i):
    if float(call.time) != elevators[i].arrfloose[int(call.source)-elevators[i].minFloor]:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].stopTime + elevators[i].openTime + elevators[i].closeTime + elevators[i].startTime + (float(call.time) - elevators[i].arrfloose[int(call.source)-elevators[i].minFloor])
    else:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].closeTime + elevators[i].openTime + elevators[i].startTime
    for j in range(int(call.source)-elevators[i].minFloor, (elevators[i].maxFloor-elevators[i].minFloor)):
        if j == int(call.destination) - elevators[i].minFloor:
            elevators[i].arrfloose[j] = elevators[i].arrfloose[j - 1] + elevators[i].stopTime + elevators[i].openTime + elevators[i].closeTime
        elevators[i].arrfloose[j + 1] = elevators[i].arrfloose[j] + elevators[i].spf



"this function initializes the array in seconds from source floor to minFloor in down mode"
"so if the elevator took a given call we will know now the elevator floor/time in any given time/floor until the elevator will arrive to her destination"
def dowm(call, i):
    if float(call.time) != elevators[i].arrfloose[int(call.source)-elevators[i].minFloor]:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].stopTime + elevators[i].openTime + elevators[i].closeTime + elevators[i].startTime + (float(call.time) - elevators[i].arrfloose[int(call.source)-elevators[i].minFloor])
    else:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].closeTime + elevators[i].openTime + elevators[i].startTime
    for j in range(int(call.source)-elevators[i].minFloor, 0):
        if j == int(call.destination) - elevators[i].minFloor:
            elevators[i].arrfloose[j] = elevators[i].arrfloose[j + 1] + elevators[i].stopTime + elevators[i].openTime + elevators[i].closeTime
        elevators[i].arrfloose[j - 1] = elevators[i].arrfloose[j] + elevators[i].spf


def nearsource(call):
    mintime = float(call.time) - elevators[0].arrfloose[0]
    maxcallsQueue = 5
    minindex = 0
    prevminindex = 0
    if (len(elevators) == 2 and abs(maxFloor - minFloor) > 80):
        allocateElevatorFor2Elevators(call)
        return
    "check if the elevator is going to source direction (up or down) so we will know if its worth to this elevator to take the call"
    if int(call.source) < int(call.destination):
        "we want to go over all elevators to see which one closer to call.source be given call.time and compering it to e[i].arrfloose[correnfloor]"
        for i in range(len(elevators)):
            prevminindex = minindex
            temp = float(call.time) - elevators[i].arrfloose[(int(call.source) - elevators[i].minFloor)]
            if temp >= 0 and temp <= mintime:
                if len(elevators[i].callsQueue) < (maxcallsQueue * elevators[i].speed):
                    if elevators[i].mood == 1 or elevators[i].mood == 2:
                        minindex = i
                        if temp > float(call.time) - elevators[prevminindex].arrfloose[
                            (int(call.source) - elevators[prevminindex].minFloor)] and len(
                                elevators[i].callsQueue) > len(elevators[prevminindex].callsQueue):
                            minindex = prevminindex
                else:
                    minindex = callQ(i)
        up(call, minindex)
        "after elevator took a call we need to update her mood"
        elevatormood(call, minindex)
    else:
        for i in range(len(elevators)):
            prevminindex = minindex
            temp = float(call.time) - float(elevators[i].arrfloose[int(call.source) - elevators[i].minFloor])
            if temp >= 0 and temp <= mintime:
                if len(elevators[i].callsQueue) < (maxcallsQueue * elevators[i].speed):
                    if elevators[i].mood == 0 or elevators[i].mood == 2:
                        minindex = i
                        if temp > float(call.time) - elevators[prevminindex].arrfloose[
                            (int(call.source) - elevators[prevminindex].minFloor)] and len(
                                elevators[i].callsQueue) > len(elevators[prevminindex].callsQueue):
                            minindex = prevminindex
                else:
                    minindex = callQ(i)
        dowm(call, minindex)
        elevatormood(call, minindex)

    call.allocatedElevator = minindex
    elevators[minindex].callsQueue.append(call)
    elevatormood2(call, minindex)
    clear(call)



def allocateElevatorFor2Elevators(call):
    fastElevatorIndex = 0
    slowElevatorIndex = 1
    if (float(elevators[0].speed) > float(elevators[1].speed)):
        fastElevatorIndex = 1
        slowElevatorIndex = 0
    floorsCount = maxFloor - minFloor

    if (float(call.destination) < float(floorsCount) / 3):
        call.allocatedElevator = slowElevatorIndex
    else:
        call.allocatedElevator = fastElevatorIndex



"this function it to check which elevators heve mincalls in callsQueue"
def callQ(i):
    minQ = len(elevators[0].callsQueue)
    minindex = 0
    for j in range(len(elevators)):
        if len(elevators[j].callsQueue) <= minQ:
            minindex = i
    return minindex



def elevatormood(call,i):
        if int(call.source) < int(call.destination):
            elevators[i].mood = 1
        else:
            elevators[i].mood = 0


def elevatormood2(call,i):
    if float(call.time) > elevators[i].arrfloose[(int(elevators[i].callsQueue[(len(elevators[i].callsQueue)-1)].destination))-elevators[i].minFloor]:
        elevators[i].mood == 2



def clear(call):
    for e in elevators:
        e.clearCompleteCalls(call)





"sys.argv is a function that gets the input from the terminal and puts its in an array"
"buildint will be the string that represent building.json location that we want to use for input"
"calls will be the string that represent calls.csv location that we want to use for input"
"output will be the string that represent outPut.csv location that we want to use fo output"
list = sys.argv
building = list[1]
calls = list[2]
output = list[3]

"we will read building.json file and will get the necessary input to our own variables"
with open(building) as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)

"now we have our building.json file int obj variable and gets from it minFloor maxFloor and elevators"
minFloor = obj['_minFloor']
maxFloor = obj['_maxFloor']

"elevators is array that contains all the elevators in the building"
"callsArr is an array that contains all the calls that we gets as input"
"arrfloose is an array that tells us where are the elevators at any given second .... hopefully"
elevators = []
callsArr = []



"init elevators"
for i in range(0, len(obj['_elevators'])):
    id = obj['_elevators'][i]['_id']
    speed = obj['_elevators'][i]['_speed']
    minFloor = obj['_elevators'][i]['_minFloor']
    maxFloor = obj['_elevators'][i]['_maxFloor']
    closeTime = obj['_elevators'][i]['_closeTime']
    openTime = obj['_elevators'][i]['_openTime']
    startTime = obj['_elevators'][i]['_startTime']
    stopTime = obj['_elevators'][i]['_stopTime']
    spf = float((obj['_elevators'][i]['_speed']*(obj['_elevators'][i]['_maxFloor']
-obj['_elevators'][i]['_minFloor']))-obj['_elevators'][i]['_startTime']
-obj['_elevators'][i]['_stopTime']-obj['_elevators'][i]['_openTime']
-obj['_elevators'][i]['_closeTime'])/(obj['_elevators'][i]['_maxFloor']
-obj['_elevators'][i]['_minFloor'])
    " stf = ((speed*(maxFloor-minFloor))-startTime-stopTime-openTime-closeTime)/(maxFloor-minFloor)"
    "???????????????20"
    mood = 2
    e = Elevator(id, speed, minFloor, maxFloor, closeTime, openTime, startTime, stopTime,spf,mood)
    elevators.append(e)

    # spf = ((e.speed*(e.maxFloor-e.minFloor))-e.startTime-e.stopTime-e.openTime-e.closeTime)/(e.maxFloor-e.minFloor)

    for j in range(0 ,((obj['_elevators'][i]['_maxFloor']-obj['_elevators'][i]['_minFloor']))+1):
        elevators[i].arrfloose.append((elevators[i].spf)*j)



"init calls"
with open(calls) as f:
    reader = csv.reader(f)
    for row in reader:
        call = Call(row[1], row[2], row[3], row[4])
        callsArr.append(call)

"row[4] represant allocated elevator"
"we will want to edit row[4] in our output file with the given call as input for allocatedElevator function"
for i in callsArr:
    nearsource(i)

inputData = []
for i in callsArr:
    tempArr = ["Elevator Call", i.time, i.source, i.destination, 3, i.allocatedElevator, " Done", " dt",
               " 164.5625272709607"]
    inputData.append(tempArr)

"write data in the new output.csv file"
with open(output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(inputData)

subprocess.Popen(["powershell.exe",
                  "java -jar Ex1_checker_V1.2_obf.jar 1111,2222,3333 " + list[1] + " " + list[3] + " out.log"])
"GUI"
# root = Tk()
# C = Canvas(root, bg="yellow", height=600, width=400)
# C.create_rectangle(20, 20, 380, 470)
# numbersOfFloors = abs(minFloor - maxFloor)
# deltaFloor = 500 / numbersOfFloors
# deltaElevators = 360 / len(elevators)
# for i in range(0, numbersOfFloors):
#    C.create_line(20, 20 + deltaFloor * i, 380, 20 + deltaFloor * i)
# for i in range(0, len(elevators)):
#    C.create_line(20 + deltaElevators * i, 20, 20 + deltaElevators * i, 470)

# C.pack()
# mainloop()
