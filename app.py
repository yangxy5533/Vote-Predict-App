from flask import Flask, render_template, request, redirect
import os
import requests
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import data_check
import plot_hover_bokeh



def load_survey_data(filename):
    df = pd.read_table(filename,delimiter=',')
    voteDR_2016, voteDR_2012, voteDR_2008 = data_check.get_cols_voteDR_2016_2012_2008(df)
    voteDR_12to16=data_check.get_cols_voteDR_convey(voteDR_2016,voteDR_2012)
    voteDR_08to12=data_check.get_cols_voteDR_convey(voteDR_2012,voteDR_2008)
    df1=df[['case_identifier']]
    df1['voteDR_2016'], df1['voteDR_2012'], df1['voteDR_2008']= [voteDR_2016, voteDR_2012, voteDR_2008]
    df1['voteDR_12to16'],df1['voteDR_08to12'] = [voteDR_12to16, voteDR_08to12]
    return df, df1


def empty_data_from_coeffile(filename, start=0):
    temp= pd.read_table(filename,delimiter=',')
    df = pd.DataFrame(columns=list(temp.iloc[start:,0]))
    return df

def add_one_row_forfit(df,the_data):
    if df.shape[0]==0:
        i=0
    else:
        i=df.index[-1]+1
    df.loc[i]=0
    for da in the_data:
        the_col = da+'_'+the_data[da]
        df.loc[i,the_col]=1
    return df
     
def add_one_row_forloaddata(df,the_data):
    if df.shape[0]==0:
        i=0
    else:
        i=df.index[-1]+1
    df.loc[i]=the_data
    return df
   

def get_prob_DtoR_RtoD(p,dp,dfprob):
    temp=dfprob[(dfprob['proba1']<=p+dp) & (dfprob['proba1']>=p-dp)]
    D = temp[temp['voteDR_12to16']==0.0].shape[0]
    RtoD = temp[temp['voteDR_12to16']==1.0].shape[0]
    DtoR = temp[temp['voteDR_12to16']==2.0].shape[0]
    R = temp[temp['voteDR_12to16']==3.0].shape[0]
    return pd.Series([float(DtoR)/float(D+DtoR), float(RtoD)/float(R+RtoD)])

def process_data(the_app):
    est=the_app.modelest
    tofitData=the_app.tofitData
    dfprob=the_app.surveyData_dfprob

    y_pred = est.predict(tofitData)
    resultData = the_app.loadData.copy()
    resultData.columns = [ _.replace('_2016','') for _ in the_app.loadData.columns]
    resultData['prediction(0-D,1-R)'] = y_pred
    resultData['score(0-1)'] = est.predict_proba(tofitData)[:,1]
    resultData[['fraction of switcher in D', 'fraction of switcher in R']]= resultData['score(0-1)'].apply(lambda _: get_prob_DtoR_RtoD(_,0.1,dfprob))

    

    resultData.to_html('templates/pred_result.html')

#need the_app.modelest, app.surveyData_df, app.surveyData_df1,the_app.loadData.columns
def surveyData_prob(the_app):
    est = the_app.modelest
    df = the_app.surveyData_df
    df1 = the_app.surveyData_df1
    sel = list(the_app.loadData.columns)
    df2 = df[sel]
    df2 = df2.dropna()
    df2=data_check.make_dummy(df2, sel)

    df_data = pd.DataFrame(est.predict_proba(df2),index=df2.index, columns=['proba0','proba1'])
    df_data['predict']=est.predict(df2)
    df_data=df_data.join(df1[['voteDR_12to16']])
    return df_data



app = Flask(__name__)
app.surveyData_df, app.surveyData_df1 = load_survey_data('data/VOTER_Survey_December16_Release1.csv')
app.tofitData = empty_data_from_coeffile('data/model_param.txt',start=1)
app.loadData = empty_data_from_coeffile('data/model_input.txt',start=0)
app.modelest = joblib.load('data/logreg.pkl')
app.surveyData_dfprob = surveyData_prob(app)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        app.tofitData = empty_data_from_coeffile('data/model_param.txt',start=1)
        app.loadData = empty_data_from_coeffile('data/model_input.txt',start=0)
        filename='templates/pred_result.html'
        if os.path.exists(filename):
            os.remove(filename)

        return render_template('index.html')



@app.route('/votedistr.html',methods=['GET','POST'])
def votedistr():
    if request.method == 'GET':
        return render_template('votedistr.html')
    else:
        df=app.surveyData_df
        df1= app.surveyData_df1
        sel =  request.form.getlist('features')
        script,div = plot_hover_bokeh.plot_D_R_dist_by_feature(df, df1, sel)
        return render_template('votedistr.html', script=script, div=div)

@app.route('/votepred.html',methods=['GET','POST'])
def votedata():
    if request.method == 'GET':
        return render_template('votepred.html')
    else:
        the_data={}
        the_data['obamaapp_2016'] = request.form['obamaapp_2016']
        the_data['immi_contribution_2016'] = request.form['immi_contribution_2016']
        the_data['race_slave_2016'] = request.form['race_slave_2016']
        the_data['imiss_g_2016'] = request.form['imiss_g_2016']
        the_data['univhealthcov_2016'] = request.form['univhealthcov_2016']
        the_data['healthreformbill_2016'] = request.form['healthreformbill_2016']
        the_data['envwarm_2016'] = request.form['envwarm_2016']
        app.tofitData = add_one_row_forfit(app.tofitData,the_data)
        app.loadData = add_one_row_forloaddata(app.loadData, the_data)


    process_data(app)

    print(request.form)
    return render_template('votepred.html')
    #return render_template('pred_result.html')

@app.route('/pred_result.html',methods=['GET','POST'])
def pred_result():
    if request.method == 'GET':
        return render_template('pred_result.html')


if __name__ == '__main__':
    port = int(os.environ.get('port', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    #app.run(host='0.0.0.0', port=port, debug=False)
 
