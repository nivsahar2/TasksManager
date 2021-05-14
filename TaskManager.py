"""
@author: nivsa
@Date: 14/05/2021
@Last Edited: 14/05/2021 By Niv Sahar

"""


##Imports
import PySimpleGUI as sg
from datetime import date
import os
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree


##Colors and designs
BORDER_COLOR = '#AAAAAA'
DARK_HEADER_COLOR = '#002838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT_INSIDE = (350, 10)
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

    tree = ET.parse(file_name)
    root = tree.getroot()
    
    for elem in root:
        for subelem in elem:
            tasks.append(subelem.text)
    return tasks


## A function that adds one task to the current to-do list
##
#########################    
def append_task(item):
    
    tasks = get_Tasks_List()
   
    if item not in tasks and item is not None:
        
        tasks.append(item)
        root = ET.Element("root")
        doc = ET.SubElement(root, "Task")
        
        for i in range(0,len(tasks)):
            ET.SubElement(doc, "task", name="task"+str(i+1)).text = str(tasks[i]) 
        
        tree = ET.ElementTree(root)
        tree.write(file_name)
        
    main()
     
    
## Refresh the tasks list
##
#########################      
def refresh_Tasks_List():
    main()
 
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
        if child.text == element:
            parent.remove(child)
    tree.write(file_name)
    main()
    
 
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
    main()
    
## Main function
##
#########################################
          
def main():
     ##get all our tasks   
    task_list = get_Tasks_List()   
    
    ##Topic banner
    top_banner = [[sg.Text('Task Manager'+ ' '*90, font='Any 20', background_color=DARK_HEADER_COLOR),
                   sg.Text(str(date.today()), font='Any 20', background_color=DARK_HEADER_COLOR)]]
    
    ## the code is separete to 3 blocks
    ################################################################################################
    #BLOCK 1
    
    block_Delete = [[sg.Text('Delete Task', font='Any 14'),],
                [sg.Combo(task_list, size=(45, 5), enable_events=True, key='-COMBO-')],
                [sg.Button('Delete Task',size=(10,2),pad=BPAD_LEFT_INSIDE),sg.Button('Delete All',size=(10,2),pad=BPAD_LEFT_INSIDE)],
                ]
    
    #BLOCK 2
    block_Add = [[sg.Text('Add new Task'+' '*25, font='Any 14'),sg.Text('Submitted Date', font='Any 14')],
                [sg.Input(key='-inputTask-',size=(35,2)),sg.Input(key='-inputDate-',size=(20,2))],
                [sg.Button('Add new Task',size=(12,2),pad=BPAD_LEFT_INSIDE)],
                ]
    #BLOCK 3
    block_List = [[sg.Text('Tasks List', font='Any 14')],
               [sg.Listbox(task_list, size=(72, 10), enable_events=True, key='-LIST-')],
                [ sg.Button('Refresh List',size=(10,2),pad=BPAD_LEFT_INSIDE), sg.Button('Exit',size=(10,2),pad=BPAD_RIGHT_INSIDE)],
                ]
              
    
    #Our program Layout
    layout = [[sg.Column(top_banner, size=(1100, 60), pad=(0,0), background_color=DARK_HEADER_COLOR)],
          [sg.Column([[sg.Column(block_Add, size=(450,150), pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(block_Delete, size=(450,150),  pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column(block_List, size=(550, 320), pad=BPAD_RIGHT)]]
    ## Create the window with title, layout we created, and designs    
    window = sg.Window('Task Manager', layout, margins=(0,0), background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True)
    
    while True: # Event Loop
        event, values = window.read()
        
        #
        # Check which Buttons were clicked
        # And called the appropriate function
        ###############################################
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
                  
        elif event == 'Add new Task':
            window['-inputTask-'].update()
            append_task(values['-inputTask-'])
      
        elif event == 'Refresh List':
            refresh_Tasks_List()
      
        elif event == 'Delete Task':
             window['-COMBO-'].update()
             delete_Task(values['-COMBO-']);
        elif event == 'Delete All':
             delete_All()
        ##############################################
             
    ## Close Windows    
    window.close()
    
if __name__ == "__main__":
    main()
    