import datetime
import glob
from typing import List, Union, Literal
from pathlib import Path

import numpy as np
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
                sampling_rate: datetime.timedelta = datetime.timedelta(minutes=15),
) -> pd.DataFrame:
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


def replace_commas(csv_path: Union[str, Path]):
    """Reformat csv file to semicolon separated columns.
    
    Args:
        csv_path (Tuple[str, Path]): Path to csv file(s) (can contain wildcards)
    """
    # read every csv in data folder as dataframe and write a new dataframe with semicolon separated columns in csv
    for file in glob.glob(csv_path):
        df = pd.read_csv(file, sep=',')
        df.to_csv(file, sep=';', index=False)
        print(f"Reformatted {file} to semicolon separated columns.")
        
        
def read_and_resample_mmts(
    csv_path: Union[str, Path],
    start_time: datetime.datetime = datetime.datetime(2022, 1, 1),
    end_time: datetime.datetime = datetime.datetime(2023, 1, 1),
) -> pd.DataFrame:
    """
    Reads a CSV file containing substation measurement data, resamples it to a fixed frequency of 15min, 
    and returns a pandas DataFrame.

    Args:
        csv_path (Union[str, Path]): The path to the CSV file.
        start_time (datetime.datetime, optional): The start time of the resampled data. Defaults to datetime.datetime(2022, 1, 1).
        end_time (datetime.datetime, optional): The end time of the resampled data. Defaults to datetime.datetime(2023, 1, 1).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the resampled MMTS data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the start time is after the end time.

    Example:
        >>> csv_path = 'data/mmts.csv'
        >>> start_time = datetime.datetime(2022, 1, 1)
        >>> end_time = datetime.datetime(2023, 1, 1)
        >>> df = read_and_resample_mmts(csv_path, start_time, end_time)
    """
    raw_df = pd.read_csv(csv_path, index_col='Ts', sep=';', 
        dtype={
            'Ts': 'str',
            'SignalName': 'str',
            'SignalId': 'int32',
            'MeasurementValue': 'float32',
            'Ts_day': 'int32',
        },
        decimal=',',
        )
    raw_df.index = pd.to_datetime(raw_df.index)
    resampled_df = reformat_df(raw_df, start_time, end_time)
    
    return resampled_df 


def read_and_resample_prod(
    csv_path: Union[str, Path],
    sampling_rate: datetime.timedelta = datetime.timedelta(minutes=15),
) -> pd.DataFrame:
    """
    Reads a CSV file containing production data, resamples it to a fixed frequency, and returns a pandas DataFrame.

    Args:
        csv_path (Union[str, Path]): The path to the CSV file.
        sampling_rate (datetime.timedelta, optional): The sampling rate of the resampled data. 
            Defaults to datetime.timedelta(minutes=15).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the resampled production data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.

    Example:
        >>> csv_path = 'data/production.csv'
        >>> sampling_rate = datetime.timedelta(minutes=15)
        >>> df = read_and_resample_prod(csv_path, sampling_rate)
    """
    # Read the raw data from the CSV file
    prod = pd.read_csv(csv_path, index_col=0, sep=';')

    # Convert the index to datetime and remove the ' - Actual Aggregated' suffix from column names
    prod.index = pd.to_datetime(prod.index.str[19:35], format="%d.%m.%Y %H:%M")
    prod.rename(
        columns=dict(zip(list(prod.columns), 
                         map(lambda x: x.replace('  - Actual Aggregated', ''), list(prod.columns)))), 
        inplace=True)    

    # Resample the data to the specified sampling rate and fill missing values
    resampled_df = prod.resample(sampling_rate).mean().ffill()
    
    return resampled_df


