"""
Functions for loading data downloaded from the PPMI database
"""

from functools import reduce
import itertools
import os
import re
from typing import List

import numpy as np
import pandas as pd

from _info2021 import BEHAVIORAL_INFO, DEMOGRAPHIC_INFO, VISITS, GENOTYPES_INFO, PRODROMAL_INFO, PRODROMAL_BERG2015
from _utils import _get_data_dir


def load_biospecimen(path: str = None,
                     measures: List[str] = None) -> pd.DataFrame:
    """
    Loads biospecimen data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. There are a number of
        biospecimen measures that are missing for large numbers of subjects, so
        if not specified only those that are present in at least 80% of entries
        are kept. Specifying `measures='all'` will retain everything, but this
        will significantly increase load time. It is highly recommended to
        specify which measures to keep; available biospecimen measures can be
        viewed with :py:func:`pypmi.available_biospecimen`. Default: None
    Returns
    -------
    data : :obj:`pandas.DataFrame`
        Biospecimen data
    See Also
    --------
    pypmi.available_biospecimen
    """

    rename_cols = dict(PATNO='participant', CLINICAL_EVENT='visit',
                       TESTNAME='test', TESTVALUE='score',TYPE='type')
    dtype = dict(PATNO=int, CLINICAL_EVENT=VISITS, TESTNAME=str, TESTVALUE=str)

    # check for file and get data directory path
    fname = 'Current_Biospecimen_Analysis_Results.csv'
    path = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

    # load data, make scores numeric, and clean up test names (no spaces!)
    data = pd.read_csv(path, dtype=dtype, usecols=rename_cols.keys())
    print(data)
    data = data.rename(columns=rename_cols)
    data['score'] = data['score'].replace(['Negative','Positive'],[0,1])
    data['score'] = pd.to_numeric(data['score'], errors='coerce')
    data['test'] = data['test'].apply(lambda x: x.replace(' ', '_').lower())
    data = data[data['type']=='Cerebrospinal Fluid']
    # keep only desired measures
    if measures is None:
        measures = ['abeta_1-42', 'csf_alpha-synuclein', 'ptau', 'ttau','gfap','nfl','amprion-alpha-synuclein-saa_qualitative_(rep1)',
                   'amprion-alpha-synuclein-saa_fmax_(rep1)','amprion-alpha-synuclein-saa_fmax_(rep2)','amprion-alpha-synuclein-saa_fmax_(rep3)']
    elif isinstance(measures, str) and measures == 'all':
        measures = data['test'].unique().tolist()
    print(measures)
    data = data.query(f'test in {measures}')

    # convert to tidy dataframe
    tidy = data.groupby(['participant', 'visit', 'test']) \
               .agg({'score': np.nanmean}) \
               .unstack(level='test') \
               .get('score') \
               .reset_index() \
               .rename_axis(None, axis=1)

    # (try to) add visit date information
    print(tidy)
    tidy = _add_dates(tidy, path="/scratch/c.c21013066/data/ppmi/phenotypes2023",#os.path.dirname(path),
                      fnames=['Lumbar_Puncture.csv'])
    if 'amprion-alpha-synuclein-saa_qualitative_(rep1)' in tidy.columns:
        tidy = tidy.rename(columns={'amprion-alpha-synuclein-saa_qualitative_(rep1)':'SAA_positive',
                                   'amprion-alpha-synuclein-saa_fmax_(rep1)':'SAA_Fmax1',
                                   'amprion-alpha-synuclein-saa_fmax_(rep2)':'SAA_Fmax2',
                                   'amprion-alpha-synuclein-saa_fmax_(rep3)':'SAA_Fmax3'})
    print(tidy)

    return tidy.sort_values(['participant', 'visit']).reset_index(drop=True)

