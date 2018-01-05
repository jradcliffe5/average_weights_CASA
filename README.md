## average_weights_CASA
Noted caveats:
 - Only works for 2 polarisation datasets (currently hard-wired). I will generalise this when I have time. We should be ok at the moment because our data is just LL, RR.
 - Flagging checks currently only work for completely flagged integrations (i.e. time-based flagging). A full channel based one is possible but involves alot of various matrices in order to count integrations per channel.

The code can be found here: https://github.com/jradcliffe5/average_weights_CASA

To run it you need to edit `inputs.txt`. And then you can run the script using python `run_average_weights.py inputs.txt`

Note that your python distr. will need the pandas and numpy packages. The script will output a .csv per measurement defined in inputs.txt. The csv file has 7 columns:

ANTENNA1 = antenna1 number in ms
ANTENNA2 = antenna2 number in ms
WEIGHT_average = average of the weight column for baseline ANTENNA1xANTENNA2 (averaged across polarisations)
WT_SPECTRUM_average =  average of the weight_spectrum column (channel-based weights) for baseline ANTENNA1xANTENNA2 (averaged across polarisations)
integrations = number of integrations per baseline that are not fully flagged
ANT1_idx = used for solvers (when you assign x[0] x[1] for variables so that any gaps in ant. numbers are avoided)
ANT2_idx = ''
