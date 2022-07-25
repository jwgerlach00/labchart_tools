import unittest
import pandas as pd

from labchart_tools import RawReader


class TestRawReader(unittest.TestCase):
    def test_run(self):
        path = './test/assets/raw_test_data.txt'
        rr = RawReader(path)
        out = rr.run()
        
        self.assertIsInstance(
            out,
            pd.DataFrame
        )
        self.assertEqual(
            list(out.columns),
            ['Time', 'Flow', 'Volume', 'Comment']
        )
        self.assertEqual(  # 4 comments
            len(out['Comment'].dropna()),
            4
        )
        print(out['Comment'].dropna())
    
    
if __name__ == '__main__':
    unittest.main()
