import unittest
import plotly.graph_objects as go

from labchart_tools import LCDataViewer


class TestLCDataViewer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = './test/assets/raw_test_data.txt'
        cls.lc_dv = LCDataViewer(path)
        return super().setUpClass()
    
    def test_plot(self):
        plots = self.lc_dv.plot(['Flow', 'Volume'])
        
        self.assertEqual(
            len(plots),
            3
        )
        [self.assertIsInstance(
            plot,
            go.Figure
        ) for plot in plots]
        
        
if __name__ == '__main__':
    unittest.main()
