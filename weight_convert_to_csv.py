import pandas as pd
import os, sys, re
import numpy as np
from code_mailer import headless

measurement_set = sys.argv[sys.argv.index('weight_convert_to_csv.py')+1]

column_names = ['ANTENNA1','ANTENNA2','WEIGHT_average','WT_SPECTRUM_average','integrations']
pd.DataFrame(data=weights, columns=column_names).to_csv('%s_av_wt.csv' % measurement_set.split('.ms')[0],index=False)