def load_SAA(path: str = None,
                     measures: List[str] = None) -> pd.DataFrame:
    """
    Loads biospecimen data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. There are a number of
        biospecimen measures that are missing for large numbers of subjects, so
        if not specified only those that are present in at least 80% of entries
        are kept. Specifying `measures='all'` will retain everything, but this
        will significantly increase load time. It is highly recommended to
        specify which measures to keep; available biospecimen measures can be
        viewed with :py:func:`pypmi.available_biospecimen`. Default: None
    Returns
    -------
    data : :obj:`pandas.DataFrame`
        Biospecimen data
    See Also
    --------
    pypmi.available_biospecimen
    """

    rename_cols = dict(PATNO='participant', CLINICAL_EVENT='visit',SAAMethod='test',FmaxRep1='SAA_Fmax1', FmaxRep2='SAA_Fmax2', FmaxRep3='SAA_Fmax3',QUALRep1='SAA_positive')
    dtype = dict(PATNO=int, CLINICAL_EVENT=VISITS)

    # check for file and get data directory path
    fname = 'SAA_Internal_20231102.csv'
    path = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

    # load data, make scores numeric, and clean up test names (no spaces!)
    data = pd.read_csv(path, usecols=rename_cols.keys())
    data = data.rename(columns=rename_cols)
    data = data[data['test']=='Amprion-Alpha-synuclein-SAA']
    data['SAA_positive'] = data['SAA_positive'].replace(['Negative','Positive'],[0,1])
    data[['SAA_positive','SAA_Fmax1','SAA_Fmax2','SAA_Fmax3']] = data[['SAA_positive','SAA_Fmax1','SAA_Fmax2','SAA_Fmax3']].apply(pd.to_numeric, errors='coerce')
    data['test'] = data['test'].apply(lambda x: x.replace(' ', '_').lower())

    # (try to) add visit date information
    idy = _add_dates(tidy, path="/scratch/c.c21013066/data/ppmi/phenotypes2021",#os.path.dirname(path),
                      fnames=['Lumbar_Puncture.csv'])
    data['participant'] = data['participant'].astype(int)

    return data.sort_values(['participant', 'visit']).reset_index(drop=True)


def available_biospecimen(path: str = None) -> List[str]:
    """
    Lists measures available in :py:func:`pypmi.load_biospecimen`
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    Returns
    -------
    measures : list
        Available biospecimen measures (i.e., "tests")
    See Also
    --------
    pypmi.load_biospecimen
    """

    # check for file and get data directory path
    fname = 'Current_Biospecimen_Analysis_Results_12Jul2023.csv'
    path = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

    data = pd.read_csv(path, usecols=['TESTNAME'])['TESTNAME'].unique()

    return sorted(list(set([f.replace(' ', '_').lower() for f in data])))

def load_imaging(path: str = None,
                     measures: List[str] = None) -> pd.DataFrame:
    """
    Loads biospecimen data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. There are a number of
        biospecimen measures that are missing for large numbers of subjects, so
        if not specified only those that are present in at least 80% of entries
        are kept. Specifying `measures='all'` will retain everything, but this
        will significantly increase load time. It is highly recommended to
        specify which measures to keep; available biospecimen measures can be
        viewed with :py:func:`pypmi.available_biospecimen`. Default: None
    Returns
    -------
    data : :obj:`pandas.DataFrame`
        Imaging data
    See Also
    --------
    pypmi.available_imaging
    """

    rename_cols = dict(PATNO='participant', CLINICAL_EVENT='visit')
    dtype = dict(PATNO=int, CLINICAL_EVENT=VISITS)

    # check for file and get data directory path
    fname = 'Grey_Matter_Volume.csv'
    path = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

    # load data, make scores numeric, and clean up test names (no spaces!)
    data = pd.read_csv(path, dtype=dtype)
    data = data.rename(columns=rename_cols)
    data = data.rename(columns={'MRIDATE':'date','GM_VALUE':'greymatter'})

    return data.sort_values(['participant', 'visit']).reset_index(drop=True)


def available_imaging(path: str = None) -> List[str]:
    """
    Lists measures available in :py:func:`pypmi.load_imaging`
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    Returns
    -------
    measures : list
        Available imaging measures
    See Also
    --------
    pypmi.load_imaging
    """

    return ['greymatter']


