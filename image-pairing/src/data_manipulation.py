import pandas as pd
from numpy import timedelta64


class DataFrame():
    def __init__(self, csv_path, dropped_columns=[0, 1, 14]):
        # self.df = pd.read_csv(csv_path, header=None,
        #                       infer_datetime_format=True, index_col=2)
        self.df = pd.read_csv(csv_path, header=None,
                              infer_datetime_format=True)
        self.df = self.df.drop(dropped_columns, axis=1)

        self.df.columns = ["patientID"] + [
            f'date_{index:02d}' for index in range(1, len(self.df.columns))]

    def access_row_by_id(self, id):
        return self.df.loc[[id]].iloc[0]

    def access_row_by_index(self, index):
        return self.df.iloc[index]


def find_time_lapses(row, time_lapse_start=0.0, time_lapse_end=12.0, find_by='M'):
    time_lapse_indices = []
    # Without the patient ID
    dates = date_series_to_list(row) 
    for i in range(len(dates)):
        for j in range(i + 1, len(dates)):
            time_difference = date_difference(
                pd.to_datetime(dates[j]), pd.to_datetime(dates[i]), find_by)
            if time_lapse_start <= time_difference and time_difference <= time_lapse_end:
                time_lapse_indices.append([i, j])

    return time_lapse_indices


def date_series_to_list(date_series):
    return list(filter(lambda x: x != 'nan', map(str, list(date_series))))


def date_difference(date1, date2, difference_in='M'):
    return (date1 - date2) / timedelta64(1, difference_in)
