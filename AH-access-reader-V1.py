from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
# ensure that the input format for date is placed in descending order, oldest top
#only 3 variables to change
sheet_url = "https://docs.google.com/spreadsheets/d/1PzKvxN1ARlnQVYnCtM05Cs15VzTi76UHMyJmk6CQrNs/edit#gid=0"
strcontain = "TC-100" #line 56, strcontains, this is what chooses the modules, make sure is commented with this
ReliabilityChamber = "Thermal Cycle" #Hast #Damp Heat #ALSO LINE 143, numbers are set to 50, 100, 200, 300, change to desired numbers




#############################################
#Projstr = 'VAL1'  # project ID
#projectboolean = df[~df['Batch_ID'].str.contains(Projstr)]
#df.drop(projectboolean.index, inplace=True)
#df = df.sort_values(by='Measurement_Date-Time', ascending=True)
pd.set_option('display.width', None)
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1,)
print(df)


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


#large dataframe, only extract modules containing certain 'rel' chamber comments
#then 
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
for i in range(1, len(workdf.index)):
    if workdf.iloc[i-1, 0].astype(int) < workdf.iloc[i, 0].astype(int):
        workdf.iloc[i, 11] = workdf.iloc[i-1, 11]
    else:
        workdf.iloc[i, 11] = i
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

    
#determines hours spent and uses that value as x-axis to plot, places it into column 19
workdf["TimeSpent"] = 0
for i in range(0, len(workdf.index)):
    Sample = workdf.iloc[i, 2]
    if Sample.find('200') != -1:
        workdf.iloc[i, 19] = 200
    elif Sample.find('150') != -1:
        workdf.iloc[i, 19] = 150
    elif Sample.find('100') != -1:
        workdf.iloc[i, 19] = 100
    elif Sample.find('50') != -1:
        workdf.iloc[i, 19] = 50
    else:
        pass
print(workdf)

#initialize figure to be plotted
fig = make_subplots(rows=3, cols=2, subplot_titles=("dIsc",
                                                    "dVoc",
                                                    "dVmp",
                                                    "dImp",
                                                    "dPmp",
                                                    "dFF"))

#loop splits the workdf into respective (partids)/(tested parts)
#loops through to collect matching partids and add the index to a dummy list
#and when it reaches a value =! part id, then plots that collected data, and reinitializes for next group
values = [0]
for z in range(0, len(workdf.index)-1):
    #if workdf.iloc[z, 11] == workdf.iloc[z+1, 11]: THIS WON'T WORK BC OMITS THE LAST couple #print(workdf.iloc[z,11])
    if (z < len(workdf.index)) & (workdf.iloc[z, 11] == workdf.iloc[z+1, 11]):
        values.append(z+1)
        print(z)
    else:
        fig.append_trace(go.Scatter(
                x=workdf.iloc[values, 19], y=workdf.iloc[values, 12], text=workdf.iloc[values, 1], hovertemplate='<br>x:%{x}<br>y:%{y}<br>m:%{text}', mode="lines+markers"
                ), row=1, col=1)  # Isc
        fig.append_trace(go.Scatter(
                x=workdf.iloc[values, 19], y=workdf.iloc[values, 14], text=workdf.iloc[values, 1], hovertemplate='<br>x:%{x}<br>y:%{y}<br>m:%{text}', mode="lines+markers"
                ), row=1, col=2)  # Voc

        fig.append_trace(go.Scatter(
                x=workdf.iloc[values, 19], y=workdf.iloc[values, 15], text=workdf.iloc[values, 1], hovertemplate='<br>x:%{x}<br>y:%{y}<br>m:%{text}', mode="lines+markers"
                ), row=2, col=1)  # Vmp

        fig.append_trace(go.Scatter(
                x=workdf.iloc[values, 19], y=workdf.iloc[values, 16], text=workdf.iloc[values, 1], hovertemplate='<br>x:%{x}<br>y:%{y}<br>m:%{text}', mode="lines+markers"
                ), row=2, col=2)  # Imp

        fig.append_trace(go.Scatter(
                x=workdf.iloc[values, 19], y=workdf.iloc[values, 17], text=workdf.iloc[values, 1], hovertemplate='<br>x:%{x}<br>y:%{y}<br>m:%{text}', mode="lines+markers"
                ), row=3, col=1)  # Pmp

        fig.append_trace(go.Scatter(
                x=workdf.iloc[values, 19], y=workdf.iloc[values, 18], text=workdf.iloc[values, 1], hovertemplate='<br>x:%{x}<br>y:%{y}<br>m:%{text}', mode="lines+markers"
                ), row=3, col=2)  # dFF
        values = [z+1]


fig.update_layout(height=1100, width=1200,
                  title_text="Scatterplots of electrical parameters versus hours in " + ReliabilityChamber)
fig.update_annotations(font_size=12)
for ax in fig['layout']:
    if ax[:5] == 'xaxis':
        fig['layout'][ax]['dtick'] = 25
fig.update_yaxes(range=[-5, 2], dtick=1)
fig.show()
