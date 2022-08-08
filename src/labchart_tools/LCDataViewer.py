import os
import plotly.graph_objects as go
from typing import List, Union

import labchart_tools


class LCDataViewer:
    def __init__(self, path:Union[str, os.PathLike]) -> None:
        self.__raw_reader = labchart_tools.RawReader(path)
        self.__trial_cleaner = labchart_tools.TrialCleaner(self.__raw_reader.run(), self.__raw_reader.time_col,
                                                           self.__raw_reader.comment_col)
        self.__trial_cleaner.main()
        self.trial_data = self.__trial_cleaner.trial_data
    
    def plot(self, column_s:Union[str, List[str]]) -> List[go.Figure]:
        return self.__trial_cleaner.plot(column_s)
    
    def write_trial(self, trial_index:int, filename:str, ext='xlsx') -> None:
        self.__trial_cleaner.write_trial(trial_index, filename, ext)
