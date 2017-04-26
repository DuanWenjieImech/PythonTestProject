import json
jsonfile = open("part-00000.json", encoding='utf-8')
datafile = jsonfile.readlines()
jsonfile.close()

#PvP Data array
dataArray=[]
for line in datafile:
    tempresults = json.loads(line)
    dataArray.append(tempresults)

#PvP User ID array
UserIDArray=[]
for i in range(len(dataArray)):
    tempUID = dataArray[i]["competitor"]["objectId"]
    if tempUID not in UserIDArray:
        UserIDArray.append(tempUID)
    tempUID = dataArray[i]["player"]["objectId"]
    if tempUID not in UserIDArray:
        UserIDArray.append(tempUID)

#WinRate Array
WinRateArray=[]
for i in range(len(UserIDArray)):
    tempWinRate={"UserId":UserIDArray[i],"PvPResult":[0,0,"0.0"]}
    WinRateArray.append(tempWinRate)

#WinRate Calc
for i in range(len(dataArray)):
    UserID_A = dataArray[i]["competitor"]["objectId"]
    UserID_B = dataArray[i]["player"]["objectId"]
    UserIndex_A = UserIDArray.index(UserID_A)
    UserIndex_B = UserIDArray.index(UserID_B)
    #print(UserIndex_A,UserIndex_B)
    if (dataArray[i]["isPlayerWon"] == False):
        WinRateArray[UserIndex_A]["PvPResult"][0]+= 1
        WinRateArray[UserIndex_B]["PvPResult"][1]+= 1
    else:
        WinRateArray[UserIndex_A]["PvPResult"][1]+= 1
        WinRateArray[UserIndex_B]["PvPResult"][0]+= 1
    
for i in range(len(WinRateArray)):
    tempWinRate = float(WinRateArray[i]["PvPResult"][0]) / float( WinRateArray[i]["PvPResult"][0] + WinRateArray[i]["PvPResult"][1] )
    WinRateArray[i]["PvPResult"][2] = str(float(tempWinRate)*100) + "%"
    
print(WinRateArray)


    

