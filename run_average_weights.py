from code_mailer import headless
import sys, re, os
import pandas as pd
import numpy as np

inputfile = sys.argv[sys.argv.index('run_average_weights.py')+1]
inputs=headless(inputfile)
measurement_set = inputs['measurement_set'].split('[')[1].split(']')[0].split(',')
casa_path = inputs['casa_path']

### First get the weights using the CASA tbtool
for i in measurement_set:
    print 'Getting average weights of %s' % i
    os.system('%scasa --nologger --log2term -c average_weights_ms.py %s' % (casa_path,i))

    ### convert to csv file
    weights = np.load('weights.npy')
    column_names = ['ANTENNA1','ANTENNA2','WEIGHT_average','WT_SPECTRUM_average','integrations']
    df = pd.DataFrame(data=weights, columns=column_names)

    ### Make index column for simultaneous array solvers
    a = []
    for j in df.ANTENNA1: ## take from antenna1
        if (j not in a) == True:
            a = a + [j]
    for j in df.ANTENNA2: ## take from antenna2
        if (j not in a) == True:
            a = a + [j]

    antenna1index = []
    antenna2index = []
    for j in range(len(df)):
        #print np.where(a==weight[i][0])[0][0]
        antenna1index = antenna1index + [np.where(a==df.ANTENNA1[j])[0][0]]
        antenna2index = antenna2index + [np.where(a==df.ANTENNA2[j])[0][0]]

    antennaindex = pd.DataFrame({'ANT1_idx':np.array(antenna1index),'ANT2_idx':np.array(antenna2index)})

    pd.concat([df, antennaindex],axis=1).dropna().to_csv('%s_av_wt.csv' % i.split('.ms')[0],index=False)
    os.system('rm weights.npy')
    os.system('rm baseline_distribution.npy')
