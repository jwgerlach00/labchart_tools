import pandas as pd
import plotly.express as px
from typing import List, Union, Optional


class TrialCleaner:
    def __init__(self, df, time_col, comment_col=Optional[str]) -> List[pd.DataFrame]:
        self.df = df.copy()
        self.__time_col = time_col
        self.__comment_col = comment_col
        
        self.trial_data = []
        self.comments = pd.Series()
        self.plots = []
    
    @staticmethod
    def __get_start_indices(df:pd.DataFrame, time_col:str) -> List[int]:
        return list(df[df[time_col] == 0].index)
    
    @staticmethod
    def __get_comments(df:pd.DataFrame, comment_col:str) -> pd.Series:
        return df[comment_col].dropna()
    
    @staticmethod
    def __plot_trial(trial, time_column, column_s) -> px.Figure:
        return px.line(x=trial[time_column], y=trial[column_s])
    
    @staticmethod
    def split_trials(df:pd.DataFrame, time_col:str) -> List[pd.DataFrame]:
        start_indices = TrialCleaner.__get_start_indices(df, time_col)
        
        trial_data = []
        for n, start_inx in enumerate(start_indices):
            end_inx = start_indices[n + 1] if (n != len(start_indices) - 1) else len(df)
            trial_data.append(df.iloc[start_inx:end_inx])
        
        assert len(start_indices) == len(trial_data)  # Ensure that all the data is accounted for
        return trial_data
    
    def main(self) -> None:
        self.trial_data = TrialCleaner.split_trials(self.df, self.__time_col)
        
        if self.__comment_col:
            self.comments = TrialCleaner.__get_comments(self.df, self.__comment_col)
        
    def plot(self, column_s:Union[str, List[str]]) -> List[px.Figure]:
        figs = []
        for trial in self.trial_data:
            figs.append(TrialCleaner.__plot_trial(trial, self.__time_col, column_s))
        return figs
    
    def write_trial(self, trial_index, filename, ext='xlsx') -> None:
        if ext == 'xlsx':
            self.trial_data[trial_index].to_excel(f'{filename}.xlsx', index=False)
        elif ext == 'csv':
            self.trial_data[trial_index].to_csv(f'{filename}.csv', index=False)
        else:
            raise ValueError(f'{ext} is not a recognized file extension.')