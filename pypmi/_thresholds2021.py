"""
Data structures specifying thresholds for behavioral and demographic data; detect outliers
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype as cdtype
import datetime


BEHAVIORAL_INFO = {
    'benton': {
        'min': 0,
        'max': 15,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'epworth': {
        'min': 0,
        'max': 24,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'gds': {
        'min': 0,
        'max': 15,
        'recode': False,
        'scale_level': 'ordinal' 
    },
    'hvlt_recall': {
        'min': 0,
        'max': 36,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'hvlt_recognition': {
        'min': -12,
        'max': 12,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'hvlt_retention': {
        'min': 0,
        'max': 12,
        'recode': True,
        'scale_level': 'normal'
    },
    'lns': {
        'min': 0,
        'max': 30,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'moca': {
        'min': 0,
        'max': 30,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'pigd': {
        'min': 0,
        'max': 20,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'pigd_mean': {
        'min': 0,
        'max': 4,
        'recode': False,
        'scale_level': 'normal'
    },
    'quip': {
        'min': 0,
        'max': 15,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'rbd': {
        'min': 0,
        'max': 13,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'scopa_aut': {
        'min': 0,
        'max': 69,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'se_adl': {
        'min': 0,
        'max': 100,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'semantic_fluency': {
        'min': 0,
        'max': 200,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'stai_state': {
        'min': 20,
        'max': 80,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'stai_trait': {
        'min': 20,
        'max': 80,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'symbol_digit': {
        'min': 0,
        'max': 110,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'systolic_bp_drop': {
        'min': -100,
        'max': 100,
        'recode': False,
        'scale_level': 'normal'
    },
    'tremor': {
        'min': 0,
        'max': 44,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'tremor_mean': {
        'min': 0,
        'max': 4,
        'recode': False,
        'scale_level': 'normal'
    },
    'updrs_i': {
        'min': 0,
        'max': 52,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'updrs_ii': {
        'min': 0,
        'max': 52,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'updrs_sleep': {
        'min': 0,
        'max': 12,
        'recode': False,
        'scale_level': 'ordinal'
    },
        'updrs_autonomic': {
        'min': 0,
        'max': 12,
        'recode': False,
        'scale_level': 'ordinal'
    },
        'updrs_neuropsychiatric': {
        'min': 0,
        'max': 19,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'updrs_iii_OFF': {
        'min': 0,
        'max': 136,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'updrs_iii_ON': {
        'min': 0,
        'max': 136,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'updrs_iii_NoMED': {
        'min': 0,
        'max': 136,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'updrs_iv': {
        'min': 0,
        'max': 24,
        'recode': False,
        'scale_level': 'ordinal'
    },
    'upsit': {
        'min': 0,
        'max': 40,
        'recode': True,
        'scale_level': 'ordinal'
    },
    'upsit_percent': {
        'min': 0,
        'max': 100,
        'recode': True,
        'scale_level': 'normal'
    },
    'date': {
        "scale_level": 'date',
        'min': pd.Timestamp(datetime.datetime(2010,1,1)),
        'max': pd.Timestamp(datetime.date.today())
    },
    'tmtb-a': {
        'min': -10,
        'max': 500,
        'recode': False,
        'scale_level': 'normal'
    },
    'tmtb/a': {
        'min': 0,
        'max': 5,
        'recode': False,
        'scale_level': 'normal'
    },
    'tmta': {
        'min': 0,
        'max': 500,
        'recode': False,
        'scale_level': 'normal'
    },
    'tmtb': {
        'min': 0,
        'max': 500,
        'recode': False,
        'scale_level': 'normal'
    },
    'state_NoMed': {
        'categories': [0,1],
        'scale_level': 'binomial'
    },
    'state_ON': {
        'categories': [0,1],
        'scale_level': 'binomial'
    },
    'state_OFF': {
        'categories': [0,1],
        'scale_level': 'binomial'
    },
    'state_A': {
        'categories': [0,1],
        'scale_level': 'binomial'
    },
}

DEMOGRAPHIC_INFO = {
    'diagnosis_enroll': {
        'scale_level': 'categorical',
        'categories': ['pd','swedd','imaging','hc','prod',np.nan]
    },
    'diagnosis': {
        'scale_level': 'categorical',
        'categories': ['pd','swedd','prod','hc','exclude',np.nan]
    },
    'date_birth': {
        'scale_level': 'date',
        'min': pd.Timestamp(datetime.datetime(1910,1,1)),
        'max': pd.Timestamp(datetime.date.today())
    },
    'date_diagnosis': {
        'scale_level': 'date',
        'min': pd.Timestamp(datetime.datetime(1910,1,1)),
        'max': pd.Timestamp(datetime.date.today())
    },
    'date_diagnosis_enroll': {
        'scale_level': 'date',
        'min': pd.Timestamp(datetime.datetime(1910,1,1)),
        'max': pd.Timestamp(datetime.date.today())
    },
    'date_enroll': {
        'scale_level': 'date',
        'min': pd.Timestamp(datetime.datetime(2010,1,1)),
        'max': pd.Timestamp(datetime.date.today())
    },
    'status': {
        'scale_level': 'categorical',
        'categories': ['complete', 'declined', 'enrolled', 'excluded', 'withdrew']
    },
    'family_history': {
        'scale_level': 'binomial',
        'categories': [True,False]
    },
    '1st_degree_relative': {
        'scale_level': 'ordinal',
        'min': 0,
        'max': 10
    },
    '2nd_degree_relative': {
        'scale_level': 'ordinal',
        'min': 0,
        'max': 10
    },
    'age': {
        'scale_level': 'ordinal',
        'min': 60,
        'max': 100
    },
    'gender': {
        'scale_level': 'binomial',
        'categories': ['f','m']
    },
    'race': {
        'scale_level': 'categorical',
        'categories': ['asian', 'black', 'hawopi', 'indals', 'multi', 'ns', 'white']
    },
    'site': {
        'scale_level': 'categorical',
        'categories': [  1,   2,   6,   7,  12,  18,  19,  23,  28,  32,  34,  40,  57,
        73,  86,  88,  89,  96, 120, 154, 164, 196, 289, 290, 291, 295,
       304, 306, 307, 308, 327, 334, 335]
    },
    'handedness': {
        'scale_level':'categorical',
        'categories': ['right','left','both']
    },
    'education': {
        'scale_level': 'normal',
        'min': 0,
        'max': 40
    },
    'date_onset': {
        'scale_level':'date',
        'min': pd.Timestamp(datetime.datetime(1930,1,1)),
        'max': pd.Timestamp(datetime.date.today())
    },
    'date_consensus': {
        'scale_level':'date',
        'min': pd.Timestamp(datetime.datetime(2021,6,1)),
        'max': pd.Timestamp(datetime.date.today())
    }
}

GENOTYPES_INFO = {
    'LRRK2': {
        'scale_level': 'categorical',
        'categories': [0,1,np.nan]
    },
    'GBA': {
        'scale_level': 'categorical',
        'categories': [0,1,np.nan]
    },
    'SNCA': {
        'scale_level': 'categorical',
        'categories': [0,1,np.nan]
    },
}