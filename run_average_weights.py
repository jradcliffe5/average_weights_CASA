from code_mailer import headless
import sys, re, os
import pandas as pd
import numpy as np

inputfile = sys.argv[sys.argv.index('run_average_weights.py')+1]
inputs=headless(inputfile)
measurement_set = inputs['measurement_set'].split('[')[1].split(']')[0].split(',')
casa_path = inputs['casa_path']

print measurement_set

### First get the weights using the CASA tbtool
for i in measurement_set:
    print 'Getting average weights of %s' % i
    os.system('%scasa --nologger --log2term -c average_weights_ms.py %s' % (casa_path,i))

    ### convert to csv file
    weights = np.load('weights.npy')
    column_names = ['ANTENNA1','ANTENNA2','WEIGHT_average','WT_SPECTRUM_average','integrations']
    pd.DataFrame(data=weights, columns=column_names).to_csv('%s_av_wt.csv' % i.split('.ms')[0],index=False)
