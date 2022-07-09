import win32com.client as win32
excel = win32.gencache.EnsureDispatch('Excel.Application')

import sys
PptApp = win32.Dispatch("Powerpoint.Application")
PptApp.Visible = True
PPtPresentation = PptApp.Presentations.Open(r'C:\Users\andre\Downloads\Test.pptx')
pptSlide = PPtPresentation.Slides.Add(1,11)
Pict1 = pptSlide.Shapes.AddPicture(FileName=r'C:\Users\andre\Desktop\mytable.png', LinkToFile=False, SaveWithDocument=True, Left=100, Top=100, Width=-1, Height=-1)

pptSlide3 = PPtPresentation.Slides.Add(1,11)
pptSlide5 = PPtPresentation.Slides.Add(1,11)
Pict2 = pptSlide3.Shapes.AddPicture(FileName=r'C:\Users\andre\Desktop\mytable.png', LinkToFile=False, SaveWithDocument=True, Left=100, Top=100, Width=-1, Height=-1)
#still ends up creating, 1 blank title slide, 2 slides with dataframe pictures, and then the last slide which is also blank

pptSlide3 = PPtPresentation.Slides.Add(1,11)
Pict2 = pptSlide3.Shapes.AddPicture(FileName=r'C:\Users\andre\Desktop\mytable.png', LinkToFile=False, SaveWithDocument=True, Left=100, Top=100, Width=-1, Height=-1)
txBox = pptSlide.Shapes.AddTextbox(1,100,100,400,400)
tf = txBox.TextFrame
Final = tf.TextRange.Text = "Here is some test text"
