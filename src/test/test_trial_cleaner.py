import unittest
import numpy as np
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
        [self.assertEqual(
            float(trial.iloc[0]['Time']),
            0
        ) for trial in trials]  # First time is 0
        
    def test_main(self):
        self.tc.main()
        trials_st = TrialCleaner.split_trials(self.df, RawReader.time_col)
        
        [self.assertTrue(
            trial_data.equals(trial_st)
        ) for trial_data, trial_st in zip(self.tc.trial_data, trials_st)]
        self.assertEqual(
            len(self.tc.comments),
            3  # 3 trials
        )
        self.assertEqual(
            len(self.tc.comments[1]),
            2  # 2 comments in second trial
        )
        self.assertEqual(
            len(self.tc.comments[1][0]),
            2  # Tuple of (index, comment)
        )
        
    def test_plot(self):
        self.tc.trial_data = TrialCleaner.split_trials(self.df, RawReader.time_col)
        figs = self.tc.plot(['Flow', 'Volume'])
        
        # X data
        [self.assertTrue(  # Flow column
            np.array_equal(
                fig['data'][0]['x'],
                self.tc.trial_data[i][RawReader.time_col].values
            )
        ) for i, fig in enumerate(figs)]
        [self.assertTrue(  # Volume column
            np.array_equal(
                fig['data'][1]['x'],
                self.tc.trial_data[i][RawReader.time_col].values
            )
        ) for i, fig in enumerate(figs)]
        
        # Y data
        [self.assertTrue(  # Flow column
            np.array_equal(
                fig['data'][0]['y'].astype(float),
                self.tc.trial_data[i]['Flow'].astype(float).values
            )
        ) for i, fig in enumerate(figs)]
        [self.assertTrue(  # Volume column
            np.array_equal(
                fig['data'][1]['y'],
                self.tc.trial_data[i]['Volume'].values
            )
        ) for i, fig in enumerate(figs)]

        
if __name__ == '__main__':
    unittest.main()
