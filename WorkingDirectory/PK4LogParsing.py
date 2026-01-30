# -*- coding: utf-8 -*-
"""
Last Edit on Tue Sep 2 2025

Attempt to parse PK4 experiment log

@author: Mason Sake
"""
#%% Import Librairies and Functions 

###############################################################################
#%% Define Variables 
'''
The following variables are intended for global definition of this file. They 
can appear in some of the functions bellow. 

NB: More user defined variables are found bellow in the Code Scripting and 
Testing section. 
'''

###############################################################################
#%% Define Functions 

#-----------------------------------------------------------------------------#
 
#-----------------------------------------------------------------------------#            
            
###############################################################################
#%% Code Scripting and Testing 

#%%% Import Libraries and Functions for scripting 
import os 
import sys 
import cv2

from datetime import datetime
from datetime import timedelta

#FUNCTIONS FROM OTHER SCRIPTING FILES!!!
from VideoHandelingFunctions import extractVideoclip
#-----------------------------------------------------------------------------#
#%%% User Defined Variables for Scripting 

max_type_chr_length = 30

# Main Log Things 
mainlog_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\PK4_combineddcrf_c20_250203_100429.log"
mainlog_type_delineator = ':'

# Camera Log Things 
vm1log_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM1_RUN_250203_100429.log"
vm2log_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM2_RUN_250203_100429.log"
vm3log_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM3_RUN_250203_100429.log"

vm1timetag_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM1_250203_100429.timetag"
vm2timetag_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM2_250203_100429.timetag"
vm3timetag_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM3_250203_100429.timetag"

vm1sync2_filepath = r"C:\Users\MasonSake\Desktop\C20 100429 Run Logs\VM1_SYNC_250203_100429.log"

#Video File Things 
#vm1avi_filepath = r"R:\Data\PK4-C20\VM1\VM1_AVI_250203_101231.avi"
#vm1_start_time = datetime.strptime("10:12:31.83", "%H:%M:%S.%f")
#vm1_end_time = datetime.strptime("11:12:23.88", "%H:%M:%S.%f")
vm2avi_filepath = r"R:\Data\PK4-C20\VM2\VM2_AVI_250203_101232.avi"
vm2_start_time = datetime.strptime("10:12:32.78", "%H:%M:%S.%f")
vm2_end_time = datetime.strptime("11:12:24.58", "%H:%M:%S.%f")

outlog_filepath = "outlogfile.txt"
#-----------------------------------------------------------------------------#
#%%% File Scripting 

#-----------------------------------------------------------------------------#
# First We will Parse the main Log 
    
#Check if the given filepath actually exists 
if os.path.exists(mainlog_filepath): 
    pass
else: 
    sys.exit("⚠ WARNING: Input File does not exist.")

mainlog = [] 
mainlog_message_types = [] 

with open(mainlog_filepath, "r", encoding = 'utf-8', errors = 'ignore') as file: 
    lines = file.readlines()
    for i in range(0,len(lines)): 
        entry = {}
        line = lines[i]
        if i == 0: 
            time = line[-9:-1]
            message = line[0:-9]
            entry["Time"] = time 
            entry["Type"] = "Log Start"
            entry["Message"] = message
            message_type = "None"
        elif i == len(lines): 
            time = line[-9:-1]
            message = line[0:-9]
            entry["Time"] = time 
            entry["Type"] = "Log End"
            entry["Message"] = message
            message_type = "None"
        else: 
            time = line[0:8]
            message = line[9:-1]
            entry["Time"] = time 
            typebreak_index = message.find(mainlog_type_delineator) 
            if typebreak_index == -1 or typebreak_index > max_type_chr_length: 
                message_type = "None" 
            else: 
                message_type = message[0:typebreak_index] 
                message = message[(typebreak_index+1):]
            entry["Type"] = message_type
            entry["Message"] = message
        
        mainlog.append(entry)
        mainlog_message_types.append(message_type)
#-----------------------------------------------------------------------------#
#Now we can loop through the main log: 

#Test by creating a log of the events:
    
# with open('output.txt', 'w') as f: 
#     total_rest_time = timedelta()
#     for index, entry in enumerate(mainlog): 
#         if "*** end" in entry['Message'] or "*** End" in entry['Message'] : 
#             i = index
#             print(entry, file=f)
#             start_time_str = entry['Time']
#             start_time_time = datetime.strptime(start_time_str, "%H:%M:%S")
#             for i in range(index, len(mainlog)): 
#                 entry_comp = mainlog[i] 
#                 found_next = False
#                 if "entered by operator" in entry_comp['Message'] and found_next == False:
#                     print(entry_comp, file = f)
#                     end_time_str = entry_comp['Time']
#                     end_time_time = datetime.strptime(end_time_str, "%H:%M:%S")
#                     found_next = True
#                     break 
#                 else: 
#                     pass
#             elapsed_time = end_time_time - start_time_time
#             total_rest_time = elapsed_time + total_rest_time
#             print("A ",elapsed_time, " pause from ", start_time_str, " to ", end_time_str, ".", file = f)
#             print("Elapsed Rest Time: ", total_rest_time, file=f)
#             print("==========",file = f)   

