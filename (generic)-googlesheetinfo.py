


# share with  andre-354@fluent-outlet-329800.iam.gserviceaccount.com

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd

username = 'andrew.hu'
api_key = 'iVl6cjSPrLfIYfp75OTP'
tls.set_credentials_file(username=username, api_key=api_key)


import pygsheets
gc = pygsheets.authorize(
    service_file='C:/Users/andre/Downloads/fluent-outlet-329800-d7ce5f1f4cd1.json')
sh = gc.open('[UCSD]encapdaq') #open the google spreadsheet
