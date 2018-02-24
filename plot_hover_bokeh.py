import data_check
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.embed import components
import pandas as pd



def plot_D_R_dist_by_feature(df, df1, sel):
    
    the_dict={'x':[],'y':[],'des':[],'c':[]}
    colors = ['blue','green','yellow','red','black','pink','cyan']
    for i in range(len(sel)):
        feature=sel[i]
        df_data=df[['case_identifier',feature]]
        df_data['voteDR_2016']=df1['voteDR_2016']
        df_data=df_data.dropna()
        da=df_data.pivot_table(index=feature,columns='voteDR_2016',values='case_identifier',aggfunc=len)
        the_dict['x'] += list(da[0.0])
        the_dict['y'] += list(da[1.0])
        the_dict['des'] += [ feature+'_'+_ for _ in da.index]
        i_c = (i % len(colors))
        the_dict['c'] += [colors[i_c] for _ in da.index]


    #output_file("plot.html")
    source = ColumnDataSource(data=the_dict)
    hover = HoverTool(tooltips=[("(D,R)", "(@x,@y)"), ("desc", "@des")])

    p = figure(plot_width=600, plot_height=600, tools=[hover,'pan','box_zoom','wheel_zoom','reset','save'], x_axis_label='Democrat', y_axis_label='Republican',
           title="D/R population by features")
    p.circle('x','y',fill_color='c', line_color=None, size=10,source=source)

    #show(p)
    #save(p)
    script, div = components(p)
    return script,div



if __name__=='__main__':
    df = pd.read_table('data/VOTER_Survey_December16_Release1.csv',delimiter=',')
    voteDR_2016, voteDR_2012, voteDR_2008 = data_check.get_cols_voteDR_2016_2012_2008(df)
    voteDR_12to16=data_check.get_cols_voteDR_convey(voteDR_2016,voteDR_2012)
    voteDR_08to12=data_check.get_cols_voteDR_convey(voteDR_2012,voteDR_2008)
    df1=df[['case_identifier']]
    df1['voteDR_2016'], df1['voteDR_2012'], df1['voteDR_2008']= [voteDR_2016, voteDR_2012, voteDR_2008]
    df1['voteDR_12to16'],df1['voteDR_08to12'] = [voteDR_12to16, voteDR_08to12]


    sel=['obamaapp_2016','immi_contribution_2016','race_slave_2016','imiss_g_2016','univhealthcov_2016','healthreformbill_2016','envwarm_2016']
    plot_D_R_dist_by_feature(df, df1, sel)
