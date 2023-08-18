import datetime
import glob
from typing import List, Union
from pathlib import Path

import pandas as pd


def reformat_df(
    df_raw: pd.DataFrame,
    start_time: datetime.datetime = datetime.datetime(2022, 1, 1),
    end_time: datetime.datetime = datetime.datetime(2023, 1, 1),
    sampling_rate: datetime.timedelta = datetime.timedelta(minutes=15),
    ) -> pd.DataFrame:
    """Resample a dataframe containing measurements stacked in rows to a dataframe with columns for each measurement.
    Resample to a chosen sampling rate by calculating the weighed mean of measurement values.

    Args:
        df_raw (pd.DataFrame): 
        start_time (datetime.datetime, optional): _description_. Defaults to datetime.datetime(2022, 1, 1).
        end_time (datetime.datetime, optional): _description_. Defaults to datetime.datetime(2023, 1, 1).
        sampling_rate (datetime.timedelta, optional): _description_. Defaults to datetime.timedelta(minutes=15).

    Returns:
        pd.DataFrame: _description_
    """
    mmt_names = df_raw['SignalName'].unique()
    dfr_resampled_list = []
    for signalname in mmt_names:
        df_feature = df_raw[df_raw['SignalName'] == signalname]
        dfr_resampled = resample_df(df_feature, start_time, end_time, signalname, sampling_rate=sampling_rate)
        dfr_resampled_list.append(dfr_resampled.loc[:, ['WeighedMean']].rename(columns={'WeighedMean': signalname}))
    return pd.concat(dfr_resampled_list, axis=1, ignore_index=False)

def resample_df(df_raw: pd.DataFrame,
                start_time: datetime.datetime,
                end_time: datetime.datetime,
                signalname: str,
                sampling_rate: datetime.timedelta = datetime.timedelta(minutes=15)) -> pd.DataFrame:
    """
    Resamples a dataframe to a chosen sampling rate by calculating the weighed mean of measurement values.

    Args:
        df_raw: pandas dataframe with columns ['MeasurementValue', 'SignalName'] and Datetime index
        sampling_rate: datetime.timedelta with the sampling rate
        start_time: datetime.datetime to start sampling at
        end_time: datetime.datetime to end sampling at
        signalname: str with column for the signal

    Returns:
        df_resampled: resampled dataframe
    """
    df = df_raw.copy()
    signalid = df['SignalId'].iloc[0]
    dfaug_index = pd.date_range(start=start_time, end=end_time, freq=sampling_rate)
    dfaug = pd.DataFrame({'SignalId': signalid,
                          'SignalName': signalname,
                          'MeasurementValue': None,
                          'Counter': range(len(dfaug_index)),
                          'Zeros': 0}, index=dfaug_index)
    df = df[(df.index>=start_time)&(df.index<end_time)]
    df = pd.concat([df, dfaug]).sort_index()
    df = df.reset_index().drop_duplicates(subset='index', keep='last').set_index('index').sort_index() # remove duplicate index

    df['MeasurementValue'] = df['MeasurementValue'].interpolate(method='pad').interpolate(method='backfill')
    df['Counter'] = df['Counter'].interpolate(method='pad')

    df.loc[df.index[0], 'MeasurementValue'] = df.loc[df.index[1], 'MeasurementValue']
    df['delta'] = (df.index[1:] - df.index[0:-1]).append(pd.TimedeltaIndex([0]))
    df['ValueWeighed'] = df['delta'] * df['MeasurementValue'] / sampling_rate

    weighted_mean = df.groupby(by=['Counter'])['ValueWeighed'].rolling(sampling_rate).sum().shift(1)
    df['WeighedMean'] = weighted_mean.to_numpy()

    df_resampled = df[df['Zeros'] == 0].iloc[1:]
    return df_resampled

def reformat_df_commas(csv_path: Union[str, Path]):
    """Reformat csv file to semicolon separated columns.
    
    Args:
        csv_path (Tuple[str, Path]): Path to csv file(s) (can contain wildcards)
    """
    # read every csv in data folder as dataframe and write a new dataframe with semicolon separated columns in csv
    for file in glob.glob(csv_path):
        df = pd.read_csv(file, sep=',')
        df.to_csv(file, sep=';', index=False)
        print(f"Reformatted {file} to semicolon separated columns.")