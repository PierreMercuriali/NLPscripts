"""
    PDFtoTXT.py
    7.7.2021: ported to python 3.x
    Requirements: pdfminer.six
    Instructions: place .py file in folder alongside pdfs and launch.    
"""

import sys, pdfminer, io
from os import listdir,mkdir
from os.path import isfile, join
from pdfminer.high_level import extract_text

def quickSaveUnicode(content, fn):
    with io.open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("\tcontent saved")

def quickSave(content, fn):
    with open(fn, "w") as f:
        f.write(content)
    print("\tcontent saved")

mypath      = u"./"
savepath	= u"./text/"
try: 
    mkdir(savepath) 
except OSError as error: 
    print(error)  
onlyfiles   = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles   = [f for f in onlyfiles if f[-3:]=='pdf']

#print(onlyfiles)

print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
print("Extracting text from ", len(onlyfiles), "pdfs")
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")

for filename in onlyfiles:
    print("*", filename)
    text = extract_text(mypath+filename)
    #print("",len(text))
    try:
        quickSaveUnicode(text, "./text/"+filename[:-4]+".txt")
    except Exception as e: 
        print("\t error saving txt")
        print("\t", e)
