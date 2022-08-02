from email import header
import os
from numpy import isin
import pandas as pd
from typing import List, Union, Optional
from werkzeug.datastructures import FileStorage


class RawReader:
    time_col = 'Time'
    comment_col = 'Comment'
    
    def __init__(self, path) -> pd.DataFrame:
        self.__path = path
    
    @staticmethod
    def __get_header(file:Union[str, os.PathLike], time_col:Optional[str]='Time',
                     comment_col:Optional[str]='Comment') -> List[str]:
        def header_loop(f):
            line = ''
            while 'ChannelTitle' not in line:
                line = f.readline().decode('utf-8').strip()  # Needs work
            return line.split('\t')[1:]
        
        if isinstance(file, str) or isinstance(file, os.PathLike):
            with open(file) as f:
                header = header_loop(f)
        elif isinstance(file, FileStorage):
            header = header_loop(file)
            
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
