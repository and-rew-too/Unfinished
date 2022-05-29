from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
sheet_url = "https://docs.google.com/spreadsheets/d/1PzKvxN1ARlnQVYnCtM05Cs15VzTi76UHMyJmk6CQrNs/edit#gid=1738090655"
strcontain = "TC-100" #line 56, strcontains, this is what chooses the modules, make sure is commented with this
ReliabilityChamber = "Thermal Cycle" #Hast #Damp Heat #ALSO LINE 143, numbers are set to 50, 100, 200, 300, change to desired numbers

T1 = '200'
T2 = '150'
T3 = '100'
T4 = '50'

#############################################
#Projstr = 'VAL1'  # project ID
#projectboolean = df[~df['Batch_ID'].str.contains(Projstr)]
#df.drop(projectboolean.index, inplace=True)

pd.set_option('display.width', None)
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1)
print(df)
df = df.sort_values(by='Measurement_Date-Time', ascending=True)

#drops any poorly iv tested values, anything negative Voc etc
MindexNames = df[(df.iloc[:, 6] <= -0.1) | (
    df.iloc[:, 40] <= 0)].index
df.drop(MindexNames, inplace=True)

#large dataframe if comments row blank, is NaN, if filled is string df.iloc[:, 116]
df.iloc[:, 3] = df.iloc[:, 3].fillna('')
df.iloc[:, 116] = df.iloc[:, 116].fillna('')

#large dataframe, just adjusting sigfigs
for i in range(0, len(df.index)):
    b = df.iloc[i, 5]*100
    if b//1000 >= 1:
        c = 3
    elif b//100 >= 1:
        c = 2
    elif b//10 >= 1:
        c = 1
    else:
        c = 0
    df.iloc[i, 5] = df.iloc[i, 5].round(decimals=c)
for j in range(6, 9):
    df.iloc[:, j] = df.iloc[:, j].round(decimals=2)
for k in range(9, 12):
    df.iloc[:, k] = df.iloc[:, k].round(decimals=2)
for m in range(38, 41):
    df.iloc[:, m] = df.iloc[:, m].round(decimals=2)
pd.set_option('display.width', None)
print(df)


#large dataframe, only extract modules containing certain 'rel' comments
#groups the same 'rel' comments and 'Sample_ID' into adjacent rows
HASTboolean = df[df.iloc[:, 116].str.contains(strcontain)]
print(HASTboolean)
int_DH = []
for n in range(0, len(HASTboolean.index)):
    str = HASTboolean.iloc[n, 3]
    str = str[3:]
    #print(str)
    for o in range(0, len(df.index)):
        samples = df.iloc[o, 3]
        if samples.find(str) != -1:
            int_DH.append(df.iloc[o, :])
        else:
            pass
final_DH = pd.concat(int_DH, axis=1)
final_DH = final_DH.transpose()
print(final_DH)


# TRUNCATE DATAFRAME
workdf = final_DH.iloc[:, [0, 3, 116, 5, 6, 7, 8, 9, 10, 11, 39]]
print(workdf)


#comment this shit out of this one bro.. head scratcher forreal
#initialize new column that will be filled and loop through the length, start at second row and check row above,
# to see if it was that data was created at a later or earlier date
# if the iv data was created at a earlier date e.g. (df.i-1,0 < df.i,0)
# then data above is for the same part
# if true, then index the new column as the same part id
# if false, then create new index number, as a new part id
workdf.loc[:, 'partid,loop'] = 0
for o in range(1, len(workdf.index)):
    if workdf.iloc[o-1, 0].astype(int) < workdf.iloc[o, 0].astype(int):
        workdf.iloc[o, 11] = workdf.iloc[o-1, 11]
    else:
        workdf.iloc[o, 11] = o
print("truncated final_DH with partids column: {}".format(workdf))


# given the partid indexes, references the Isc Voc as control hours
# and calculates the percentage dropped when part got retested
workdf.loc[:, 'dIsc'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 3]
    workdf.iloc[i, 12] = (workdf.iloc[i, 3] - initvalue) / initvalue * 100
workdf.loc[:, 'dVoc'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 4]
    workdf.iloc[i, 13] = (workdf.iloc[i, 4]-initvalue) / initvalue * 100
workdf.loc[:, 'dVmp'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 5]
    workdf.iloc[i, 14] = (workdf.iloc[i, 5] - initvalue) / initvalue * 100
workdf.loc[:, 'dImp'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 6]
    workdf.iloc[i, 15] = (workdf.iloc[i, 6] - initvalue) / initvalue * 100
workdf.loc[:, 'dPmp'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 7]
    workdf.iloc[i, 16] = (workdf.iloc[i, 7] - initvalue) / initvalue * 100
workdf.loc[:, 'dFF'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 8]
    workdf.iloc[i, 17] = (workdf.iloc[i, 8] - initvalue) / initvalue * 100
workdf.loc[:, 'dEff'] = 0
for i in range(1, len(workdf.index)):
    index = workdf.iloc[i, 11]
    initvalue = workdf.iloc[index, 9]
    workdf.iloc[i, 18] = (workdf.iloc[i, 9] - initvalue) / initvalue * 100


#determines hours spent and uses that value as x-axis to plot, places into column 19
workdf["TimeSpent"] = 0
for p in range(0, len(workdf.index)):
    Sample = workdf.iloc[p, 2]
    if Sample.find(T1) != -1:
        workdf.iloc[p, 19] = int(T1)
    elif Sample.find(T2) != -1:
        workdf.iloc[p, 19] = int(T2)
    elif Sample.find(T3) != -1:
        workdf.iloc[p, 19] = int(T3)
    elif Sample.find(T4) != -1:
        workdf.iloc[p, 19] = int(T4)
    else:
        pass

      
#view final dataframe, and export to a csv file for further processing      
print(workdf)
workdf.to_csv(r'C:\Users\andre\Downloads\4-07-22lri-hast.csv')



