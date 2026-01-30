import pickle as pkl
import numpy as np

class Video:
    '''
    Description: Instances of Video will contain a numpy array of the video as well as relevant 
    video metadata as attributes.

    Attributes:
        dataset: a string identifying which dataset the video originates.
        length:  a float with the length of the video in seconds.
        frames:  a 3-dimensional numpy array where axis 0 is time, axis 1 is the horizontal axis of video
            frame and axis 2 is the vertical axis. 

    Methods:
        download_video: extracts video from specified path and saves in attribute 'frames'.
        identify_dropped: identifies dropped frames and returns idxs and number of frames dropped.
        insert_dropped: inserts null frames where frames were dropped in the camera logs.
        sync_to_house: syncs cameras to housekeeping time.
        pickle_video: saves instance of Video as .pickle file.

    '''
    def __init__(
        self,
        dataset: str,
        length: float,
        frames: np.ndarray
    ):
        self.dataset = dataset
        self.length = length
        self.frames = None

    def download_video(
        self, 
        path
    ):
        '''
        Description: extracts video file from path specified in 'path' and saves in attribute
        'frames' as a 3d numpy array, where axis 0 is time, axis 1 is the horizontal axis of video
        frame and axis 2 is the vertical axis.
        '''
        return self

    def identify_dropped(
        self, 
        log_path
    ):
        '''
        Description: Reads camera log file and finds where and how many frames were dropped.
        '''
        pass

    def insert_dropped(
        self, 
        dropped_idxs: list, 
        nums_dropped: list
    ):
        '''
        Description: Inserts matrix of zeros where frames were dropped into the frames attribute.
        '''
        pass

    def sync_to_house(
        self, 
        house_path
    ):
        '''
        Description: Syncs the camera times to housekeeping times so they can be directly compared.
        '''
        pass

    def pickle_video(
        self, 
        save_dir
    ):
        '''
        Description: Saves class instance as a .pickle file to directory specified by 'save_dir'.
        '''
        pass


class Scan:
    '''
    Description:
    Attributes:
    '''
    def __init__(
        self,
        depth: float,
        speed: float,
        videos: list
    ):
        pass
