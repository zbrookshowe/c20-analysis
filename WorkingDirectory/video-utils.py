# -*- coding: utf-8 -*-
"""
File Containing general video utility functions  

Last Edit on Wed Aug  6, 2025 ~ Mason S. Sake

@author(s): Mason Sake

# -----------------------------------------------------------------------------
# DISCLAIMER:
# Portions of this script were developed with the assistance of generative AI,
# including suggestions and code explanations provided by OpenAI's ChatGPT.
# All AI implemented code has been reviewed and tested by the author(s).
# -----------------------------------------------------------------------------
"""

#%% Import Libraries As Bulk
import subprocess 
import json
import ffmpeg
import numpy as np

#Specific Fucntions Import 
from os.path import isfile 

###############################################################################

#%% Varriable Setting 

video_path = r"R:\OneDrive - Auburn University\b Research\Coding\Working Directory\C20_plane_example.avi"

###############################################################################
#%% Define Functions
def extract_frame_timestamps(video_path): 
    """
    Extracts frame presentation timestamps from a video using ffprobe. 

    Parameters
    ----------
    video_path : str
        Path to the input video file

    Returns
    -------
    list[float]
        A list of frame timestamps in seconds.

    """
    # Build the ffprobe command to extract frame info from the video
    cmd = [
        'ffprobe',
        '-show_frames',             # Show information for each frame
        '-select_streams', 'v',     # Select only the video stream
        '-of', 'json',              # Output format as JSON
        video_path
    ]

    # Run the command and capture stdout and stderr
    result = subprocess.run(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )

    # If ffprobe fails (e.g., invalid file), print error and return empty list
    if result.returncode != 0:
        print("ffprobe error:", result.stderr)
        return []

    # Parse the JSON output
    data = json.loads(result.stdout)

    # Extract 'pkt_pts_time' from each frame (presentation timestamp in seconds)
    timestamps = []
    for frame in data.get('frames', []):
        if 'pkt_pts_time' in frame:
            timestamps.append(float(frame['pkt_pts_time']))

    # Return list of timestamps
    return timestamps

###############################################################################

def check_for_dropped_frames(argument, deviation = 0.05, verbose = True): 
    """
    Checks for dropped frames in a vidoe or a list/array of frame timetamps
    
    Parameters
    ----------
    argument : (str | list | np.ndarray)
        A video path, list of frame timestamps, or 1D numpy array containing 
        the frame timestamps 
    deviation : (float), optional
        Allowed deviation as a fraction of the ideal frame interval. (The 
        default is 0.05 = 5%)
    verbose : bool, optional
        Prints detailed info and diagnostics.( The default is True.)

    Returns
    -------
    did_deviate : bool
        Whether any time between frames deviated beyond allowed deviation.
    skipped_frames_index : list[int]
        Indicies of the frames where delays outside the allowed deviation 
        likely occurred. 

    """
    # Handle the input and figure out what the argument is 
    if isinstance(argument, str) and isfile(argument):
        video_path = argument
        timestamps = extract_frame_timestamps(video_path)
    elif isinstance(argument, list):
        timestamps = argument
    elif isinstance(argument, np.ndarray) and argument.ndim == 1:
        timestamps = argument
    else:
        raise ValueError("Argument must be a video file path, a list, or a 1D numpy array of timestamps.")

    # Ensure timestamps are in numpy format for consistency
    timestamps = np.array(timestamps)
    
    #Get timestamp differences
    delta_ts = np.diff(timestamps)
    
    #Estimate the "ideal" frame interval 
    ideal_frame_interval = np.median(delta_ts)
    expected_frame_rate = 1.0 / ideal_frame_interval
    threshold = deviation * ideal_frame_interval

    if verbose:
            print(f"Estimated frame rate: {expected_frame_rate:.4f} fps")
            print(f"Allowed deviation: {deviation*100:.2f}% ({threshold:.6f} s)")
    
    # Detect dropped or delayed frames
    did_deviate = False
    skipped_frames_index = []
    
    for i, delta in enumerate(delta_ts):
        if abs(delta - ideal_frame_interval) > threshold:
            did_deviate = True
            skipped_frames_index.append(i)
            if verbose:
                print(f"Dropped or delayed frame at index {i}: Δt = {delta:.6f}s")

    if verbose and not did_deviate:
        print("No dropped or delayed frames detected.")

    return did_deviate, skipped_frames_index

###############################################################################
#%% Coding For Thinking and Testing
      
