import json

def PrintListOneByOne(tempList):
    for i in range(len(tempList)):
        print(tempList[i])
        input()

#Read PvP Data File
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
    
#PrintListOneByOne(WinRateArray)

#Read PvP AI File
jsonfile = open("part-00001.json", encoding='utf-8')
datafile = jsonfile.readlines()
jsonfile.close()

AIDataArray=[]
for line in datafile:
    tempresults = json.loads(line)
    AIDataArray.append(tempresults)

#Match AI with userId
jsonfile = open("part-00002.json", encoding='utf-8')
datafile = jsonfile.readlines()
jsonfile.close()

TeamDataArray=[]
for line in datafile:
    tempresults = json.loads(line)
    TeamDataArray.append(tempresults)

UserAIArray=[]
for i in range(len(UserIDArray)):
    AIListGroup=[];
    tempUserAI={"UserId":UserIDArray[i],"AIList":AIListGroup,"PvPResult":WinRateArray[i]["PvPResult"]}
    UserAIArray.append(tempUserAI)

for i in range(len(AIDataArray)):
    tempTeamId = AIDataArray[i]["team"]["objectId"]
    tempAIUserId=""
    for j in range(len(TeamDataArray)):
        if (TeamDataArray[j]["objectId"] == tempTeamId):
            tempAIUserId = TeamDataArray[j]["player"]["objectId"]
    #PrintListOneByOne(tempAIUserId)
    if tempAIUserId in UserIDArray:
        tempUserIter = UserIDArray.index(tempAIUserId)
        UserAIArray[tempUserIter]["AIList"].append(AIDataArray[i])

#PrintListOneByOne(UserAIArray)

#Sort AI with Win Rate
RealUserAIArray=[]
for i in range(len(UserAIArray)):
    if ( len(UserAIArray[i]["AIList"]) != 0 ):
        RealUserAIArray.append(UserAIArray[i])

RealUserAIArray.sort(key=lambda d: float(d["PvPResult"][2].split("%")[0]),reverse=True)

#PrintListOneByOne(RealUserAIArray)

#Remove data which has less than 5 matches
RealUsefulUserAIArray=[]
for i in range(len(RealUserAIArray)):
    if ( RealUserAIArray[i]["PvPResult"][0] + RealUserAIArray[i]["PvPResult"][1] >= 5 ):
       RealUsefulUserAIArray.append(RealUserAIArray[i]);

#PrintListOneByOne(RealUsefulUserAIArray)
