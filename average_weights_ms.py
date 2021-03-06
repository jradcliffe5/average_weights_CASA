### CASA script to expunge average weights and weight_spectrum from a CASA measurement set
## Author: J. Radcliffe, 2018
# If you use this script, please acknowledge me
# Caveats:
## - Only works on 2 pols atm
import os, re
import numpy as np

## Inputs ############################################################
'''
tb.open(msfile1,nomodify=False)
msfile1_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
tb.open(msfile2,nomodify=False)
msfile2_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
'''
### This function pulls the unique baseline numbers from the measurement set. The measurement sets are ordered such that ANTENNA1 is always < ANTENNA2


def pull_baselines(msfile):
    baseline_distribution = []
    t = tbtool()
    print 'Opening %s' % msfile
    t.open(msfile, nomodify=False)
    for colname in ['ANTENNA1']:
        if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
            for j in xrange(0,t.nrows()):
                if j % 10000 == 0:
                    print '%d/%d' % (j,t.nrows())
                a = [t.getcell(colname, j)]+[t.getcell('ANTENNA2', j)]
                if (a not in baseline_distribution) == True:
                    baseline_distribution = baseline_distribution + [a]
    return np.array(baseline_distribution)

def pull_baselines_quick(msfile):
    print 'Finding baseline pairs'
    antenna_list = []
    baseline_distribution = []
    t = tbtool()
    print 'Opening %s' % msfile
    t.open(msfile+'/ANTENNA', nomodify=False)
    for colname in ['FLAG_ROW']:
        if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
            for j in xrange(0,t.nrows()):
                if t.getcell(colname, j) != 1:
                    antenna_list = antenna_list + [j]

    for i in antenna_list:
        for j in antenna_list:
            if j>i:
                a = [i]+[j]
                baseline_distribution = baseline_distribution + [a]
    return np.array(baseline_distribution)


def find_baseline_arg(baseline,baseline_distribution):
    j = 0
    for i in baseline_distribution:
        if np.array_equal(i, baseline) == True:
            index = j
        j += 1
    try:
        return index
    except UnboundLocalError:
        print 'Baseline distribution doesn\'nt match, Quitting'
        exit()

t = tbtool()
theconcatvis = sys.argv[sys.argv.index('average_weights_ms.py')+1]

baseline_distribution = pull_baselines_quick(theconcatvis)
#baseline_distribution = pull_baselines(theconcatvis)

#print baseline_distribution
#print baseline_distribution2
#print baseline_distribution == baseline_distribution2

weight_table = np.append(baseline_distribution,np.zeros((baseline_distribution.shape[0],baseline_distribution.shape[1]+1)),axis=1)

np.save('baseline_distribution.npy',baseline_distribution)
t.open(theconcatvis, nomodify=False)
print 'Finding weights'
for colname in ['WEIGHT','WEIGHT_SPECTRUM']:
    print 'Finding averages from the %s column' % colname
    if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
        for j in xrange(0,t.nrows()):
            #if ((j+1) % 10000 == 0):
            #    print '%d/%d' % (j+1,(t.nrows()))
            #if (j+1==(t.nrows())):
            #    print '%d/%d ... Complete' % (j+1,t.nrows())
            a = t.getcell(colname, j)
            flags = t.getcell('FLAG', j)
            if colname == 'WEIGHT':
                flag_weight = [np.all(flags[0]),np.all(flags[1])]
                a = np.delete(a,np.argwhere(flag_weight)==True) ## Delete flagged entries
                if a.size != 0: ## Catches the data which is flagged i.e. WEIGHTS==0
                    baseline = np.array([t.getcell('ANTENNA1',j),t.getcell('ANTENNA2',j)])
                    #print baseline
                    baseline_arg = find_baseline_arg(baseline,baseline_distribution)
                    #print baseline_arg
                    weight_table[baseline_arg][2] = weight_table[baseline_arg][2] + np.average(a)
                    weight_table[baseline_arg][4] = weight_table[baseline_arg][4] + 1.
            if colname == 'WEIGHT_SPECTRUM':
                flag_weight = flags
                a = np.delete(a,np.argwhere(flag_weight)==True) ## Delete flagged entries
                if a.size != 0: ## Catches the data which is flagged i.e. WEIGHTS==0
                    baseline = np.array([t.getcell('ANTENNA1',j),t.getcell('ANTENNA2',j)])
                    baseline_arg = find_baseline_arg(baseline,baseline_distribution)
                    weight_table[baseline_arg][3] = weight_table[baseline_arg][3] + np.average(a)
                    #weight_table[baseline_arg][3] = weight_table[baseline_arg][3] + 1

for i in range(len(weight_table)):
    weight_table[i][2]= weight_table[i][2]/weight_table[i][4]
    weight_table[i][3]= weight_table[i][3]/weight_table[i][4]

np.save('weights.npy',weight_table)
os.system('rm casa*log')

t.close()
