import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from brokenaxes import brokenaxes

pd.set_option('display.width', None)
df = pd.read_csv(
    "C:/Users/andre/Downloads/All-101521-Modules.csv")


MindexNames = df[(df.iloc[:, 6] <= 0.1) | (
    df.iloc[:, 11] <= 9) ].index
df.drop(MindexNames, inplace=True)

#condition to only choose a specific Batch_ID \ Project ID
Projstr = 'REFERENCE'
projectboolean = df[~df['Batch_ID'].str.contains(Projstr)]
df.drop(projectboolean.index, inplace=True)

IDstr = 'REFERENCE1-1X2'
#IDstr = 'REFERENCE2-1X1'
idboolean = df[~df['Sample_ID'].str.contains(IDstr)]
df.drop(idboolean.index, inplace=True)

#Pmp mean
pmpmean = df["Pmp_(W)"].mean()
print(pmpmean)
#Pmp standard deviation
P1 = (df.iloc[:,9].sub(pmpmean)).pow(2)
P2 = P1.sum()
pmpSD = (P2 / len(df.index))**(1/2)

#pmpSD = df["Pmp_(W)"].std()
pmpUCL = pmpmean+pmpSD*3
pmpLCL = pmpmean-pmpSD*3
print(pmpLCL)

#Isc mean
iscmean = df.iloc[:,5].mean()
#isc standard deviation
#.....
#.....
#fill this in


outside = []
xoutside = []
for i in range(0,len(df.index)) :
    if (df.iloc[i, 9] <= pmpLCL ):
        outside.append(df.iloc[i, 9])
        xoutside.append(i+1)
        print('outside expected values, please review')
    else:
        pass
print(outside)
print(df)


x = np.linspace(1, len(df.index), num=len(df.index))
fig, ax = plt.subplots(figsize = (10, 6))
ax.axhline(pmpUCL, color='red')
ax.axhline(pmpLCL, color='red')
# Create a chart title
plt.scatter(x, df.iloc[:,9], s=40, facecolors='none', edgecolors='b')
plt.scatter(xoutside, outside,s=40, facecolors='none', edgecolors='r')
#plt.plot(x,df.iloc[:,5], 'bo')
plt.plot(x,df.iloc[:,9], 'b-')
ax.set_title('Reference-1x2 SPC Chart of Pmp_(W)')
right = 135
ax.text(right + 0.3, pmpUCL, "UCL = " + str("{:.2f}".format(pmpUCL)), color='red')
ax.text(right + 0.3, pmpmean, r'$\bar{x}$' + " = " + str("{:.2f}".format(pmpmean)), color='green')
ax.text(right + 0.3, pmpLCL, "LCL = " + str("{:.2f}".format(pmpLCL)), color='red')
ax.set(xlabel='Observation', ylabel='Individual Value')

import pygsheets
gc = pygsheets.authorize(
    service_file=r'C:\Users\andre\Downloads\fluent-outlet-329800-d7ce5f1f4cd1.json')
sh = gc.open('PY to Gsheet Test') #open the google spreadsheet
wks = sh[3] #select which sheet you want to use
wks.set_dataframe(df.iloc[:120,:],(1,1)) #inside the sheet, now it gets updated with specific dataframe

plt.grid()
#plt.show()
