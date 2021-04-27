#Convert sdlxliff to xlsx
#pip install PySimpleGUI,tkinter,xlsxwriter
#By Bill Fan Zhxin
import os
import re
import PySimpleGUI as sg
import tkinter
import xlsxwriter
from GetTUsInfosSDLXLIFF import GetTUsInfosSDLXLIFF

if __name__ == '__main__':
    
    layout=[
            [sg.InputText('',enable_events=True,key='_Path_',size=(60,0)),sg.Button('Borwse the .sdlxliff',key='_Browse_')],[sg.Text('By SuperBill (fzx2004@126.com)'),sg.Button('Convert to XLSX',key='_Convert_'),]
            
    ]
    window=sg.Window('Convert sdlxliff to XLSX',layout=layout,finalize=True)
    while True:
        event,value=window.read()
        if event is None:
            break
        if event=='_Browse_':
            file_opt = options = {}  
            #options['defaultextension'] = '.sdlxliff,.docx'  
            options['filetypes'] = [ ('sdlxliff', '.sdlxliff'),('all files', '.*')] 
            
            filenamest=tkinter.filedialog.askopenfilenames(**file_opt)
            #print(filenamest)
            if len(filenamest)>0:
                window.Element('_Path_').update(filenamest[0].replace('/','\\'))
        if event=='_Convert_':
            tulist=GetTUsInfosSDLXLIFF(value['_Path_'])
            if len(tulist)>0:
                xlsxpath=os.path.splitext(value['_Path_'])[0]+'.xlsx'
                i=0
                wb = xlsxwriter.Workbook(xlsxpath)
                wsh=wb.add_worksheet()
                
                wsh.write(i,0,'Source')
                wsh.write(i,1,'Target')
                wsh.write(i,2,'Status')
                wsh.write(i,3,'origin')
                wsh.write(i,4,'origin-system')
                wsh.write(i,5,'percent')
                wsh.write(i,6,'Locked')
                for tuinfo in tulist:
                    i+=1
                    j=0
                    for tue in tuinfo:
                        wsh.write(i,j,tue)
                        j+=1
                wb.close()
                sg.popup('Done!')
