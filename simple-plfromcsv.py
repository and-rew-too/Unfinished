import plotly
import plotly.graph_objects as go
import numpy as np
import pandas as pd

df = pd.read_csv(r"C:\Users\andre\Downloads\2022 February 25 12_28_11.csv")
pd.set_option('display.width', None)
newdf = pd.DataFrame(np.zeros([1024,1024]))
sh_0, sh_1 = newdf.shape
x, y = np.linspace(0, sh_0-1, sh_0), np.linspace(0, sh_1-1, sh_1)

#for i in range(0,len(df.index)):
for i in range(0,100000):
    a = df.iloc[i,2]
    b = df.iloc[i,3]
    newdf.iloc[a,b] = df.iloc[i,4]
print(newdf)

fig = go.Figure(data=[go.Surface(z=newdf, x=x, y=y)])
fig.update_layout(title='PL Image Intensity', autosize=False,
                  width=3000, height=3000,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()

#ILOC
#to do 100,000 assignments it takes 14.61sec
# to do 1,000,000 assignments it takes 180sec
#IAT
# to do 100,000 assignments it takes 3.77sec
# to do 1,000,000 assignments it takes 27.55sec
