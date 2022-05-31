import pyodbc
import numpy as np
import pandas as pd

# conn = pyodbc.connect(
#    r'Driver={Microsoft Access Driver(*.mdb, *.accdb)};DBQ=C:/Users/Andrew Hu/Dropbox/PC/Downloads/Database1.accdb;')
# # for the Database1 testing, 'select * FROM poo')
# # as poo is the name of the database table
# for row in cursor.fetchall():
#    print(row)

#conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;ReadOnly=1;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};Exclusive=0;DriverId=25;DefaultDir=C:\USERS\ANDREW HU\DROPBOX\PC\DOWNLOADS;DBQ=C:\USERS\ANDREW HU\DROPBOX\PC\DOWNLOADS\Database1.accdb;')
pd.set_option('display.width', None)
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;ReadOnly=1;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};Exclusive=0;DriverId=25;DefaultDir=C:\USERS\ANDREW HU\DROPBOX\PC\DOWNLOADS;DBQ=C:\USERS\ANDREW HU\DROPBOX\PC\DOWNLOADS\MultiFlash_Database.accdb;')
cursor = conn.cursor()
cursor.execute('select * from Results')

df = pd.read_sql_query('SELECT * FROM Results', conn)


Powercutoff = 76
Projstr = 'LIQ1'  # project ID

# condition to only drop any "bad measurements" that have low Isc values
MindexNames = df[(df.iloc[:, 6] <= -0.1) | (
    df.iloc[:, 40] <= 0) | (df.iloc[:, 9] > Powercutoff)].index
df.drop(MindexNames, inplace=True)




#condition to only choose a specific Batch_ID \ Project ID
projectboolean = df[~df.iloc[:, 2].str.contains(Projstr)]
df.drop(projectboolean.index, inplace=True)
print(df)
