import os
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Union

from labchart_tools import RawReader, TrialCleaner


class LCDataViewer:
    def __init__(self, path:Union[str, os.PathLike]) -> None:
        self.__raw_reader = RawReader(path)
        self.__trial_cleaner = TrialCleaner(self.__raw_reader.run(), RawReader.time_col, RawReader.comment_col)
        self.__trial_cleaner.main()
    
    def plot(self, column_s:Union[str, List[str]]) -> List[go.Figure]:
        return self.__trial_cleaner.plot(column_s)
    
    def write_trial(self, trial_index:int, filename:str, ext='xlsx') -> None:
        self.__trial_cleaner.write_trial(trial_index, filename, ext)
