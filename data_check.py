import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import seaborn as sns

#columns_avail['pid3']=['pid3_2016', 'pid3_baseline', 'post_pid3_2012']
def columns_avail(df):
    ques_sets = {}
    for x in df.columns:
        da = x.split('_')
        if da[-1]=='2016':
            the_key = '_'.join(da[:-1])
        elif da[-1]=='baseline':
            the_key = '_'.join(da[:-1])
        elif da[0] == 'post' and da[-1]=='2012':
            the_key = '_'.join(da[1:-1])
        else:
            the_key = x
        if not the_key in ques_sets:
            ques_sets[the_key]=[]
        ques_sets[the_key].append(x)
    return ques_sets

def format_answer_set_1(col_x):
    ans = col_x.fillna('nan').unique() #fill na
    ans = [ str(_).lower() for _ in ans] #upper to lower
    ans = ['not sure' if _=="don't know" else _ for _ in ans] #don't know to not sure'
    ans = sorted(ans) #sort
    return ans

def format_col_1(col_x):
    ans = col_x.fillna('nan')
    ans = ans.apply(lambda _: str(_).lower())
    ans = ans.apply(lambda _: 'not sure' if _=="don't know" else _)
    return ans


#
def answer_avail(df, ignoreabove=100):
    formatans_to_q = {}
    for x in df.columns:
        ans = format_answer_set_1(df[x]) 
        if len(ans)>ignoreabove:
            continue

        ans = tuple(ans)
        if not ans in formatans_to_q:
            formatans_to_q[ans]=[]
        formatans_to_q[ans].append(x)
    return formatans_to_q


#change on df itself, on cols
#use the_ansToNumTrans to translate values other than nan and not sure
#treat nan and not sure specifically
def numer_data(df, cols, the_ansToNumTrans, ignore_fail=False, nan_val=0.5, notsure_val=0.5):
    for col in cols:
        da = df[col]
        the_col = format_col_1(da)
        ans = sorted(the_col.unique())
        ans = [_ for _ in ans if (_!='nan' and _!='not sure')] #remove nan and not sure to match with translation rule
        ans = tuple(ans)
        if not ans in the_ansToNumTrans:
            if ignore_fail:
                continue
            print('Do not know how to translate for '+col, ans)
            sys.exit()
        the_ansToNum = the_ansToNumTrans[ans]
        the_ansToNum['nan']=nan_val
        the_ansToNum['not sure']=notsure_val
        df[col] = the_col.apply(lambda _:the_ansToNum[_])
    return df


######## some columns ############
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


def html_checkbox_line1(field,id):
    x='<input type="checkbox" name="features" value="{0}" Id="check{1}"  onclick="myFunction(\'check{1}\',\'text{1}\')"/>{0}<br>'.format(field,id)
    return x

def html_checkbox_line2(des,id):
    x='<p id="text{1}" style="display:none">{0}</p>'.format(des,id)
    return x

def get_html_lines(filename='others/table_view_id_2016_and_baseline.txt'):
    df=pd.read_table(filename,delimiter='|')
    df=df[df['use']=='1']
    df['id']=range(df.shape[0])
    df['field_2016']=df['field'].apply(lambda _ : _+'_2016')
    df['field_baseline']=df['field'].apply(lambda _ : _+'_baseline')

    for i in range(df.shape[0]):
        explanation,id,field_2016,field_baseline=df.iloc[i,2:]
        print(html_checkbox_line1(field_2016,id))
        print(html_checkbox_line2(explanation,id))
    return





########## learning test ###########
def make_dummy(data, cat_vars):
    for var in cat_vars:
        cat_list = pd.get_dummies(data[var], prefix=var)
        data1=data.join(cat_list)
        data=data1
    temp = data.columns.values.tolist()
    to_keep=[i for i in temp if i not in cat_vars]
    return data[to_keep]


#da_class = {col_name: np.array}
def get_cloest_class(df, da_class):
    df_res = df.copy()
    for x in df.columns:
        temp = da_class[x]
        df_res[x] = df[x].apply(lambda _:temp[(abs(temp-_)).argmin()])
    return df_res
	