def load_datscan(path: str = None,
                 measures: List[str] = None) -> pd.DataFrame:
    """
    Loads DaT scan data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available DaT scan measures can be viewed with
        :py:func:`pypmi.available_datscan`. Default: None
    Returns
    -------
    data : :obj:`pandas.DataFrame`
        DaTScan data
    See Also
    --------
    pypmi.available_datscan
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit', DATSCAN_DATE='date')
    dtype = dict(PATNO=int, EVENT_ID=VISITS, SCAN_DATE=str)

    # check for file and get data directory path
    fname = 'DaTScan_Analysis.csv'
    path = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

    # load data and coerce into standard format
    raw = pd.read_csv(path)
    print(raw.head())
    raw = pd.read_csv(path, dtype=dtype)
    tidy = raw.rename(columns=rename_cols).dropna(subset=['visit'])
    tidy.columns = [f.lower() for f in tidy.columns]
    # keep only desired measures
    if measures is not None:
        if isinstance(measures, str) and measures == 'all':
            measures = available_datscan(path=os.path.dirname(path))
        elif not isinstance(measures, list):
            measures = list(measures)
        for m in measures:
            if m not in tidy.columns:
                raise ValueError('Specified measure {} is not valid. Please '
                                 'see available datscan measures with `pypmi.'
                                 'available_datscan()`.'.format(m))
        tidy = tidy[['participant', 'visit','date'] + measures]
    if 'date' in tidy.columns:
        tidy['date'] = pd.to_datetime(tidy['date'], format='%m/%Y',
                                      errors='coerce')
    else:
        tidy = _add_dates(tidy, path=os.path.dirname(path))

    return tidy.sort_values(['participant', 'visit']).reset_index(drop=True)

def load_datscan_all(path: str = None,
                 measures: List[str] = None) -> pd.DataFrame:
    """
    Loads DaT scan data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available DaT scan measures can be viewed with
        :py:func:`pypmi.available_datscan`. Default: None
    Returns
    -------
    data : :obj:`pandas.DataFrame`
        DaTScan data
    See Also
    --------
    pypmi.available_datscan
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit', DATSCAN_DATE='date')
    dtype = dict(PATNO=int, EVENT_ID=VISITS, SCAN_DATE=str)

    # check for file and get data directory path
    fnames = ['DaTScan_Analysis.csv','DaTscan/inv_spect_sbr_sequestered_merge_20231026.csv']
    tidies = []
    for fname in fnames:
        file = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

        # load data and coerce into standard format
        raw = pd.read_csv(file, dtype=dtype)
        tidy = raw.rename(columns=rename_cols).dropna(subset=['visit'])
        tidy.columns = [f.lower() for f in tidy.columns]
        # keep only desired measures
        if measures is not None:
            if isinstance(measures, str) and measures == 'all':
                measures = available_datscan(path=os.path.dirname(path))
            elif not isinstance(measures, list):
                measures = list(measures)
            for m in measures:
                if m not in tidy.columns:
                    raise ValueError('Specified measure {} is not valid. Please '
                                     'see available datscan measures with `pypmi.'
                                     'available_datscan()`.'.format(m))
            tidy = tidy[['participant', 'visit','date'] + measures]
        if 'date' in tidy.columns:
            tidy['date'] = pd.to_datetime(tidy['date'], format='%m/%Y',
                                          errors='coerce')
        else:
            tidy = _add_dates(tidy, path=os.path.dirname(path))
        tidies.append(tidy)
    tidies = pd.concat(tidies)
    tidies = tidies.drop_duplicates()
    return tidies.sort_values(['participant', 'visit']).reset_index(drop=True)



def available_datscan(path: str = None) -> List[str]:
    """
    Lists measures available in :py:func:`pypmi.load_datscan`
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    Returns
    -------
    measures : list
        Available DaT scan measures
    See Also
    --------
    pypmi.load_datscan
    """

    # check for file and get data directory path
    fname = 'DaTScan_Analysis.csv'
    path = os.path.join(_get_data_dir(path=path, fnames=[fname]), fname)

    # only need first line!
    with open(path, 'r') as src:
        data = src.readline().strip().replace('"', '').split(',')[3:-3]
    print(data)

    if 'DATSCAN_DATE' in data:
        data = data[1:]

    return sorted([f.lower() for f in data])


