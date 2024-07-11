"""
Data structures specifying methods for creating or calculating behavioral and
demographic measures
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype as cdtype


BEHAVIORAL_INFO = {
    'benton': {
        'files': {
            'Benton_Judgement_of_Line_Orientation.csv': [
                [f'BJLOT{num}' for num in range(1, 31)]
            ]
        }
    },
    'education': {
        'files': {
            'Socio-Economics.csv': [
                ['EDUCYRS']
            ]
        },
        'applymap': [
            lambda x: 1.0 if x <= 12 else 0
        ]
    },
    'epworth': {
        'files': {
            'Epworth_Sleepiness_Scale.csv': [
                #['ESS1', 'ESS2', 'ESS3', 'ESS4', 'ESS5', 'ESS6', 'ESS7',
                # 'ESS8']
                [f'ESS{num}' for num in range(1, 9)]
            ]
        }
    },
    'gds': {
        'files': {
            'Geriatric_Depression_Scale__Short_Version_.csv': [
                ['GDSSATIS', 'GDSGSPIR', 'GDSHAPPY', 'GDSALIVE', 'GDSENRGY'],
                ['GDSDROPD', 'GDSEMPTY', 'GDSBORED', 'GDSAFRAD', 'GDSHLPLS',
                 'GDSHOME', 'GDSMEMRY', 'GDSWRTLS', 'GDSHOPLS', 'GDSBETER']
            ],
        },
        'applymap': [
            lambda x: 1.0 if x == 0.0 else 0.0,
            lambda x: x
        ]
    },
    'hvlt_recall': {
        'files': {
            'Hopkins_Verbal_Learning_Test_-_Revised.csv': [
                ['HVLTRT1', 'HVLTRT2', 'HVLTRT3']
            ]
        }
    },
    'hvlt_recognition': {
        'files': {
            'Hopkins_Verbal_Learning_Test_-_Revised.csv': [
                ['HVLTREC'],
                ['HVLTFPRL'],
                ['HVLTFPUN']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: -x,
            lambda x: -x
        ]
    },
    'hvlt_retention': {
        'files': {
            'Hopkins_Verbal_Learning_Test_-_Revised.csv': [
                ['HVLTRDLY'],
                ['HVLTRT2', 'HVLTRT3']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: 1. / x if x != 0 else np.inf
        ],
        'operation': [
            np.sum, np.min
        ],
        'joinfunc': np.prod
    },
    'lns': {
        'files': {
            'Letter_-_Number_Sequencing.csv': [
                ['LNS1A', 'LNS1B', 'LNS1C', 'LNS2A', 'LNS2B', 'LNS2C', 'LNS3A',
                 'LNS3B', 'LNS3C', 'LNS4A', 'LNS4B', 'LNS4C', 'LNS5A', 'LNS5B',
                 'LNS5C', 'LNS6A', 'LNS6B', 'LNS6C', 'LNS7A', 'LNS7B', 'LNS7C']
            ]
        }
    },
    'moca': {
        'files': {
            'Montreal_Cognitive_Assessment__MoCA_.csv': [
                ['MCAALTTM', 'MCACUBE', 'MCACLCKC', 'MCACLCKN', 'MCACLCKH',
                 'MCALION', 'MCARHINO', 'MCACAMEL', 'MCAFDS', 'MCABDS',
                 'MCAVIGIL', 'MCASER7', 'MCASNTNC', 'MCAVF', 'MCAABSTR',
                 'MCAREC1', 'MCAREC2', 'MCAREC3', 'MCAREC4', 'MCAREC5',
                 'MCADATE', 'MCAMONTH', 'MCAYR', 'MCADAY', 'MCAPLACE',
                 'MCACITY']
            ]
        }
    },
    'pigd_OFF': {
       'files': {
           'MDS_UPDRS_Part_III.csv': [
               ['NP3GAIT', 'NP3FRZGT', 'NP3PSTBL'],['PAG_NAME']
           ]
       },
       'extra': [
           'PATNO', 'EVENT_ID', 'INFODT'
       ],
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3OF' else -999
        ],
        'operation': [
            np.sum,np.sum
        ],
        'joinfunc': np.prod
    },
    'pigd_ON': {
       'files': {
           'MDS_UPDRS_Part_III.csv': [
               ['NP3GAIT', 'NP3FRZGT', 'NP3PSTBL'],['PAG_NAME']
           ]
       },
       'extra': [
           'PATNO', 'EVENT_ID', 'INFODT'
       ],
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3ON' else -999
        ],
        'operation': [
            np.sum,np.sum
        ],
        'joinfunc': np.prod
    },
    'pigd_NoMED': {
       'files': {
           'MDS_UPDRS_Part_III.csv': [
               ['NP3GAIT', 'NP3FRZGT', 'NP3PSTBL'],['PAG_NAME']
           ]
       },
       'extra': [
           'PATNO', 'EVENT_ID', 'INFODT'
       ],
     'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDRS3' else -999
        ],
        'operation': [
            np.sum,np.sum
        ],
        'joinfunc': np.prod
    },
    'pigd_II': {
       'files': {
           'MDS_UPDRS_Part_II__Patient_Questionnaire.csv': [
               ['NP2WALK', 'NP2FREZ']
           ]
       }
    },
    'quip': {
        'files': {
            'QUIP-Current-Short.csv': [
                ['CNTRLGMB', 'TMGAMBLE'],
                ['CNTRLSEX', 'TMSEX'],
                ['CNTRLBUY', 'TMBUY'],
                ['CNTRLEAT', 'TMEAT'],
                ['TMTORACT', 'TMTMTACT', 'TMTRWD']
            ]
        },
        'operation': [
            np.any, np.any, np.any, np.any, np.sum
        ]
    },
    'rbd': {
        'files': {
            'REM_Sleep_Behavior_Disorder_Questionnaire.csv': [
                ['DRMVIVID', 'DRMAGRAC', 'DRMNOCTB', 'SLPLMBMV', 'SLPINJUR',
                 'DRMVERBL', 'DRMFIGHT', 'DRMUMV', 'DRMOBJFL', 'MVAWAKEN',
                 'DRMREMEM', 'SLPDSTRB'],
                ['STROKE', 'HETRA', 'PARKISM', 'RLS', 'NARCLPSY', 'DEPRS',
                 'EPILEPSY', 'BRNINFM', 'CNSOTH']
            ]
        },
        'operation': [
            np.sum, np.any
        ]
    },
    'scopa_aut': {
        'files': {
            'SCOPA-AUT.csv': [
                [f'SCAU{num}' for num in range(1, 22)],
                ['SCAU22', 'SCAU23', 'SCAU24', 'SCAU25']
            ]
        },
        'applymap': [
            lambda x: 3.0 if x == 9.0 else x,
            lambda x: 0.0 if x == 9.0 else x
        ]
    },
    'se_adl': {
        'files': {
            'Modified_Schwab___England_Activities_of_Daily_Living.csv': [
                ['MSEADLG']
            ]
        }
    },
    'semantic_fluency': {
        'files': {
            'Modified_Semantic_Fluency.csv': [
                ['VLTANIM', 'VLTVEG', 'VLTFRUIT']
            ]
        }
    },
    'stai_state': {
        'files': {
            'State-Trait_Anxiety_Inventory.csv': [
                ['STAIAD3', 'STAIAD4', 'STAIAD6', 'STAIAD7', 'STAIAD9',
                 'STAIAD12', 'STAIAD13', 'STAIAD14', 'STAIAD17', 'STAIAD18'],
                ['STAIAD1', 'STAIAD2', 'STAIAD5', 'STAIAD8', 'STAIAD10',
                 'STAIAD11', 'STAIAD15', 'STAIAD16', 'STAIAD19', 'STAIAD20']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: 5 - x
        ]
    },
    'stai_trait': {
        'files': {
            'State-Trait_Anxiety_Inventory.csv': [
                ['STAIAD22', 'STAIAD24', 'STAIAD25', 'STAIAD28', 'STAIAD29',
                 'STAIAD31', 'STAIAD32', 'STAIAD35', 'STAIAD37', 'STAIAD38',
                 'STAIAD40'],
                ['STAIAD21', 'STAIAD23', 'STAIAD26', 'STAIAD27', 'STAIAD30',
                 'STAIAD33', 'STAIAD34', 'STAIAD36', 'STAIAD39']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: 5 - x
        ]
    },
    'symbol_digit': {
        'files': {
            'Symbol_Digit_Modalities_Test.csv': [
                ['SDMTOTAL']
            ]
        }
    },
    'systolic_bp_drop': {
        'files': {
            'Vital_Signs.csv': [
                ['SYSSUP'],
                ['SYSSTND']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: -x
        ]
    },
    'tremor_II': {
        'files': {
           'MDS_UPDRS_Part_II__Patient_Questionnaire.csv': [
               ['NP2TRMR']
           ],
        }, 
    },
    'tremor_A': {
       'files': {
           'MDS_UPDRS_Part_III.csv': [
               ['NP3PTRMR', 'NP3PTRML', 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU',
                'NP3RTALU', 'NP3RTARL', 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],['PAG_NAME']
            ]
        },
        'extra':['PAG_NAME'],
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDRS3A' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'tremor_OFF': {
       'files': {
           'MDS_UPDRS_Part_III.csv': [
               ['NP3PTRMR', 'NP3PTRML', 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU',
                'NP3RTALU', 'NP3RTARL', 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],['PAG_NAME']
           ]
       },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3OF' else -999
        ],
        'operation': [
            np.sum,np.sum
        ],
        'joinfunc': np.prod
    },
    'tremor_ON': {
       'files': {
           'MDS_UPDRS_Part_III.csv': [
               ['NP3PTRMR', 'NP3PTRML', 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU',
                'NP3RTALU', 'NP3RTARL', 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],['PAG_NAME']
           ]
       },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3ON' else -999
        ],
        'operation': [
            np.sum,np.sum
        ],
        'joinfunc': np.prod
    },
    'state_NoMED': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['PAG_NAME'],
                ['PDSTATE']
            ],
        },
        'applymap': [
            lambda x: 1 if x=='NUPDRS3' else np.nan,
            lambda x: 1 if x=='OFF' else 2 if x=='ON' else np.nan
        ],
        'joinfunc': np.prod
    },
    'state_A': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['PAG_NAME'],
                ['PDSTATE']
            ],
        },
        'applymap': [
            lambda x: 1 if x=='NUPDRS3A' else np.nan,
            lambda x: 1 if x=='OFF' else 2 if x=='ON' else np.nan
        ],
        'joinfunc': np.prod
    },
    'state_OFF': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['PAG_NAME'],
                ['PDSTATE']
            ],
        },
        'applymap': [
            lambda x: 1 if x=='NUPDR3OF' else -999,
            lambda x: 1 if x=='OFF' else 2 if x=='ON' else np.nan
        ],
        'joinfunc': np.prod
    },
    'state_ON': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['PAG_NAME'],
                ['PDSTATE']
            ],
        },
        'applymap': [
            lambda x: 1 if x=='NUPDR3ON' else np.nan,
            lambda x: 1 if x=='OFF' else 2 if x=='ON' else np.nan
        ],
        'joinfunc': np.prod
    },
    'updrs_i': {
        'files': {
            'MDS-UPDRS_Part_I.csv': [
                ['NP1COG', 'NP1HALL', 'NP1DPRS', 'NP1ANXS', 'NP1APAT',
                 'NP1DDS']
            ],
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv': [
                ['NP1SLPN', 'NP1SLPD', 'NP1PAIN', 'NP1URIN', 'NP1CNST',
                 'NP1LTHD', 'NP1FATG']
            ]
        },
        'extra': [
            'PATNO', 'EVENT_ID', 'INFODT'
        ],
    },
    'updrs_ii': {
        'files': {
            'MDS_UPDRS_Part_II__Patient_Questionnaire.csv': [
                ['NP2SPCH', 'NP2SALV', 'NP2SWAL', 'NP2EAT', 'NP2DRES',
                 'NP2HYGN', 'NP2HWRT', 'NP2HOBB', 'NP2TURN', 'NP2TRMR',
                 'NP2RISE', 'NP2WALK', 'NP2FREZ']
            ]
        }
    },
    'updrs_sleep': {
        'files': {
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv': [
                ['NP1SLPN', 'NP1SLPD', 'NP1FATG']
            ]
        }
    },
    'updrs_neuropsychiatric': {
        'files': {
            'MDS-UPDRS_Part_I.csv': [
                ['NP1COG', 'NP1HALL', 'NP1DPRS', 'NP1ANXS', 'NP1APAT']
            ]
        }
    },
    'updrs_autonomic': {
        'files': {
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv': [
                ['NP1URIN', 'NP1CNST','NP1LTHD']
            ]
        }
    },
    'updrs_iii_NoMED': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU',
                 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR',
                 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL',
                 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT',
                 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3PTRMR', 'NP3PTRML',
                 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL',
                 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],['PAG_NAME']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDRS3' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'updrs_iii_OFF': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU',
                 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR',
                 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL',
                 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT',
                 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3PTRMR', 'NP3PTRML',
                 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL',
                 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],
                ['PAG_NAME'],
            ],
        },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3OF' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'updrs_iii_ON': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU',
                 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR',
                 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL',
                 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT',
                 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3PTRMR', 'NP3PTRML',
                 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL',
                 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],
                ['PAG_NAME']
            ],
        },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3ON' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'updrs_iii_A': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU',
                 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR',
                 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL',
                 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT',
                 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3PTRMR', 'NP3PTRML',
                 'NP3KTRMR', 'NP3KTRML', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL',
                 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],
                ['PAG_NAME']
            ],
        },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDRS3A' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'updrs_iv': {
        'files': {
            'MDS-UPDRS_Part_IV__Motor_Complications.csv': [
                ['NP4WDYSK', 'NP4DYSKI', 'NP4OFF', 'NP4FLCTI', 'NP4FLCTX',
                 'NP4DYSTN']
            ]
        }
    },
    'updrs_iii_OFF_notremor': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU',
                 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR',
                 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL',
                 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT',
                 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 
                  'NP3RTARU', 'NP3RTALU', 'NP3RTARL',
                 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],
                ['PAG_NAME'],
            ],
        },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDR3OF' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'updrs_iii_NoMED_notremor': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['NP3SPCH', 'NP3FACXP', 'NP3RIGN', 'NP3RIGRU', 'NP3RIGLU',
                 'NP3RIGRL', 'NP3RIGLL', 'NP3FTAPR', 'NP3FTAPL', 'NP3HMOVR',
                 'NP3HMOVL', 'NP3PRSPR', 'NP3PRSPL', 'NP3TTAPR', 'NP3TTAPL',
                 'NP3LGAGR', 'NP3LGAGL', 'NP3RISNG', 'NP3GAIT', 'NP3FRZGT',
                 'NP3PSTBL', 'NP3POSTR', 'NP3BRADY', 'NP3RTARU', 'NP3RTALU', 'NP3RTARL',
                 'NP3RTALL', 'NP3RTALJ', 'NP3RTCON'],['PAG_NAME']
            ]
        },
        'applymap': [
            lambda x: x,
            lambda x: 1 if x=='NUPDRS3' else -999
        ],
        'operation': [
            np.sum, np.sum
        ],
        'joinfunc': np.prod
    },
    'upsit': {
        'files': {
            'University_of_Pennsylvania_Smell_Identification_Test__UPSIT_.csv': [
                ['TOTAL_CORRECT']
            ]
        }
    },
    'upsit_percent': {
        'files': {
            'University_of_Pennsylvania_Smell_Identification_Test__UPSIT_.csv': [
                ['UPSIT_PRCNTGE']
            ]
        }
    },
    'tmtb': {
        'files': {
            'Trail_Making_A_and_B.csv': [['TMTBSEC']],
        },
    },
    'tmta': {
        'files': {
            'Trail_Making_A_and_B.csv': [['TMTASEC']],
        },
    },
    'tmtb/a': {
        'files': {
            'Trail_Making_A_and_B.csv': [['TMTBSEC'],['TMTASEC']],
        },
        'applymap': [
            lambda x: x,
            lambda x: 1. / x if x != 0 else np.inf
        ],
        'operation': [
            np.sum, np.min
        ],
        'joinfunc': np.prod
    },
    'tmtb-a': {
        'files': {
            'Trail_Making_A_and_B.csv': [['TMTBSEC','TMTASEC']],
        },
        'diff': {
            'input': 1,
            'kwargs': {
                'axis': 1
            }
        },
    },
    'updrs_i_constipation': {
        'files': {
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv': [['NP1CNST']]
        },
       'applymap': [
            lambda x: 0.0 if x <1 else x
        ]
    },
    'updrs_i_urinary': {
        'files': {
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv': [[ 'NP1URIN' ]]
        },
       'applymap': [
            lambda x: 0.0 if x <1 else x
        ]
    },
    'updrs_i_OH': {
        'files': {
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv':[ [ 'NP1LTHD' ]]
        },
       'applymap': [
            lambda x: 0.0 if x <1 else x
        ]
    },
    'updrs_i_daytimesleepiness': {
        'files': {
            'MDS-UPDRS_Part_I_Patient_Questionnaire.csv': [[ 'NP1FATG' ]]
        },
       'applymap': [
            lambda x: 0.0 if x <1 else x
        ]
    },
   'updrs_i_depression': {
        'files': {
            'MDS-UPDRS_Part_I.csv':[[ 'NP1DPRS' ]]
        },   
       'applymap': [
            lambda x: 0.0 if x <1 else x
        ]
    },
    'scopa_aut_erectileDysfunction': {
        'files': {
            'SCOPA-AUT.csv':
                [['SCAU22']]
        },
        'applymap': [
            lambda x: 0.0 if x == 9.0 else x
        ]
    },
}

MEDICATION_INFO = {
    'medicated_now': {
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['PDSTATE']
            ],
        },
    },
    'medicated':{
        'files': {
            'MDS_UPDRS_Part_III.csv': [
                ['PDTRTMNT']
            ],
        }
    }
}

DEMOGRAPHIC_INFO = {
    'diagnosis_enroll': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'COHORT_DEFINITION'
        },
        'replace': {
            'input': {
                "Parkinson's Disease": 'pd',
                'Healthy Control': 'hc',
                'SWEDD': 'swedd',
                'Prodromal': 'prod',
                'Early Imaging (original study participants only)': 'imaging',
            }
        },
        'astype': {
            'input': 'category'
        }
    },
    'diagnosis': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONCOHORT_DEFINITION'
        },
        'replace': {
            'input': {
                "Parkinson's Disease": 'pd',
                'Healthy Control': 'hc',
                'SWEDD': 'swedd',
                'non-PD, non-Prodromal, non-HC (participants to be excluded)': 'exclude',
                'Prodromal': 'prod',
            }
        },
        'astype': {
            'input': 'category'
        }
    },
    'date_birth': {
        'files': {
            'Demographics.csv': 'BIRTHDT'
        },
        'apply': {
            'input': pd.to_datetime
        }
    },
    'date_diagnosis': {
        'files': {
            'PD_Diagnosis_History.csv': 'PDDXDT'
        },
        'apply': {
            'input': pd.to_datetime
        }
    },
    'date_consensus': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONDATE'
        },
        'apply': {
            'input': pd.to_datetime
        }
    },
    'date_enroll': {
        'files': {
            'Demographics.csv': 'INFODT'
        },
        'apply': {
            'input': pd.to_datetime
        }
    },
    'status': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'ENROLL_STATUS'
        },
        'apply': {
            'input': lambda x: x.lower()
        }
    },
    'family_history': {
        'files': {
            'Family_History.csv': [
                'BIOMOMPD',
                'BIODADPD',
                'FULSIBPD',
                'HAFSIBPD',
                'MAGPARPD',
                'PAGPARPD',
                'MATAUPD',
                'PATAUPD',
                'KIDSPD'
            ]
        },
        'apply': {
            'input': np.nansum,
            'kwargs': {
                'axis': 1
            }
        },
        'astype': {
            'input': 'bool'
        }
    },
    '1st_degree_relative': {
        'files': {
            'Family_History.csv': [
                'BIOMOMPD',
                'BIODADPD',
                'FULSIBPD',
                'KIDSPD',
            ]
        },
        'apply': {
            'input': np.nansum,
            'kwargs': {
                'axis': 1
            }
        }
    },
    '2nd_degree_relative': {
        'files': {
            'Family_History.csv': [
                'HAFSIBPD',
                'MAGPARPD',
                'PAGPARPD',
                'MATAUPD',
                'PATAUPD',
            ]
        },
        'apply': {
            'input': np.nansum,
            'kwargs': {
                'axis': 1
            }
        }
    },
    'age': {
        'files': {
            'Demographics.csv': [
                'BIRTHDT',
                'INFODT'
            ]
        },
        'apply': {
            'input': pd.to_datetime
        },
        'diff': {
            'input': 1,
            'kwargs': {
                'axis': 1
            }
        },
        'get': {
            'input': 'INFODT'
        },
        'divide': {
            'input': np.timedelta64(1, 'Y')
        }
    },
    'gender': {
        'files': {
            'Demographics.csv': 'SEX'
        },
        'replace': {
            'input': {
                0: 'f',
                1: 'm',
                np.nan: 'ns'
            }
        },
        'astype': {
            'input': 'category'
        }
    },
    'race': {
        'files': {
            'Demographics.csv': [
                'RAINDALS',
                'RAASIAN',
                'RABLACK',
                'RAHAWOPI',
                'RAWHITE',
                'RANOS'
            ]
        },
        'apply': {
            'input': np.where,
            'kwargs': {'axis': 1}
        },
        'transform': {
            'input': lambda x: x[0][0] if len(x[0]) == 1 else 'multi'
        },
        'replace': {
            'input': {
                0: 'indals',
                1: 'asian',
                2: 'black',
                3: 'hawopi',
                4: 'white',
                5: 'ns'
            }
        },
        'astype': {
            'input': 'category'
        }
    },
    'handedness': {
        'files': {
            'Demographics.csv': 'HANDED'
        },
        'replace': {
            'input': {
                1: 'right',
                2: 'left',
                3: 'both'
            }
        },
        'astype': {
            'input': 'category'
        }
    },
    'education': {
        'files': {
            'Socio-Economics.csv': 'EDUCYRS'
        }
    },
    'date_onset':{
        'files':{ 'PD_Diagnosis_History.csv':'SXDT'
                },
        'apply': {
            'input': pd.to_datetime
        },
    }
}

PRODROMAL_INFO = {
    'rbd':{
        'files': {'Participant_Status_19Oct2023.csv' : 'CONRBD'
        },
    },
    'dat_deficit':{
        'files': {'DaTScan_Visual_Interpretation_Results.csv' : 'DATSCAN_VISINTRP'
        },
    },
    'hyposmia':{
        'files': {'Participant_Status_19Oct2023.csv' : 'CONHPSM'
        },
    },
    'phenoconverted':{
        'files': {'Participant_Status_19Oct2023.csv' : 'PHENOCNV'
        },
    },
    'phenoconverted_visit':{
        'files': {'Participant_Status_19Oct2023.csv' : 'DIAG1VIS'
        },
    },
    'phenoconverted_diagnosis':{
        'files': {'Participant_Status_19Oct2023.csv' : 'DIAG1'
        },
    }
}

PRODROMAL_BERG2015 = {
    'rbd':{
        'files': {'Participant_Status_19Oct2023.csv' : 'CONRBD'
        },
    },
    'dat_deficit':{
        'files': {'DaTScan_Visual_Interpretation_Results.csv' : 'DATSCAN_VISINTRP'
        },
    },
    'hyposmia':{
        'files': {'Participant_Status_19Oct2023.csv' : 'CONHPSM'
        },
    },
    'phenoconverted':{
        'files': {'Participant_Status_19Oct2023.csv' : 'PHENOCNV'
        },
    },
    'phenoconverted_visit':{
        'files': {'Participant_Status_19Oct2023.csv' : 'DIAG1VIS'
        },
    },
    'phenoconverted_diagnosis':{
        'files': {'Participant_Status_19Oct2023.csv' : 'DIAG1'
        },
    },
    '1st_degree_family_history': {
        'files': {
            'Family_History.csv': [
                'BIOMOMPD',
                'BIODADPD',
                'FULSIBPD',
            ]
        },
        'apply': {
            'input': np.nansum,
            'kwargs': {
                'axis': 1
            }
        },
        'astype': {
            'input': 'bool'
        }
    },
    'pesticide_occupational_exposure':{
        'files': {'FOUND_RFQ_Pesticides_at_Work.csv' : 'pwlabelintro1'
        },
    },
    'pesticide_personal_exposure':{
        'files': {'FOUND_RFQ_Pesticides_Non-Work.csv' : 'phintro'
        },
    },
    # 'nonuse_caffeine':{
    #     'files': {'FOUND_RFQ_Caffeine.csv' : [['cfqa5week','cfqa5day'],
    #                                           ['cfqb5week','cfqb5day']] # cups per week coffee, tea         
    #     },
    #     'applymap': [
    #         lambda x: x[0] < 3 or x[1] < 0.43,
    #         lambda x: x[0] < 6 or x[1] < 0.86
    #     ],
    #     'joinfunc': { np.all
    #     }
    # },
    'coffee_week':{
        'files': {'FOUND_RFQ_Caffeine.csv' : 'cfqa5week' # cups per week coffee, tea     
                 }
    },
    'coffee_day':{
        'files': {'FOUND_RFQ_Caffeine.csv' : 'cfqa5day' # cups per week coffee, tea         
                 }
    },
    'tea_week':{
        'files': {'FOUND_RFQ_Caffeine.csv' : 'cfqb5week' # cups per week coffee, tea   
                 }
    },
    'tea_day':{
        'files': {'FOUND_RFQ_Caffeine.csv' : 'cfqb5day' # cups per week coffee, tea         
                 }
    },
    'ever_smoke':{
        'files': {'FOUND_RFQ_Smoking_History.csv' : 'smq2' # lifetime ever smoked reqularily (more than 1 each day for 6 months)
        },
    },
    'current_smoke':{
        'files': {'FOUND_RFQ_Smoking_History.csv' : 'smq4' # currently regular
        },
    },
    'urate':{
        'files': {'Participant_Status_19Oct2023.csv' : 'DIAG1'
        },
    },
    'cognitive_deficit':{
        'files': {'Participant_Status_19Oct2023.csv' : 'DIAG1'
        },
    },
    'physical_inactivity':{
        'files': {'FOUND_RFQ_Physical_Activity.csv' : 'pa1a'
        },
    },
    
}


GENOTYPES_INFO = {
    'LRRK2': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONLRRK2'
        }
    },
    'GBA': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONGBA'
        }
    },
    'SNCA': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONSNCA'
        }
    },
        'PRKN': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONPRKN'
        }
    },
        'PINK1': {
        'files': {
            'Participant_Status_19Oct2023.csv': 'CONPINK1'
        }
    },
}


VISITS = cdtype([
    'SC',
    'ST',
    'RS1',
    'BL',
    'V01',
    'V02',
    'T06',
    'V03',
    'V04',
    'R04',
    'T12',
    'T15',
    'T17',
    'V05',
    'R05',
    'T18',
    'T19',
    'T21',
    'V06',
    'R06',
    'T24',
    'T27',
    'V07',
    'R07',
    'T30',
    'T33',
    'V08',
    'R08',
    'T36',
    'T39',
    'V09',
    'R09',
    'T42',
    'T45',
    'V10',
    'R10',
    'T48',
    'T51',
    'V11',
    'R11',
    'T54',
    'T57',
    'V12',
    'R12',
    'T60',
    'V13',
    'R13',
    'T72',
    'P78',
    'V14',
    'R14',
    'T84',
    'P90',
    'V15',
    'R15',
    'T96',
    'P102',
    'V16',
    'R16',
    'T108',
    'P114',
    'V17',
    'R17',
    'P126',
    'V18',
    'R18',
    'T132',
    'P138',
    'V19',
    'R19',
    'P150',
    'V20',
    'R20',
    'T156',
    'U01',
    'U02',
    'U03',
    'U04',
    'U05',
    'U06',
    'PW',
], ordered=True)