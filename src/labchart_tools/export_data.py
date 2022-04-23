import os
from labchart_tools import LabChart


def write_trials(df, time_col, signal_col, plot_dir, excel_dir):
    """Splits data into trials. Writes dataframes to Excel files and plots to plotly html files.

    :param df: Lab data, may contain several trials
    :type df: pandas DataFrame
    :param time_col: Name of time column in df
    :type time_col: str
    :param signal_col: Name of signal column in df to plot
    :type signal_col: str
    :param plot_dir: Name of directory to send plots to
    :type plot_dir: str
    :param excel_dir: Name of directory to send Excel files to
    :type excel_dir: str
    """

    # Split raw data into trials
    raw = LabChart(df, time_col)
    raw.split_trials()
    
    # Output html plots
    if plot_dir is not None and signal_col is not None:
        # Make directory if it doesn't exist
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        
        figs = raw.plot_trials(signal_col)
        [f.write_html(f'{plot_dir}/{signal_col}_trial{i}.html') for i, f in enumerate(figs)]

    # Ouput Excel files
    if excel_dir is not None:
        # Make directory if it doesn't exist
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)
        
        [df.to_excel(f'{excel_dir}/{signal_col}_trial{i}.xlsx', index=False) for i, df in enumerate(raw.trial_data)]
