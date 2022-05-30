import win32com.client as win32
excel = win32.gencache.EnsureDispatch('Excel.Application')

import sys
PptApp = win32.Dispatch("Powerpoint.Application")
PptApp.Visible = True
PPtPresentation = PptApp.Presentations.Open(r'C:\Users\andre\Downloads\Test.pptx')
pptSlide = PPtPresentation.Slides.Add(1,11)
Pict1 = pptSlide.Shapes.AddPicture(FileName=r'C:\Users\andre\Desktop\mytable.png', LinkToFile=False, SaveWithDocument=True, Left=100, Top=100, Width=-1, Height=-1)