def load_behavior(path: str = None,
                  measures: List[str] = None) -> pd.DataFrame:
    """
    Loads clinical-behavioral data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available behavioral measures can be viewed with
        :py:func:`pypmi.available_behavior`. Default: None
    Returns
    -------
    df : :obj:`pandas.DataFrame`
        Tidy DataFrame with all clinical-behavioral assessments
    See Also
    --------
    pypmi.available_behavior
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit', INFODT='date')

    # determine measures
    if measures is not None:
        if isinstance(measures, str) and measures == 'all':
            beh_info = BEHAVIORAL_INFO
        else:
            beh_info = {d: v for d, v in BEHAVIORAL_INFO.items()
                        if d in measures}
        if 'moca' not in beh_info.keys() and 'education' in beh_info.keys():
            del beh_info['education']
    else:
        beh_info = BEHAVIORAL_INFO

    if len(beh_info) == 0:
        return pd.DataFrame(columns=['participant', 'visit', 'date'])

    # check for files and get data directory path
    fnames = []
    for info in beh_info.values():
        fnames.extend(list(info.get('files', {}).keys()))
    path = _get_data_dir(path=path, fnames=set(fnames))

    df = pd.DataFrame()
    # iterate through all keys in dictionary
    for key, info in beh_info.items():
        print(key)
        cextra = info.get('extra', ['PATNO', 'EVENT_ID', 'INFODT','PAG_NAME'])
        capply = info.get('applymap', itertools.repeat(lambda x: x))
        copera = info.get('operation', itertools.repeat(np.sum))

        temp_scores = []
        # go through relevant files and items for current key and grab scores
        for fname, items in info['files'].items():
            # read in file
            data = pd.read_csv(os.path.join(path, fname),na_values=['UR']) # needed as for one participant in UPDRSIII file one value UR instead of numeric
            # iterate through items to be retrieved and apply operations
            for n, (it, ap, ope) in enumerate(zip(items, capply, copera)):
                score = ope(data[it].applymap(ap), axis=1)
                temp_scores.append(data[cextra].join(pd.Series(score, name=n)))

        # merge temp score DataFrames
        curr_df = reduce(lambda df1, df2: pd.merge(df1, df2, on=cextra),
                         temp_scores)
        # combine individual scores for key with joinfunc and add to extra info
        joinfunc = info.get('joinfunc', np.sum)
        score = pd.Series(joinfunc(curr_df.drop(cextra, axis=1), axis=1)
                          .astype('float'), name='score')
        curr_df = curr_df[cextra].astype('str').join(score).assign(test=key)
        # append resultant DataFrame to df
        df = df.append(curr_df, ignore_index=True, sort=True)
    print(df[np.logical_and(df['test']=='tremor_NoMED',df['PATNO']=='3002')])
    print(df[np.logical_and(df['test']=='updrs_iii_NoMED',df['PATNO']=='3002')])
    print(df[np.logical_and(df['test']=='moca',df['PATNO']=='3002')])
    # rename post-treatment UDPRS III scores so there's no collision
    # pivot_table would average between the two by default. we don't want that!
    #df.loc[df['test'] == "updrs_iii", 'test'] = 'updrs_iii_a'
    df.loc[np.logical_and(df['test'].str.contains('(_OFF)|(_ON)|(_NoMED)|(_A)'),df['score']<=0),'score'] = np.nan

    print(df[np.logical_and(df['test']=='tremor_NoMED',df['PATNO']=='3002')])
    # clean up column names and convert to tidy dataframe
    df = df.rename(columns=rename_cols)
    tidy = pd.pivot_table(df, index=['participant', 'visit', 'date'],
                          columns='test', values='score',aggfunc='mean').reset_index()
    tidy = tidy.rename_axis(None, axis=1)

    # get adjusted MOCA scores (add 'education' variable)
    if 'moca' in tidy.columns:
        adjust = tidy['moca'] < 30
        tidy.loc[adjust, 'moca'] += tidy.loc[adjust, 'education'].fillna(0)
        tidy = tidy.drop(['education'], axis=1)

    # coerce data types to desired format
    tidy['participant'] = tidy['participant'].astype(int)
    tidy['visit'] = tidy['visit'].astype(VISITS)
    tidy['date'] = pd.to_datetime(tidy['date'], format='%m/%Y',
                                  errors='coerce')
    tidy[tidy.filter(regex='state_').columns] = tidy[tidy.filter(regex='state_').columns].replace([1,2],['OFF','ON'])

    return tidy.sort_values(['participant', 'visit']).reset_index(drop=True).set_index(['participant','visit'])


def available_behavior(path: str = None) -> List[str]:
    """
    Lists measures available in :py:func:`pypmi.load_behavior`
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    Returns
    -------
    measures : list
        Available behavioral measures
    See Also
    --------
    pypmi.load_behavior
    """

    measures = sorted(list(BEHAVIORAL_INFO.keys()))
    measures.remove('education')

    return measures


def load_demographics(path: str = None,
                      measures: List[str] = None) -> pd.DataFrame:
    """
    Loads demographic data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available demographics measures can be viewed
        with :py:func:`pypmi.available_demographics`. Default: None
    Returns
    -------
    demographics : :obj:`pandas.DataFrame`
        Tidy data frame containing demographic information for PPMI subjects
    See Also
    --------
    pypmi.available_demographics
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit')
    dtype = dict(PATNO=int)

    # determine measures
    if measures is not None:
        if isinstance(measures, str) and measures == 'all':
            dem_info = DEMOGRAPHIC_INFO
        else:
            dem_info = {d: v for d, v in DEMOGRAPHIC_INFO.items()
                        if d in measures}
    else:
        dem_info = DEMOGRAPHIC_INFO

    # check for files and get data directory path
    fnames = []
    for info in dem_info.values():
        fnames.extend(list(info.get('files', {}).keys()))
    path = _get_data_dir(path=path, fnames=set(fnames))

    # empty data frame to hold information
    tidy = pd.DataFrame([], columns=['PATNO'])

    # iterate through demographic info to wrangle
    for key, curr_key in dem_info.items():
        for n, (fname, items) in enumerate(curr_key['files'].items()):
            data = pd.read_csv(os.path.join(path, fname), dtype=dtype)
            curr_score = data[items]
            for attr in [f for f in curr_key.keys() if f not in ['files']]:
                if hasattr(curr_score, attr):
                    fnc = getattr(curr_score, attr)
                    curr_score = fnc(curr_key[attr].get('input', None),
                                     **curr_key[attr].get('kwargs', {}))
            curr_score = pd.Series(curr_score, name=key)
            temp_scores = data[['PATNO']].join(curr_score)
        tidy = pd.merge(tidy, temp_scores, on='PATNO', how='outer')

    # rename columns and remove duplicates (how are there duplicates???)
    tidy = (tidy.rename(columns=rename_cols)
                .drop_duplicates(subset=['participant']))

    return tidy.sort_values('participant').reset_index(drop=True)


