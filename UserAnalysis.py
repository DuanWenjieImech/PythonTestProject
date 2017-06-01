import json
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def PrintListOneByOne(tempList):
    print(len(tempList))
    for i in range(len(tempList)):
        print(tempList[i])
        input()

#Read User Data File
jsonfile = open("UserData.json", encoding='utf-8')
datafile = jsonfile.readlines()
jsonfile.close()

#User Data Array
UserDataArray=[]
for line in datafile:
    tempresults = json.loads(line)
    UserDataArray.append(tempresults)

#PrintListOneByOne(UserDataArray)

UserDataFrame = pd.DataFrame(UserDataArray)

UserRegDataFrame = UserDataFrame.loc[:,["createdAt","objectId"]]

for i in range(len(UserRegDataFrame)):
    TempTime = UserRegDataFrame[i:i+1]["createdAt"]
    TempTimeInFormat = TempTime[i].split("T")[0]+ " " + (TempTime[i].split("T")[1]).split(".")[0]
    TempTimeInFormat = datetime.datetime.strptime(TempTimeInFormat,"%Y-%m-%d %H:%M:%S")
    UserRegDataFrame.at[i,"createdAt"] = TempTimeInFormat
    
UserRegDataFrame.sort_values(by="createdAt")

#Part the User list into 10 parts by reg time
MinTime = int(time.mktime(UserRegDataFrame.at[0,"createdAt"].timetuple()))
MaxTime = int(time.mktime(UserRegDataFrame.at[len(UserRegDataFrame)-1,"createdAt"].timetuple())) + 1

TimeRange = []
TimePart = 20;
for i in range(TimePart + 1):
    TimeRange.append( datetime.datetime.fromtimestamp( MinTime + (MaxTime - MinTime) / TimePart * i) )

UserRegTimeList = []
for i in range(TimePart):
    UserRegTimeList.append( len(UserRegDataFrame[(UserRegDataFrame["createdAt"]>=TimeRange[i]) & (UserRegDataFrame["createdAt"]<TimeRange[i+1])]) )

UserRegTimeList.append(0);    

UserRegTime = pd.DataFrame({"CreateTime":pd.Series(TimeRange),"Number of Registed User":pd.Series(UserRegTimeList)})

#Draw a figure of User reg time
plt.figure(1)
plt.plot(UserRegTime.loc[:,"CreateTime"],UserRegTime.loc[:,"Number of Registed User"])
plt.show()

    


