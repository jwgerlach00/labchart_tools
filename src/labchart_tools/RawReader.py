import os
import pandas as pd
from typing import List, Union, Optional


class RawReader:
    time_col = 'Time'
    comment_col = 'Comment'
    
    def __init__(self, path) -> pd.DataFrame:
        self.__path = path
    
    @staticmethod
    def __get_header(path:Union[str, os.PathLike], time_col:Optional[str]='Time',
                     comment_col:Optional[str]='Comment') -> List[str]:
        with open(path) as f:
            line = ''
            while 'ChannelTitle' not in line:
                line = f.readline().strip()
            header = line.split('\t')[1:]
            
        if time_col:
            header.insert(0, time_col)
        if comment_col:
            header.append(comment_col)
        return header

    @staticmethod
    def read_raw_file(path:Union[str, os.PathLike]) -> pd.DataFrame:
        header = RawReader.__get_header(path, RawReader.time_col, RawReader.comment_col)
        return pd.read_csv(path, sep='\t', header=None, names=header)
    
    def run(self) -> pd.DataFrame:
        return RawReader.read_raw_file(self.__path)
