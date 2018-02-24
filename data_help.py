import numpy as np
import pandas as pd

#democratic 0
#republican 1
def get_cols_voteDR_2016_2012_2008(df):
    voteDR_2016 = df['presvote16post_2016'].apply(lambda _: 0 if _=='Hillary Clinton' else (1 if _=='Donald Trump' else np.nan))
    voteDR_2012 = df['post_presvote12_2012'].apply(lambda _: 0 if _=='Barack Obama' else (1 if _=='Mitt Romney' else np.nan))
    voteDR_2008 = df['presvote08_baseline'].apply(lambda _: 0 if _=='Barack Obama' else (1 if _=='John McCain' else np.nan))
    
    return voteDR_2016, voteDR_2012, voteDR_2008


#input democratic 0, republican 1
#output democratic 0, republican to democratic 1, democratic to republic 2, republic 3
def get_cols_voteDR_convey(col_voteDR_cur, col_voteDR_pre):
    res = pd.Series(np.nan, index=col_voteDR_cur.index)
    res.loc[(col_voteDR_cur==0) & (col_voteDR_pre==0)]=0
    res.loc[(col_voteDR_cur==0) & (col_voteDR_pre==1)]=1
    res.loc[(col_voteDR_cur==1) & (col_voteDR_pre==0)]=2
    res.loc[(col_voteDR_cur==1) & (col_voteDR_pre==1)]=3
    return res

def make_dummy(data, cat_vars):
    for var in cat_vars:
        cat_list = pd.get_dummies(data[var], prefix=var)
        data1=data.join(cat_list)
        data=data1
    temp = data.columns.values.tolist()
    to_keep=[i for i in temp if i not in cat_vars]
    return data[to_keep]


