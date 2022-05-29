
## MUST MAKE SURE TO KEEP CONSISTENCY FROM THE OTHER PYTHON < -- USE THAT SAME CSV FILE THAT HAD BEEN PRINTED FROM workdf

from datetime import datetime
dateTimeObj = datetime.now()
tsStr = dateTimeObj.strftime("%b %d %Y")
print('Current Timestamp : ', tsStr)

import dataframe_image as dfi 
start = "C:/Users/andre/Downloads/"
openpath = start + "lri-hast" + ".csv"
exitpath = start + "lri-hast-" + tsStr + ".png"

df = pd.read_csv(openpath, header = None) #THIS ONE IS THE MOST IMPORTANT LINE 
df = df.head()
df_styled = df.style.set_properties(**{'text-align': 'center'})
dfi.export(df_styled, exitpath)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
image = mpimg.imread(exitpath)
plt.imshow(image)
plt.show()
