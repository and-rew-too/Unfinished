import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from scipy.interpolate import UnivariateSpline

## full list of resources needed to make this code function
#https://stackoverflow.com/questions/52014197/how-to-interpolate-a-2d-curve-in-python
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html
#https://matplotlib.org/3.5.0/gallery/shapes_and_collections/ellipse_demo.html
#https://www.researchgate.net/publication/354226402_Development_of_a_code_in_python_programming_language_to_generate_Ashby_chart_applied_for_materials_selection


import torch
x = torch.rand(2)
print(x)

exit()

#initializing data read from the 'csv' file
sheet_url = "https://docs.google.com/spreadsheets/d/1DlP7xF7aEk0xDsFkoAHK4fokn7nnX0AkwAXq0nBJSIs/edit#gid=1252599109"
url_1 = sheet_url.replace('/edit#gid=' , '/export?format=csv&gid=')
df = pd.read_csv(url_1,)
pd.set_option('display.width', None)

#taking out any extreneous information, ie the page numbers
dfm = df.iloc[:,0:7]
dfp = df.iloc[:,0:7]
dfc = df.iloc[:,0:7]


#METAL BRANCH
projectboolean = dfm[~dfm['Family'].str.contains('Metals')]
dfm.drop(projectboolean.index, inplace=True) #taking out any non-metal families
dfm = dfm[dfm['E(GPa)'].notna()] #taking out any metals entries without a value for E
print(dfm)
#now that data has been sufficiently cleaned, can parse it through to numpy array

data = dfm.to_numpy()
print(data)
print(data.shape)
fig, ax = plt.subplots()

def familyfinder(FamilyStr):
    test = np.zeros(shape=(100,2))
    for i in range(0,data.shape[0]):
        if data[i,3]==FamilyStr:
            test[i,0] = data[i,4]
            test[i,1] = data[i,6]
    test = test[~np.all(test == 0, axis=1)]
    return(test)

test1 = familyfinder("Steels")
test2 = familyfinder("Ti Alloys")
test3 = familyfinder("Precious")




#now that the subfamilies have been separated, find major minor axes to plot ellipse
def convexcreate(metalarray):
    maxx,maxy = np.amax(metalarray, axis=0)
    minx,miny = np.amin(metalarray, axis=0)
    print(maxx)
    print(maxy)
    centerx = ((maxx+minx)/2)
    centery = ((maxy+miny)/2)
    ellipse = Ellipse((centerx, centery), maxx-minx, maxy-miny, angle=0, alpha=0.1)
    return ellipse, centerx, centery



ellipse1,centerx,centery = convexcreate(test1)
plt.text(centerx,centery,'Steels',color='maroon')
ax.add_artist(ellipse1)
ellipse2,centerx,centery = convexcreate(test2)
ax.add_artist(ellipse2)
plt.text(centerx,centery,'Titanium',color='maroon')
ellipse3,centerx,centery = convexcreate(test3)
ax.add_artist(ellipse3)
plt.plot(test2[:,0], test2[:,1], 'o')
plt.plot(test1[:,0], test1[:,1], 'o')
plt.plot(test3[:,0], test3[:,1], 'o')
#fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})




#now subfamily ellipses have been plotted, need to plot the overall family polygons
metaltest = np.concatenate([test1,test2,test3]) #combining metals into large array (large square)
hull = ConvexHull(metaltest)
Convexm = np.zeros(shape=(100,2))
for simplex in hull.simplices:
    plt.plot(metaltest[simplex, 0], metaltest[simplex, 1], 'k-')
    Convexm[simplex, 0] = metaltest[simplex, 0]
    Convexm[simplex, 1] = metaltest[simplex, 1]
Convexm = Convexm[~np.all(Convexm == 0, axis=1)]
print(Convexm)
S = Convexm[0,:]
S = [S]
Convexm = np.concatenate((Convexm,S))


projectboolean = dfp[~dfp['Family'].str.contains('Polymers')]
dfp.drop(projectboolean.index, inplace=True) #taking out any non-polymers families
dfp = dfp[dfp['E(GPa)'].notna()] #taking out any polymers entries without a value for E
#print(dfp)
data = dfp.to_numpy()
print(data.shape)
test4 = familyfinder("Polystyrene")
test5 = familyfinder("Urea")
test6 = familyfinder("Fluorocarbons")
ellipse4,centerx,centery = convexcreate(test4)
ax.add_artist(ellipse4)
plt.text(centerx,centery,'PS',color='wheat')
ellipse5,centerx,centery = convexcreate(test5)
ax.add_artist(ellipse5)
plt.text(centerx,centery,'Ureas', color='wheat')
ellipse6,centerx,centery = convexcreate(test6)
ax.add_artist(ellipse6)
plt.text(centerx,centery,'Fluorocarbons',color='wheat')


