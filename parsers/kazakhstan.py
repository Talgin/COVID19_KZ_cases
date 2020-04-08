import sys
import requests
import csv
import io

from collections import defaultdict
from .utils import store_data

# ------------------------------------------------------------------------
# Globals

regional_codes = {
   "AST": "Nur-Sultan",
   "ALA": "Almaty",
   "SHY": "Shymkent",
   "AKM": "Aqmola oblysy",
   "AKT": "Aqtöbe oblysy",
   "ALM": "Almaty oblysy",
   "ATY": "Atyraū oblysy",
   "VOS": "Shyghys Qazaqstan oblysy",
   "ZHA": "Zhambyl oblysy",
   "ZAP": "Batys Qazaqstan oblysy",
   "KAR": "Qaraghandy oblysy",
   "KUS": "Qostanay oblysy",
   "KZY": "Qyzylorda oblysy",
   "MAN": "Mangghystaū oblysy",
   "PAV": "Pavlodar oblysy",
   "SEV": "Soltüstik Qazaqstan oblysy",
   "YUS": "Türkistan oblysy",   
}

URL  = "https://raw.githubusercontent.com/talgin/COVID19_KZ_cases/master/COVID19_Cases_Bundeslaender_DE.csv"
LOC  = "case-counts/Asia/Central Asia/Kazakhstan"
cols = ['time', 'cases', 'deaths', 'hospitalized', 'icu', 'recovered']

# ------------------------------------------------------------------------
# Functions

def to_int(x):
    if x == "NA" or x == "":
        return None
    else:
        return int(x)

# ------------------------------------------------------------------------
# Main point of entry

def parse():
    r  = requests.get(URL)
    if not r.ok:
        print(f"Failed to fetch {URL}", file=sys.stderr)
        exit(1)
        r.close()

    regions = defaultdict(list)
    fd  = io.StringIO(r.text)
    rdr = csv.reader(fd)
    hdr = next(rdr)

    for row in rdr:
        date = row[0]
        if row[1] in bundesland_codes:
            bundesland = '-'.join(['KAZ', bundesland_codes[row[1]]])
            regions[bundesland].append([date, to_int(row[2]), to_int(row[3]), None, None, None])

    store_data(regions,  'kazakhstan', cols)