def read_and_resample_weather(
    csv_path: Union[str, Path],
    sampling_rate: datetime.timedelta = datetime.timedelta(minutes=15),
) -> pd.DataFrame:
    """_summary_

    Args:
        csv_path (Union[str, Path]): _description_
        sampling_rate (datetime.timedelta, optional): _description_. Defaults to datetime.timedelta(minutes=15).

    Returns:
        pd.DataFrame: _description_
    """
    weather = pd.read_csv(csv_path, index_col=0, skiprows=9)
    weather.index = pd.to_datetime(weather.index, format="%Y%m%dT%H%M")
    weather.rename(
        columns=dict(zip(list(weather.columns), 
                         map(lambda x: x.replace('Basel ', ''), list(weather.columns)))), 
        inplace=True)  
    resampled_df = weather.resample(sampling_rate).mean().bfill()
    
    return resampled_df


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds temporal features to a pandas DataFrame.

    The function adds four new columns to the input DataFrame, representing the hour of the day and the day of the year
    as sine and cosine functions. These features can be useful for time series analysis and modeling.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A new DataFrame with the added temporal features.

    Example:
        >>> df = pd.read_csv('data.csv', index_col='timestamp')
        >>> df_with_temporal_features = add_temporal_features(df)
    """
    holidays = ['01.01.2022', '15.04.2022', '18.04.2022', '01.05.2022', '26.05.2022',
                '06.06.2022', '01.08.2022', '15.08.2022', '18.09.2022', '25.12.2022', '26.12.2022',
                '01.01.2023', '14.04.2023', '17.04.2023', '01.05.2023', '25.05.2023']
    holidays = pd.to_datetime(holidays, format='%d.%m.%Y')
    df_temporal = df.copy()
    df_temporal['hour_sin'] = np.sin(2 * np.pi * (df_temporal.index.hour*60 + df_temporal.index.minute)/24.0/60)
    df_temporal['hour_cos'] = np.cos(2 * np.pi * (df_temporal.index.hour*60 + df_temporal.index.minute)/24.0/60)
    df_temporal['dayofyear_sin'] = np.sin(2 * np.pi * (df_temporal.index.dayofyear)/365)
    df_temporal['dayofyear_cos'] = np.cos(2 * np.pi * (df_temporal.index.dayofyear)/365)
    df_temporal['dayofweek_sin'] = np.sin(2 * np.pi * (df_temporal.index.dayofweek)/7)
    df_temporal['dayofweek_cos'] = np.cos(2 * np.pi * (df_temporal.index.dayofweek)/7)
    
    # mark as holiday if timestamp is in holidays or weekend
    df_temporal['holiday'] = df_temporal.index.isin(holidays) | df_temporal.index.dayofweek.isin([5, 6])
    
    return df_temporal
    

def get_data_df(
    split: Literal['train', 'val'], 
    station: Literal['A', 'B'],
) -> pd.DataFrame:
    """Reads the data from the CSV files and returns a pandas DataFrame for the specified split.
    
    Args:
        split (Literal['train', 'val']): The split to return the data for.
        station (Literal['A', 'B']): The station to return the data for.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing the data for the specified split.
    """
    if split == 'train':
        start_time = datetime.datetime(2022, 1, 1)
        end_time = datetime.datetime(2022, 12, 31)
    elif split == 'val':
        start_time = datetime.datetime(2023, 1, 1)
        end_time = datetime.datetime(2023, 4, 1)
    else:
        raise ValueError(f'Invalid split: {split}')
    
    weather_ch = read_and_resample_weather(f'data/CH_basel_weather_data_{split}_utc.csv')
    station = read_and_resample_mmts(f'data/station{station}_{split}_utc.csv', start_time, end_time)
    prod_ch = read_and_resample_prod(f'data/CH_generation_{split}_utc.csv')
    prod_de = read_and_resample_prod(f'data/DE_generation_{split}_utc.csv')
    joined_df = pd.concat([station, prod_ch.add_prefix('CH '), prod_de.add_prefix('DE '), weather_ch], axis=1, join='inner')
    
    return joined_df