projectboolean = dfp[~dfp['Family'].str.contains('Ceramics')]
dfc.drop(projectboolean.index, inplace=True) #taking out any non-ceramic families
dfc = dfc[dfc['E(GPa)'].notna()] #taking out any ceramic entries without a value for E
#print(dfc)
data = dfc.to_numpy()
test7 = familyfinder("Al2O3")
test8 = familyfinder("Si3N4")
test9 = familyfinder("SiC")
ellipse7,centerx,centery = convexcreate(test7)
ax.add_artist(ellipse7)
plt.text(centerx,centery,'Al2O3',color='indigo')
ellipse8,centerx,centery = convexcreate(test8)
ax.add_artist(ellipse8)
plt.text(centerx,centery,'Si3N4',color='indigo')
ellipse9,centerx,centery = convexcreate(test9)
ax.add_artist(ellipse9)
plt.text(centerx,centery,'SiC',color='indigo')

##############################################################################3
c =[  ( 7800,   203),
( 7500,  200),
 ( 4370,   124),
 ( 4510,   102),
( 4480,   106),
( 4430,   113),
 (10490,    83),
 (19320,    78),
 (21450,   168),( 7800,   203)]
points = np.array(c)
# C HERE IS THE EXACT SAME AS CONVEXM , JUST SHOWINGFOR CLARITY
distance = np.cumsum( np.sqrt(np.sum( np.diff(Convexm, axis=0)**2, axis=1 )) )
distance = np.insert(distance, 0, 0)/distance[-1]
splines = [UnivariateSpline(distance, coords, k=4, s=1333333) for coords in Convexm.T]
alpha = np.linspace(0, 1, 75)
points_fitted = np.vstack( spl(alpha) for spl in splines ).T
print(points_fitted)
ax.fill(points_fitted[:,0],points_fitted[:,1],facecolor='lightsalmon')
#plt.plot(*points.T, 'ok', label='original points');
#plt.plot(*points_fitted.T, '-r', label='fitted spline k=4, s=133333');
############################################################################

polytest = np.concatenate([test7,test8,test9]) #combining metals into large array (large square)
hull = ConvexHull(polytest)
Convexc = np.zeros(shape=(100,2))
for simplex in hull.simplices:
    plt.plot(metaltest[simplex, 0], polytest[simplex, 1], 'k-')
    Convexc[simplex, 0] = polytest[simplex, 0]
    Convexc[simplex, 1] = polytest[simplex, 1]
Convexc = Convexc[~np.all(Convexc == 0, axis=1)]
print(Convexc)
S = Convexc[0,:]
S = [S]
Convexc = np.concatenate((Convexc,S))





##############################################################################3
o = 400
Convexc = [(3970+o,         351.0344828),
(3986 +o  ,     408.9655172),
(3210 -o,        410.4827586),
 (2600  -o ,      143.1034483),
 (3580  +o,       237.9310345),
 (3970+o,         351.0344828)]
Convexc = np.array(Convexc)
distance = np.cumsum( np.sqrt(np.sum( np.diff(Convexc, axis=0)**2, axis=1 )) )
distance = np.insert(distance, 0, 0)/distance[-1]
splines = [UnivariateSpline(distance, coords, k=2,s=10000) for coords in Convexc.T]
alpha = np.linspace(0, 1, 75)
points_fitted = np.vstack( spl(alpha) for spl in splines ).T
ax.fill(points_fitted[:,0],points_fitted[:,1],facecolor='lightsalmon')
###############################################################################



#now that family polygons are all composed, can plot entire set of values together
ax.set_xlim(400,24000)
ax.set_ylim(0.01,500)
ax.set_yscale('log')
ax.set_xscale('log')
plt.plot(Convexc[:,0], Convexc[:,1], 'o')
plt.plot(Convexc[1,0], Convexc[1,1], 'ko')
plt.plot(Convexc[2,0], Convexc[2,1], 'go')
plt.plot(Convexc[3,0], Convexc[3,1], 'ro')
plt.plot(Convexc[4,0], Convexc[4,1], 'bo')
print(Convexc)
plt.xlabel('density [kg/m3]')
plt.ylabel('Youngs modulus [GPa]')
plt.grid(True)
plt.show()
