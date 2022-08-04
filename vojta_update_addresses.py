#CREATED BY VOJTA RIPA
#07-26-2022

#USE:
# given a CSV file, I use Samsaras API to loop through the CSV file and update addresses in the dashboard
#** will need to replace with VALID API token!!!


#import os
import pandas as pd
from tkinter import *
#import io
#import csv
import requests
#import urllib
#import json
from tkinter.filedialog import askopenfilename
import time

#Section 1: Allows to select a file
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename) #Section 2: Turns the CSV File into a readable table

#now working with the dataframe 
df = pd.read_csv(filename)
#df2 = df #.rename(str.lower, axis='columns')
df_data = pd.DataFrame(df) 



#LINK TO PAGE: https://developers.samsara.com/reference/updateaddress


'''
--- TEST EXAMPLE - PLEASE IGNOOR ---

3 test addresses:

#array of addresses
addressIDs = [36812505
,36812506
,36812507
]

    {
      "id": "36812505",
      "name": "Freightliner- GR",
      "createdAtTime": "2022-08-03T14:15:40.805884Z",
      "formattedAddress": "616 Trailmobile Trail SW  Wyoming MI 49548",
      "geofence": {
        "circle": {
          "latitude": 42.86949,
          "longitude": -85.67844,
          "radiusMeters": 75
        }
      },
      "latitude": 42.86949,
      "longitude": -85.67844
    },
    {
      "id": "36812506",
      "name": "Gas 17",
      "createdAtTime": "2022-08-03T14:15:40.815237Z",
      "formattedAddress": "15901 ELEVEN MILE ROAD  BATTLE CREEK MI 49014",
      "geofence": {
        "circle": {
          "latitude": 42.302591,
          "longitude": -85.082553,
          "radiusMeters": 250
        }
      },
      "latitude": 42.302591,
      "longitude": -85.082553
    },
    {
      "id": "36812507",
      "name": "Gas 83446",
      "createdAtTime": "2022-08-03T14:15:40.823729Z",
      "formattedAddress": "789 AMBOY AVENUE  EDISON NJ 8837",
      "geofence": {
        "circle": {
          "latitude": 40.53094,
          "longitude": -74.32557,
          "radiusMeters": 100
        }
      },
      "latitude": 40.53094,
      "longitude": -74.32557
    },
'''

#my function to modify address:
###############################
def modify_address(id,Address,	Name,	Latitude,	Longitude,	Radius,	Tags,	Notes,	Type, myIndex, start):
  currentTime = time.time()
  elapsed_time = currentTime - start
  print(str(myIndex)+". address id:"+str(id)+" (time -"+ str(elapsed_time)+")\n") 
  #Gets all addresses:
  url = "https://api.samsara.com/addresses/"+str(id)
  
  payload = {
    #"addressTypes": [Type],
    "geofence": {"circle": {"radiusMeters": 75}}, #Radius
    #"tagIds": [Tags],
    "name": str(Name),
    "formattedAddress": str(Address),
    "latitude": str(Latitude),
    "longitude": str(Longitude),
    "notes": str(Notes)
}

  headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "<INSERT API TOKEN HERE>"
    }

  response = requests.patch(url, json=payload, headers=headers)

  
  #Responses.. 
  print(response.text+"\n")
  
#NOW EXECUTE FOR EACH ADDRESS ID:
'''
OLD WAY:
while addressIDs:
    modify_address(addressIDs.pop())
'''  

#starting time
start = time.time()
#reseting index
df_data = df_data.reset_index()  # make sure indexes pair with number of rows

#loop:
for index, row in df_data.iterrows():
    #print(row['ID'], row['Address'], row['Name'], row['Latitude'],	row['Longitude'],	row['Radius'],	row['Tags'],	row['Notes'],	row['Type']
    modify_address(row['ID'], row['Address'], row['Name'], row['Latitude'],	row['Longitude'],	row['Radius'],	row['Tags'],	row['Notes'],	row['Type'],index,start)
end = time.time()
print("Total Elapsed time:"+str(end - start))


#I could also use API for both the input / PULL (via GET) and the PUSH but not if customer made other changes to the CSV File
