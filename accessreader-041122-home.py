import pyodbc


#THEN AFTER THIS ALL OF THE access database has then been turned into a google sheets
#pass the dataframe through, into uhh 


#test dataframe


import pygsheets
gc = pygsheets.authorize(
    service_file='C:/Users/andre/Downloads/fluent-outlet-329800-d7ce5f1f4cd1.json')
sh = gc.open('2022 Reliability Parts') #open the google spreadsheet
print(df)
wks = sh[1]

wks.set_dataframe(df, start=(1,1),copy_head=False)

