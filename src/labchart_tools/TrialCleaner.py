import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Union, Optional


class TrialCleaner:
    def __init__(self, df, time_col, comment_col=Optional[str]) -> List[pd.DataFrame]:
        self.df = df.copy()
        self.__time_col = time_col
        self.__comment_col = comment_col
        
        self.trial_data = []
        self.comments = pd.Series()
        self.plots = []
        
        self.split_trials = self.__instance_split_trials
    
    @staticmethod
    def __get_start_indices(df:pd.DataFrame, time_col:str) -> List[int]:
        @np.vectorize
        def try_float(x):
            try: 
                return float(x) == float(0)
            except ValueError:
                return False
            
        return df[try_float(df[time_col])].index.tolist()
    
    @staticmethod
    def __get_end_indices(df:pd.DataFrame, time_col:str) -> List[int]:
        out = df[time_col][df[time_col] == 'Interval='].index.tolist()
        out = out[1:]  # Remove first bc of 0 time
        out.append(len(df) - 1)  # Add last index
        return out
    
    @staticmethod
    def __get_comments(df:pd.DataFrame, comment_col:str, split:bool=True) -> Union[List[Tuple[int, str]], pd.Series]:
        dropped = df[comment_col].dropna()
        if split:
            comments = dropped.tolist()
            indices = list(dropped.index)
            return [(i, c) for i, c in zip(indices, comments)]
        else:
            return dropped
    
    @staticmethod
    def __plot_trial(trial, time_column, column_s) -> go.Figure:
        return px.line(trial, x=time_column, y=column_s)
    
    @staticmethod
    def split_trials(df:pd.DataFrame, time_col:str) -> List[pd.DataFrame]:
        start_slices = TrialCleaner.__get_start_indices(df, time_col)
        end_slices = TrialCleaner.__get_end_indices(df, time_col)  # Dont need to add 1 for slicing bc it is where the \
            # interval is
        trial_data = [df.iloc[ss:es] for ss, es in zip(start_slices, end_slices)]
        
        assert len(start_slices) == len(end_slices) == len(trial_data)  # Ensure that all the data is accounted for
        return trial_data
    
    def __instance_split_trials(self) -> List[pd.DataFrame]:
        return TrialCleaner.split_trials(self.df, self.__time_col)
    
    def main(self) -> None:
        self.trial_data = TrialCleaner.split_trials(self.df, self.__time_col)
        
        if self.__comment_col:
            self.comments = [self.__get_comments(trial, self.__comment_col) for trial in self.trial_data]
        
    def plot(self, column_s:Union[str, List[str]]) -> List[go.Figure]:
        return [self.__plot_trial(trial, self.__time_col, column_s) for trial in self.trial_data]
    
    def write_trial(self, trial_index, filename, ext='xlsx') -> None:
        if ext == 'xlsx':
            self.trial_data[trial_index].to_excel(f'{filename}.xlsx', index=False)
        elif ext == 'csv':
            self.trial_data[trial_index].to_csv(f'{filename}.csv', index=False)
        else:
            raise ValueError(f'{ext} is not a recognized file extension.')
