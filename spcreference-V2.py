from plotly.subplots import make_subplots
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygsheets
gc = pygsheets.authorize(
    service_file='C:/Users/andre/Downloads/fluent-outlet-329800-d7ce5f1f4cd1.json')
sh = gc.open('2022 Reliability Parts') #open the google spreadsheet
wks = sh[0] #select which sheet you want to use
df = wks.get_as_df() #inside the sheet, now it gets updated with specific dataframe
print(df.head())

#read.iloc[:,3] = read.iloc[:,3].fillna('')
print(df.iloc[:,3])



#Pmp mean
pmpmean = df["REL MODULE (W)"].mean()
print(pmpmean)
#Pmp standard deviation
P1 = (df.iloc[5:,1].sub(pmpmean)).pow(2)
P2 = P1.sum()
pmpSD = (P2 / len(df.index))**(1/2)
exit()

#pmpSD = df["Pmp_(W)"].std()
pmpUCL = pmpmean+pmpSD*3
pmpLCL = pmpmean-pmpSD*3
print(pmpLCL)

outside = []
xoutside = []
for i in range(5,len(df.index)) :
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




plt.show()