#Get the total number of frames in a video
VM2_capture = cv2.VideoCapture(vm2avi_filepath)
if not VM2_capture.isOpened(): 
    print(f"Error: Could not open video vile {vm2avi_filepath}")

total_VM2_frames = int(VM2_capture.get(cv2.CAP_PROP_FRAME_COUNT))


with open(outlog_filepath, 'w') as f: 
    total_rest_time = timedelta()
    for index, entry in enumerate(mainlog): 
        #Hard coded find the "Pauses" start and end times 
        if "*** end" in entry['Message'] or "*** End" in entry['Message'] : 
            i = index
            print(entry, file=f)
            start_time_str = entry['Time']
            start_time_time = datetime.strptime(start_time_str, "%H:%M:%S")
            for i in range(index, len(mainlog)): 
                entry_comp = mainlog[i] 
                found_next = False
                if "entered by operator" in entry_comp['Message'] and found_next == False:
                    print(entry_comp, file = f)
                    end_time_str = entry_comp['Time']
                    end_time_time = datetime.strptime(end_time_str, "%H:%M:%S")
                    found_next = True
                    break 
                else: 
                    pass
            #Now Do the things with the time stamps found 
            if start_time_time < vm2_start_time or end_time_time > vm2_end_time: 
                pass
            else: 
                start_frame_time = start_time_time - vm2_start_time
                end_frame_time = end_time_time - vm2_start_time 
                
                #Convert to corrected frame time 
                end_time_delta = vm2_end_time - end_time_time 
                end_frames_delta = 70*end_time_delta.total_seconds()
                end_frame_num = total_VM2_frames - int(end_frames_delta)
                
                start_frame_num = int(70*start_frame_time.total_seconds())
                
                extract_filename = (start_time_str.replace(":","") + "-" + 
                                    end_time_str.replace(":","") + "-" +
                                    "VM2_Video_Snip.avi")
                
                #Extract video Clip
                extractVideoclip(vm2avi_filepath, 
                                 start_frame_num, end_frame_num, 
                                 outfilename = extract_filename)
            
            elapsed_time = end_time_time - start_time_time
            total_rest_time = elapsed_time + total_rest_time
            print("A ",elapsed_time, " pause from ", start_time_str, " to ", end_time_str, ".", file = f)
            print("Elapsed Rest Time: ", total_rest_time, file=f)
            print("==========",file = f)

#-----------------------------------------------------------------------------#


###############################################################################
################################# Depreciated #################################
###############################################################################

# input_file = r"R:\Data\PK4-C20\Logs\PK4_combineddcrf_c20_250203_100429.log"

# if os.path.exists(input_file): 
#     pass 
# else: 
#     sys.exit("WARNING: Input File does not exist.")
    
# log = [] 
# message_types = [] 
# type_delineator = ":"
# max_type_length = 30

# count = 0

# with open(input_file, "r", encoding = 'utf-8', errors = 'ignore') as file: 
#     lines = file.readlines()
#     for i in range(0,len(lines)): 
#         entry = {}
#         line = lines[i]
#         if i == 0: 
#             time = line[-9:-1]
#             message = line[0:-9]
#             entry["Time"] = time 
#             entry["Type"] = "Log Start"
#             entry["Message"] = message
#             message_type = "None"
#         elif i == len(lines): 
#             time = line[-9:-1]
#             message = line[0:-9]
#             entry["Time"] = time 
#             entry["Type"] = "Log End"
#             entry["Message"] = message
#             message_type = "None"
#         else: 
#             time = line[0:8]
#             message = line[9:-1]
#             entry["Time"] = time 
#             typebreak_index = message.find(type_delineator) 
#             if typebreak_index == -1 or typebreak_index > max_type_length: 
#                 message_type = "None" 
#             else: 
#                 message_type = message[0:typebreak_index] 
#                 message = message[(typebreak_index+1):]
#             entry["Type"] = message_type
#             entry["Message"] = message
        
#         log.append(entry)
#         message_types.append(message_type)
        
#         if "dlr_Pause" in message_type: 
#             #print(entry["Time"] + " " +entry["Message"])
#             count += 1
#         # if "Start camera move" in message: 
#         #     print(entry["Time"] + " " +entry["Message"])
#         # if "end camera move" in message: 
#         #     print(entry["Time"] + " " +entry["Message"])

###############################################################################
################################ End of Script ################################
###############################################################################