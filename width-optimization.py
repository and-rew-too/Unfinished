#TAKES INTO account the losses on a huasun cell, the silver paste and laser damage

import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

#ASSUMPTIONS MADE
#assuming voc does not change as laser cut width decreases, it does just barely, so (error is around 0.8%)
#assuming Jsc does not change as laser cut width decreases, IT DOES BY ABOUT (5%) 

# interpolated pFF from curve fitting function, r^2 is 0.985, (error is around 0.05%) 
# fill factor losses predominantly in Vmp and did not include in Imp at all, that fractional power losses, 
# 90% is responsible from Vmp, Imp the other 10% (FOUND THAT FOR HUASUN, 0.90 is ratio, but other cells 0.95 is) (error is around 0.001%) 
# the ideal diode equation has a n = 1 at all times (error is around ????) 
# assuming value for Rs, and also assuming a lumped series resistance model for single diode equation (error is ??????) 
# the Voc / Isc and Vmp / Imp ratio are equal (error around 6%)

sheet_url = "https://docs.google.com/spreadsheets/d/12RYFtjew1XxsE4Tf3L7E2ABPJv7y6wk80gXFf52WVzU/edit#gid=0"
pd.set_option('display.width', None)

url_1 = sheet_url.replace('/edit#gid=' , '/export?format=csv&gid=')
df = pd.read_csv(url_1,)
print(df)


def objective(x, a, c):
	return a*(x**-1.286) + c
    # b was actually the x^n power had to enter manually to find a solution
    # find it here, in desmos link https://www.desmos.com/calculator/og5tjbyujk

x = df.iloc[:,1]
y = df.iloc[:,10]
popt, _ = curve_fit(objective, x, y)
# summarize the parameter values
a, c = popt
# interploting values from 15 mm to 160mm and plotting the new curve
x_new = np.linspace(15, 160, 146)
y_new = objective(x_new, a, c)



k = 1.380*10**-23
q = 1.602*10**-19
Jsc = 0.038
Rs = 1.05
Voc = 0.730
Vmp = Voc* (y_new/100 *(1-(Rs*Jsc/Voc) ) / 0.95 )

# Isc = Jsc*16.6*((x_new*0.1)-0.5))
# STANDARD diode equation (including Rs) is Isc - Io*(e** (q*((V+I*Rs)/ (1.1*k*T))-1)) 

# right now we have Isc, Voc, n, but not Io yet
# STANDARD diode equation solve Voc = n*k*T*ln(Isc/Io +1)
# Io = Isc /   (   e** (q*((Voc)/ (1.1*k*T))-1 )
## how to solve for Io https://www.desmos.com/calculator/hiw9r119wh
## how to solve for Io https://www.pveducation.org/pvcdrom/solar-cell-operation/open-circuit-voltage


# WITH Io, can find Imp
## equation is: Imp = Isc - Io*(e** (q*((Vmp+Imp*Rs)/ (k*T))-1))
# error = 100
# Itest = 0.95*Isc
# while error > 0.05
	# Imp = Isc - Io*(e** (q*((Vmp+Itest*Rs)/ (k*T))-1))
	# error = Imp-Itest
	# Itest = Imp
# print(Itest)


Imp = (Jsc * 16.6 * ((x_new*0.1)-0.5) ) * 0.95
Pmp = Imp*Vmp
#below, ignores other factors and looks at only resistive losses from increasing length (ignores shading)
ff_finger_laser = Voc* (y_new/100*(1-(Rs*Jsc/Voc) )) * (1-((0.00064*Jsc*(x_new/10)**2)/(48*0.0014*Voc)) )
max_val = np.amax(ff_finger_laser)
max_index = np.where(ff_finger_laser == max_val)
max_x = x_new[max_index]



resistloss = 0.83 * (1-((0.00064*Jsc*(x_new/10)**2)/(48*0.0014*Voc)) )
print(resistloss)
new_Pmp = ff_finger_laser*Imp


fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=("pFF points", "fitted pFF","Voltage change/laser", "max Power","Final","Voltage change/fingers"))

fig.add_trace(go.Scatter(x=x, y=y),
              row=1, col=1)

fig.add_trace(go.Scatter(x=x_new, y=y_new),
              row=1, col=2)

fig.add_trace(go.Scatter(x=x_new, y=Vmp),
              row=1, col=3)
fig.add_trace(go.Scatter(x=x_new, y=Pmp),
              row=2, col=1)
fig.add_trace(go.Scatter(x=x_new, y=ff_finger_laser),
              row=2, col=2)
fig.add_trace(go.Scatter(x=x_new, y=new_Pmp),
              row=2, col=1)
fig.add_trace(go.Scatter(x=x_new, y=resistloss),
              row=2, col=3)
fig.add_trace(go.Scatter(x=max_x, y=[max_val]),
              row=2, col=2)

fig.update_layout(height=500, width=900,
                  title_text="Shingle Width Optimization")



#does not include shading yet... shading effect of Isc as we change the widths of fingers
