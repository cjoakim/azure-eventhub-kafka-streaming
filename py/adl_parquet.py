
import os
import sys
import time
import traceback

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


# python adl_parquet.py data/-85212802_5f589aedca7a41eca29d306c9c62631a_1.parquet
# pyarrow.lib.ArrowInvalid: Mix of struct and list types not yet supported

if __name__ == '__main__':
    infile = sys.argv[1]
    print('infile: {}'.format(infile))

    # infile = 'data/openflights/airports.dat.txt'
    # tmpfile = 'tmp/airports.parquet'
    # df = read_pandas_dataframe(infile, ',', None)
    # tbl = pa.Table.from_pandas(df)
    # print('df  type: {}'.format(type(df)))   # <class 'pandas.core.frame.DataFrame'>
    # print('tbl type: {}'.format(type(tbl)))  # <class 'pyarrow.lib.Table'>
    # pq.write_table(tbl, tmpfile)

    tbl2 = pq.read_table(infile)
    print('tbl2 type: {}'.format(type(tbl2)))
    df2 = tbl2.to_pandas()
    print('df2  type: {}'.format(type(df2)))
    print('=== df2.describe()')
    print(df2.describe())
    print('=== df2.columns')
    print(df2.columns)
