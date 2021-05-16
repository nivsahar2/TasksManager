"""
@author: nivsa
@Date: 14/05/2021
@Last Edited: 14/05/2021 By Niv Sahar
"""
##Imports
#########################
import PySimpleGUI as sg
from datetime import datetime
from datetime import date
import os
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree
import pywhatkit as pt


##Colors and designs
#########################
BORDER_COLOR = '#550FAA'
DARK_HEADER_COLOR = '#000555'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT_INSIDE = (250, 10)
BPAD_RIGHT = ((10,20), (10, 20))


task_list = []

##get working directory
cwd = os.getcwd()
file_name = cwd+'\\Tasks_List.xml'

## A function that returns the current to-do list to be performed
##
#########################
def get_Tasks_List():
   
    tasks = []
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
    
        for elem in root:
            for subelem in elem:
                tasks.append(subelem.text)
   
    except Exception:
    
        pass
    
    return tasks


## A function that adds one task to the current to-do list
##
#########################    
def append_task(item,date):
    
    tasks = get_Tasks_List()
   
    if item not in tasks and item is not None:
        
        tasks.append(item+"   "+ date)
        root = ET.Element("root")
        doc = ET.SubElement(root, "Task")
        
        for i in range(0,len(tasks)):
            ET.SubElement(doc, "task", name="task"+str(i+1)).text = str(tasks[i]) 
        
        tree = ET.ElementTree(root)
        tree.write(file_name)
    
    task_list = get_Tasks_List() 
    window['-inputTask-'].update()
    window['-LIST-'].update(task_list) 
    
## A function that remove in one task from the current to-do list
##
#########################  
def delete_Task(element):
                        
    tree = ElementTree()
    tree.parse(file_name)

    parents = tree.findall('Task')
    
    for parent in parents:
      
      childs = parent.findall('task')
      
      for child in childs:
          element = ''.join(element)
          
          if child.text == element:
              print(1)
              parent.remove(child)
    
    tree.write(file_name)
    task_list = get_Tasks_List() 
    window['-LIST-'].update(task_list) 

 
## A function that remove all the tasks from the list
##
#########################      
def delete_All():
    
    tree = ElementTree()
    tree.parse(file_name)

    parents = tree.findall('Task')
    
    for parent in parents:
    
      childs = parent.findall('task')
      
      for child in childs:
          parent.remove(child)
    
    tree.write(file_name)
    task_list = get_Tasks_List() 
    window['-LIST-'].update(task_list) 
    
    
##get all our tasks   
task_list = get_Tasks_List()   
    
##Topic banner
top_banner = [[sg.Text('Task Manager'+ ' '*90, font='Any 20', background_color=DARK_HEADER_COLOR),
                   sg.Text(str(date.today()), font='Any 20', background_color=DARK_HEADER_COLOR)]]

##Down banner
down_banner = [[sg.Text('Developed by Niv Sahar'+' '*5, font='Any 12', background_color=DARK_HEADER_COLOR),
                sg.Button('Click Me for my LinkedIn', font='Any 12'),sg.Text(' '*40 ,background_color=DARK_HEADER_COLOR),sg.Input('', font='Any 12',key='-GOOGLE-'),
                sg.Button('Google Search', font='Any 12')
              ]]
    
## the code is separete to 3 blocks
#############################################################################################################################
#BLOCK 1
block_Delete = [[sg.Text('Will be added later', font='Any 14'),],
            ]
    
#BLOCK 2
block_Add = [[sg.Text('Add new Task'+' '*25, font='Any 14'),sg.Text('Submitted Date', font='Any 14')],
            [sg.Input(key='-inputTask-',size=(35,2)),sg.Input(key='-inputDate-',size=(20,2))],
            [sg.Button('Add new Task',size=(12,2),pad=BPAD_LEFT_INSIDE)],
            ]
#BLOCK 3
block_List = [[sg.Text('Tasks List', font='Any 14')],
           [sg.Listbox(task_list, size=(72, 9), enable_events=True, key='-LIST-',font=("Helvetica", 15))],
            [ sg.Button('Refresh List',size=(10,2),pad=BPAD_LEFT_INSIDE), sg.Button('Delete Task',size=(10,2),pad=BPAD_LEFT_INSIDE),sg.Button('Delete All',size=(10,2),pad=BPAD_LEFT_INSIDE), sg.Button('Exit',size=(10,2),pad=BPAD_RIGHT_INSIDE)],
            ]              
    
#Our program Layout
layout = [[sg.Column(top_banner, size=(1120, 60), pad=(0,0), background_color=DARK_HEADER_COLOR)],
          [sg.Column([[sg.Column(block_Add, size=(450,150), pad=BPAD_LEFT_INSIDE)],
          [sg.Column(block_Delete, size=(450,150),  pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column(block_List, size=(610, 320), pad=BPAD_RIGHT)],
          [sg.Column(down_banner, size=(1120, 45), pad=(0,0), background_color=DARK_HEADER_COLOR)]]

## Create the window with title, layout we created, and designs    
window = sg.Window('Task Manager', layout, margins=(0,0), background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True)

#############################################################################################################################3


## Refresh the tasks list
##
#########################################      
def refresh_Tasks_List():
    
    task_list = get_Tasks_List() 

    window['-LIST-'].update(task_list)   
 

## Main function
##
#########################################    
def main():
    
    while True: # Event Loop
        
        event, values = window.read()
        
        #
        # Check which Buttons were clicked
        # And called the appropriate function
        ###############################################
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
                  
        elif event == 'Add new Task':
            
            if values['-inputTask-'] != '':
                
                try:
                    task_date = datetime.strptime(values['-inputDate-'], '%d/%m/%Y').date()
                
                ##  Check if the date is bigger then today date
                    if task_date > date.today():
                
                ## Check for task that less than 40 chars        
                        if len(values['-inputTask-']) < 40:
                ## Call append_task function
                            append_task(values['-inputTask-'],values['-inputDate-'])
                    else:
                        sg.Popup("Cannot enter date from before today's date", keep_on_top=True)
                ## Exception if the date is not in the format 'xx/xx/xxxx'
                except ValueError:
                        sg.Popup('Wrong date format', keep_on_top=True)
                
                ## Clear inputs
                window['-inputDate-'].update()
                window['-inputTask-'].update()
            else:
                sg.Popup('Empty Field', keep_on_top=True)
            
        elif event == 'Refresh List':
        ## Call refresh list function
            refresh_Tasks_List()
      
        elif event == 'Delete Task':
        ## Call delete task function
            delete_Task(values['-LIST-']);
        elif event == 'Delete All':
        ## Call delete all tasks function     
            delete_All()
        elif event == 'Click Me for my LinkedIn':
        ## Call delete all tasks function     
            pt.search("https://www.linkedin.com/in/niv-sahar-a815651b7/")
            
        elif event == 'Google Search':
        ## Make a google search if input not empty  
            if values['-GOOGLE-'] != '':
                pt.search(values['-GOOGLE-'])
                window['-GOOGLE-'].update([])
        ##############################################
             
    ## Close Windows    
    window.close()
    
if __name__ == "__main__":
    main()
    
    
    

    
    
    