def available_demographics(path: str = None) -> List[str]:
    """
    Lists measures available in :py:func:`pypmi.load_demographics`
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    Returns
    -------
    measures : list
        Available demographic measures
    See Also
    --------
    pypmi.load_demographics
    """

    return list(DEMOGRAPHIC_INFO.keys())


def _load_dates(path: str = None,
                fnames: List[str] = None) -> pd.DataFrame:
    """
    Loads visit date information into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    fnames : list, optional
        List of PPMI data files that may contain additional date information
        beyond the "default" files used (i.e., Inclusion_Exclusion.csv,
        Signature_Form.csv', Socio-Economics.csv, and Vital_Signs.csv). If not
        specified only default files are used. Default: None
    Returns
    -------
    dates : :obj:`pandas.DataFrame`
        Tidy data frame with columns ['participant', 'visit', 'date'] for
        linking each visit (valued as e.g., "V01", "V02") with a specific
        YYYY-MM-DD date
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit', INFODT='date')
    dtype = dict(PATNO=int, EVENT_ID=VISITS)

    # check for file and get data directory path
    # we use four files to try and capture as much "visit date" info:
    files = [
        'Inclusion_Exclusion.csv',
        'Socio-Economics.csv',
        'Vital_Signs.csv',
        #'Signature_Form.csv',
    ]
    # add additional files as needed by datatype and then get data path
    if fnames is not None:
        files = fnames + files
    path = _get_data_dir(path=path, fnames=files)
    print(path)

    # load data and coerce into standard format
    raw = [pd.read_csv(os.path.join(path, f),
                       dtype=dtype,
                       usecols=rename_cols.keys()) for f in files]
    tidy = (pd.concat(raw).rename(columns=rename_cols)
                          .get(list(rename_cols.values()))
                          .dropna()
                          .drop_duplicates(subset=['participant', 'visit']))
    tidy['date'] = pd.to_datetime(tidy['date'], format='%m/%Y',
                                  errors='coerce')

    return tidy.sort_values(['participant', 'visit']).reset_index(drop=True)


def _add_dates(df: pd.DataFrame,
               path: str = None,
               fnames: List[str] = None) -> pd.DataFrame:
    """
    Attempts to add visit date to information to dataframe `df`
    If files required for visit date information cannot be found then `df` is
    returned, unaltered
    Parameters
    ----------
    df : :obj:`pandas.DataFrame`
        Data frame to add date information to
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    fnames : list, optional
        List of PPMI data files that may contain additional date information
        beyond the "default" files used (i.e., Inclusion_Exclusion.csv,
        Signature_Form.csv', Socio-Economics.csv, and Vital_Signs.csv). If not
        specified only default files are used. Default: None
    Returns
    -------
    df : :obj:`pandas.DataFrame`
        Provided `df` with new 'date' columns
    """

    try:
        tidy = pd.merge(df, _load_dates(path=path, fnames=fnames),
                        on=['participant', 'visit'], how='left')
        # reorder columns so that 'participant', 'visit', and 'date' are first
        cols = ['participant', 'visit', 'date']
        tidy = tidy[cols + np.setdiff1d(tidy.columns, cols).tolist()]
    except FileNotFoundError:
        tidy = pd.DataFrame()

    return tidy

def load_genotypes(path: str = None,
                      measures: List[str] = None) -> pd.DataFrame:
    """
    Loads genotypes data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available demographics measures can be viewed
        with :py:func:`pypmi.available_demographics`. Default: None
    Returns
    -------
    demographics : :obj:`pandas.DataFrame`
        Tidy data frame containing demographic information for PPMI subjects
    See Also
    --------
    pypmi.available_demographics
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit')
    dtype = dict(PATNO=int)

    # determine measures
    if measures is not None:
        if isinstance(measures, str) and measures == 'all':
            gen_info = GENOTYPES_INFO
        else:
            gen_info = {d: v for d, v in GENOTYPES_INFO.items()
                        if d in measures}
    else:
        gen_info = GENOTYPES_INFO

    # check for files and get data directory path
    fnames = []
    for info in gen_info.values():
        fnames.extend(list(info.get('files', {}).keys()))
    path = _get_data_dir(path=path, fnames=set(fnames))

    # empty data frame to hold information
    tidy = pd.DataFrame([], columns=['PATNO'])

    # iterate through demographic info to wrangle
    for key, curr_key in gen_info.items():
        for n, (fname, items) in enumerate(curr_key['files'].items()):
            data = pd.read_csv(os.path.join(path, fname), dtype=dtype)
            curr_score = data[items]
            for attr in [f for f in curr_key.keys() if f not in ['files']]:
                if hasattr(curr_score, attr):
                    fnc = getattr(curr_score, attr)
                    curr_score = fnc(curr_key[attr].get('input', None),
                                     **curr_key[attr].get('kwargs', {}))
            curr_score = pd.Series(curr_score, name=key)
            temp_scores = data[['PATNO']].join(curr_score)
        tidy = pd.merge(tidy, temp_scores, on='PATNO', how='outer')

    # rename columns and remove duplicates (how are there duplicates???)
    tidy = (tidy.rename(columns=rename_cols)
                .drop_duplicates(subset=['participant']))

    return tidy.sort_values('participant').reset_index(drop=True)


def available_genotypes(path: str = None) -> List[str]:
    """
    Lists measures available in :py:func:`pypmi.load_genotypes`
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    Returns
    -------
    measures : list
        Available genotype measures
    See Also
    --------
    pypmi.load_genotypes
    """

    return list(GENOTYPES_INFO.keys())

def load_prodromal(path: str = None,
                      measures: List[str] = None) -> pd.DataFrame:
    """
    Loads genotypes data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available demographics measures can be viewed
        with :py:func:`pypmi.available_demographics`. Default: None
    Returns
    -------
    demographics : :obj:`pandas.DataFrame`
        Tidy data frame containing demographic information for PPMI subjects
    See Also
    --------
    pypmi.available_demographics
    """

    rename_cols = dict(PATNO='participant', EVENT_ID='visit')
    dtype = dict(PATNO=int)

    # determine measures
    if measures is not None:
        if isinstance(measures, str) and measures == 'all':
            gen_info = PRODROMAL_INFO
        else:
            gen_info = {d: v for d, v in PRODROMAL_INFO.items()
                        if d in measures}
    else:
        gen_info = PRODROMAL_INFO

    # check for files and get data directory path
    fnames = []
    for info in gen_info.values():
        fnames.extend(list(info.get('files', {}).keys()))
    path = _get_data_dir(path=path, fnames=set(fnames))

    # empty data frame to hold information
    tidy = pd.DataFrame([], columns=['PATNO'])

    # iterate through demographic info to wrangle
    for key, curr_key in gen_info.items():
        for n, (fname, items) in enumerate(curr_key['files'].items()):
            data = pd.read_csv(os.path.join(path, fname), dtype=dtype)
            curr_score = data[items]
            for attr in [f for f in curr_key.keys() if f not in ['files']]:
                if hasattr(curr_score, attr):
                    fnc = getattr(curr_score, attr)
                    curr_score = fnc(curr_key[attr].get('input', None),
                                     **curr_key[attr].get('kwargs', {}))
            curr_score = pd.Series(curr_score, name=key)
            temp_scores = data[['PATNO']].join(curr_score)
        tidy = pd.merge(tidy, temp_scores, on='PATNO', how='outer')

    # rename columns and remove duplicates
    tidy = (tidy.rename(columns=rename_cols).groupby('participant').last()).reset_index()
               # .drop_duplicates(subset=['participant']))
    more_dat = pd.read_csv(f'{path}/DaTscan/inv_spect_vi_sequestered_merge_20231026.csv',usecols=['PATNO','DATSCAN_VISINTRP']).rename(columns={'DATSCAN_VISINTRP':'dat_deficit_add','PATNO':'participant'})
    more_dat = more_dat.groupby('participant').last().reset_index()
    tidy = pd.merge(tidy,more_dat,on='participant',how='left')
    print(tidy['dat_deficit'].isna().sum())
    tidy['dat_deficit'] = tidy['dat_deficit'].fillna(tidy['dat_deficit_add'])
    print(tidy['dat_deficit'].isna().sum())

    return tidy.sort_values('participant').reset_index(drop=True)

def load_prodromalBerg(path: str = None,
                      measures: List[str] = None) -> pd.DataFrame:
    """
    Loads genotypes data into tidy dataframe
    Parameters
    ----------
    path : str, optional
        Filepath to directory containing PPMI data files. If not specified this
        function will, in order, look (1) for an environmental variable
        $PPMI_PATH and (2) in the current directory. Default: None
    measures : list, optional
        Which measures to keep in the final dataframe. If not specified all
        measures are retained; available demographics measures can be viewed
        with :py:func:`pypmi.available_demographics`. Default: None
    Returns
    -------
    demographics : :obj:`pandas.DataFrame`
        Tidy data frame containing demographic information for PPMI subjects
    See Also
    --------
    pypmi.available_demographics
    """

    rename_cols = dict(PATNO='participant')
    dtype = dict(PATNO=int)

    # determine measures
    if measures is not None:
        if isinstance(measures, str) and measures == 'all':
            gen_info = PRODROMAL_INFO
        else:
            gen_info = {d: v for d, v in PRODROMAL_BERG2015.items()
                        if d in measures}
    else:
        gen_info = PRODROMAL_BERG2015

    # check for files and get data directory path
    fnames = []
    for info in gen_info.values():
        fnames.extend(list(info.get('files', {}).keys()))
    path = _get_data_dir(path=path, fnames=set(fnames))

    # empty data frame to hold information
    tidy = pd.DataFrame([], columns=['PATNO'])

    # iterate through demographic info to wrangle
    for key, curr_key in gen_info.items():
        print(key)
        for n, (fname, items) in enumerate(curr_key['files'].items()):
            data = pd.read_csv(os.path.join(path, fname), dtype=dtype)
            data = data.rename(columns={'patno':"PATNO"})
            data['PATNO'] = data['PATNO'].astype(int)
            curr_score = data[items]
            for attr in [f for f in curr_key.keys() if f not in ['files']]:
                if hasattr(curr_score, attr):
                    fnc = getattr(curr_score, attr)
                    curr_score = fnc(curr_key[attr].get('input', None),
                                     **curr_key[attr].get('kwargs', {}))
            curr_score = pd.Series(curr_score, name=key)
            temp_scores = data[['PATNO']].join(curr_score)
        tidy = pd.merge(tidy, temp_scores, on='PATNO', how='outer')

    # rename columns and remove duplicates
    # keep last entry per participant
    tidy = (tidy.rename(columns=rename_cols).groupby('participant').last()).reset_index()
                #.drop_duplicates(subset=['participant']))
    
    # add datscan visual inspect new results
    more_dat = pd.read_csv(f'{path}/DaTscan/inv_spect_vi_sequestered_merge_20231026.csv',usecols=['PATNO','DATSCAN_VISINTRP']).rename(columns={'DATSCAN_VISINTRP':'dat_deficit_add','PATNO':'participant'})
    more_dat = more_dat.groupby('participant').last().reset_index()
    tidy = pd.merge(tidy,more_dat,on='participant',how='left')
    tidy['dat_deficit'] = tidy['dat_deficit'].fillna(tidy['dat_deficit_add'])

    return tidy.sort_values('participant').reset_index(drop=True)


def load_genetics(fname: str,
                  gene_list: str = None) -> (pd.DataFrame, pd.DataFrame):
    """
    Loads PPMI genotyping data stored at `fname`
    Parameters
    ----------
    fname : str
        Filepath to genotyping PLINK files
    gene_list : str, optional
        Path to pandas-compatible csv with at least 'snp', 'target', and
        'odds_ratio' columns denoting rs#, target (effect) allele, and odds
        ratio of target allele in population.
    Returns
    -------
    data : (N, G) :obj:`pandas.DataFrame`
        Wide-format genetics data where `N` is participants and `G` is SNPs
    info : (G, 5) :obj:`pandas.DataFrame`
        Information on SNPs in `data`, including 'odds_ratio' for genetic
        risk score calculation
    """

    try:
        from pandas_plink import read_plink
    except ImportError:
        raise ImportError('Loading genotyping data requires installing the '
                          '`pandas_plink` module. Please install that and try '
                          'again.')

    # make helper function for extracting SNP rs# from PLINK files
    def extract(x):
        try:
            return re.findall('[-_]*(rs[0-9]+)[-_]*', x)[0]
        except IndexError:
            return None

    # load PLINK data
    bim, fam, gen = read_plink(fname, verbose=False)
    participant_id = pd.Series(fam.fid.get_values(), name='participant')
    cols = ['snp', 'a0', 'a1']

    if gene_list is not None:
        # load gene list
        gene_info = pd.read_csv(gene_list).drop_duplicates(subset=['snp'])

        # check where SNPs match desired gene list & subset data
        inds = bim.snp.apply(extract).isin(gene_info.snp.dropna()).get_values()
        bim, gen = bim[inds], gen[inds]

        # clean up ugly bim.snp names with just rs# of SNPs
        bim.loc[:, 'snp'] = bim.snp.map({f: extract(f) for f in bim.snp})

        # get allele info for making sense of the data
        cols += ['target', 'odds_ratio', 'study']
        info = pd.merge(bim, gene_info, on='snp')[cols]

        # if a0/a1 alleles don't match target, confusion ensues
        # drop the non-matched ones and then grab SNPs that need to be reversed
        info = info[~((info.a0 != info.target) & (info.a1 != info.target))]
        flip = info[info.a1 != info.target].snp
        info = info[['snp', 'odds_ratio', 'study']]
    else:
        # placeholders so below code doesn't fail
        info = bim[cols]
        flip = pd.Series([], name='snp')

    # make wide-format participant x SNP dataframe
    data = pd.DataFrame(gen.compute().T, index=participant_id, columns=bim.snp)
    # if multiple columns represent same snp, combine them
    # THEY SHOULD ALL BE THE SAME -- if they aren't, that's bad...
    data = (data.dropna(axis=1, how='all')
                .groupby(level=0, axis=1)
                .mean()
                .dropna(axis=0, how='all')
                .sort_index())
    # flip reverse-coded SNPs
    data[flip] = data[flip].applymap(lambda x: {0: 2, 1: 1, 2: 0}.get(x))

    # retain only relevant SNPs in allele
    info = info[info.snp.isin(data.columns)]
    info = info.drop_duplicates(subset=['snp']).reset_index(drop=True)

    # return sorted data and info
    return data[info.snp], info