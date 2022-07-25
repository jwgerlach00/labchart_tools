import unittest
import pandas as pd

from labchart_tools import RawReader, TrialCleaner


class TestTrialCleaner(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = './test/assets/raw_test_data.txt'
        
        cls.df = RawReader(path).run()
        cls.tc = TrialCleaner(cls.df, RawReader.time_col, RawReader.comment_col)
        return super().setUpClass()

    def test_split_trials(self):
        trials = TrialCleaner.split_trials(self.df, RawReader.time_col)
        
        self.assertIsInstance(
            trials,
            list
        )
        self.assertIsInstance(
            trials[0],
            pd.DataFrame
        )
        self.assertEqual(
            len(trials),
            3
        )
        [self.assertEqual(float(trial.iloc[0]['Time']), 0) for trial in trials]  # First time is 0

        
if __name__ == '__main__':
    unittest.main()
