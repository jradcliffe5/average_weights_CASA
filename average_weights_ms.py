t = tbtool()
## Inputs ############################################################
'''
tb.open(msfile1,nomodify=False)
msfile1_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
tb.open(msfile2,nomodify=False)
msfile2_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
'''
print sys.argv
theconcatvis = sys.argv[sys.argv.index('average_weights_ms.py')+1]

### This function pulls the unique baseline numbers from the measurement set. The measurement sets are ordered such that ANTENNA1 is always < ANTENNA2
def pull_baselines(msfile):
    baseline_distribution = []
    t = tbtool()
    t.open(msfile, nomodify=False)
    for colname in ['ANTENNA1']:
        if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
            for j in xrange(0,t.nrows()):
                a = [t.getcell(colname, j)]+[t.getcell('ANTENNA2', j)]
                if (a not in baseline_distribution) == True:
                    baseline_distribution = baseline_distribution + [a]
    return baseline_distribution


x = pull_baselines(theconcatvis)
print np.array(x).T
'''
t.open(theconcatvis, nomodify=False)
for colname in [ 'WEIGHT', 'WEIGHT_SPECTRUM']:
    if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
        for j in xrange(0,t.nrows()):
            a = t.getcell(colname, j)
            print a
'''
'''
for colname in ['SIGMA']:
	if (wscale > 0. and colname in t.colnames()) and (t.iscelldefined(colname,0)):
		sscale = 1./sqrt(wscale)
		for j in xrange(0,t.nrows()):
			a = t.getcell(colname, j)
			a *= sscale
			t.putcell(colname, j, a)
'''
t.close()
