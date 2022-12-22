import pyasn
import pandas as pd
import os
from matplotlib import pyplot as plt


asndb = pyasn.pyasn('ipasn.20220929.dat')
results = pd.read_csv(os.path.join('..', 'data', 'result.csv'))
con_ips = results[(results.type == 'lg') | (results.type == 'pf')]['ip'].tolist()
uncon_ips = results[(results.type != 'lg') & (results.type != 'pf')]['ip'].tolist()
con_asns = {}
uncon_asns = {}
asns = {}
for ip in con_ips:
    asn = asndb.lookup(ip)[0]
    if asn in con_asns:
        con_asns[asn] += 1
    else:
        con_asns[asn] = 1
    if asn in asns:
        asns[asn] += 1
    else:
        asns[asn] = 1
for ip in uncon_ips:
    asn = asndb.lookup(ip)[0]
    if asn in uncon_asns:
        uncon_asns[asn] += 1
    else:
        uncon_asns[asn] = 1
    if asn in asns:
        asns[asn] += 1
    else:
        asns[asn] = 1
con_asns = sorted(con_asns.items(), key=lambda x: x[1], reverse=True)
uncon_asns = sorted(uncon_asns.items(), key=lambda x: x[1], reverse=True)
print('Top 10 ASNs for controllable landmarks:', con_asns[:10])
print('Top 10 ASNs for uncontrollable landmarks:', uncon_asns[:10])
print('len of con_asns', len(con_asns))
print('len of uncon_asns', len(uncon_asns))
print('len of all_asns', len(asns))
# plt.pie(con_asns.values(), labels=con_asns.keys())
# plt.title('AS Distribution of Con IPs')
# plt.savefig('con_as_distribution.png')
# plt.close()
# plt.pie(uncon_asns.values(), labels=uncon_asns.keys())
# plt.title('AS Distribution of Uncon IPs')
# plt.savefig('uncon_as_distribution.png')
# plt.close()
