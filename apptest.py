import re
sequence = 'afrykanerskojezyczny'
queries = [ 'afrykanerskojezycznym', 'afrykanerskojezyczni',
            'nieafrykanerskojezyczni','afrykanerskojezyczny' ]
for q in queries:
    m = re.search(r'(%s){e<=2}'%q, sequence)
    print('match' if m else 'nomatch')