import glob
import pandas as pd

path = "/Users/luiscruz/dev/designite/output"

def _read_multiple_csv(path):
    all_files = glob.glob(path)
    list_ = []
    for file_ in all_files:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    return pd.concat(list_, axis = 0, ignore_index = True)

type_metrics_frame = _read_multiple_csv(path + "/*/typeMetrics.csv")
method_metrics_frame = _read_multiple_csv(path + "/*/methodMetrics.csv")

import pdb; pdb.set_trace()
