#!/usr/bin/env python
# coding: utf-8

# In[6]:


import dill
from bokeh.io import curdoc,output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import (LinearColorMapper, ColorBar,GMapOptions, Patches,GMapPlot,Range1d,HoverTool,
                         WheelZoomTool,PanTool,TapTool,CustomJS,BoxZoomTool,OpenURL)
from bokeh.palettes import brewer
from bokeh.plotting import gmap,curdoc
from bokeh.models.widgets import RadioGroup
from bokeh.layouts import widgetbox, row, column
from bokeh.models import CustomJS
import pandas as pd


# In[7]:


merged=dill.load(open('static/merged.pkd','rb'))
Y_2024=dill.load(open('static/Y_2024.pkd','rb'))

# In[8]:


def get_coords(poly):
    if poly.type == 'Polygon':
        x,y=poly.exterior.xy
        return [list(x),list(y)]
    else:
        X=[]
        Y=[]
        for p in poly:
            x,y=p.exterior.xy
            X.append(list(x))
            Y.append(list(y))
        return [X,Y]



# In[9]:

merged=pd.merge(merged, Y_2024, left_on='boro_cd', right_on='cd')


from bokeh.models import ColumnDataSource
X=[]
Y=[]
Need_1=[]
Need_2=[]
Need_3=[]
CD=[]
Pov_rate=[]
Need_1_2024=[]
Need_2_2024=[]
Need_3_2024=[]

for i in range(55):
    coords=get_coords(merged['geometry'][i])
    if len(coords[0])>50:
        X.append(coords[0])
        Y.append(coords[1])
        Need_1.append(merged['son_issue_1'][i])
        Need_2.append(merged['son_issue_2'][i])
        Need_3.append(merged['son_issue_3'][i])
        CD.append(merged['boro_cd'][i])
        Pov_rate.append(merged['poverty_rate'][i])
        Need_1_2024.append(merged['top3'][i][0])
        Need_2_2024.append(merged['top3'][i][1])
        Need_3_2024.append(merged['top3'][i][2])
    else:
        for j in range(len(coords[0])):
            X.append(coords[0][j])
            Y.append(coords[1][j])
            Need_1.append(merged['son_issue_1'][i])
            Need_2.append(merged['son_issue_2'][i])
            Need_3.append(merged['son_issue_3'][i])
            CD.append(merged['boro_cd'][i])
            Pov_rate.append(merged['poverty_rate'][i])
            Need_1_2024.append(merged['top3'][i][0])
            Need_2_2024.append(merged['top3'][i][1])
            Need_3_2024.append(merged['top3'][i][2])
            
source= ColumnDataSource(
    data=dict(
        lat=Y,
        lon=X,
        son_issue_1=Need_1,
        son_issue_2=Need_2,
        son_issue_3=Need_3,
        cd=CD,
        X=CD,
        PR=Pov_rate,
        pred_1=Need_1_2024,
        pred_2=Need_2_2024,
        pred_3=Need_3_2024
    )
)

# In[10]:


palette = brewer['Pastel2'][5]

color_mapper=LinearColorMapper(palette=palette,low=100,high=500)

# In[11]:


TOOLTIPS="""
    <div>
        <div>
            <span style="font-size: 16px; font-weight:bold; color: #00BFFF;">District:</span> <span style="font-size: 14px; color: #000000"> @cd </span><br>
            <span style="font-size: 14px; font-weight:bold; color: #00BFFF;">1st need:</span> <span style="font-size: 14px; color: #000000"> @son_issue_1 </span><br>
            <span style="font-size: 12px; font-weight:bold; color: #00BFFF;">2nd need: </span> <span style="font-size: 12px; color: #000000">@son_issue_2</span><br>
            <span style="font-size: 10px; font-weight:bold; color: #00BFFF;">3rd need: </span> <span style="font-size: 10px; color: #000000">@son_issue_3</span>
        </div>
    </div>
    """

TOOLTIPS_PRED="""
    <div>
        <div>
            <span style="font-size: 16px; font-weight:bold; color: #00BFFF;">District:</span> <span style="font-size: 14px; color: #000000"> @cd </span><br>
            <span style="font-size: 14px; font-weight:bold; color: #00BFFF;">1st need:</span> <span style="font-size: 14px; color: #000000"> @pred_1 </span><br>
            <span style="font-size: 12px; font-weight:bold; color: #00BFFF;">2nd need: </span> <span style="font-size: 12px; color: #000000">@pred_2</span><br>
            <span style="font-size: 10px; font-weight:bold; color: #00BFFF;">3rd need: </span> <span style="font-size: 10px; color: #000000">@pred_3</span>
        </div>
    </div>
    """

TOOLTIPS_PR="""
    <div>
        <div>
            <span style="font-size: 16px; font-weight:bold; color: #00BFFF;">District:</span> <span style="font-size: 14px; color: #000000"> @cd </span><br>
            <span style="font-size: 14px; font-weight:bold; color: #00BFFF;">Poverty Rate:</span> <span style="font-size: 14px; color: #000000"> @PR </span><br>
        </div>
    </div>
    """

# In[ ]:


TOOLTIPS="""
    <div>
        <div>
            <span style="font-size: 16px; font-weight:bold; color: #00BFFF;">District:</span> <span style="font-size: 14px; color: #000000"> @cd </span><br>
            <span style="font-size: 14px; font-weight:bold; color: #00BFFF;">1st need:</span> <span style="font-size: 14px; color: #000000"> @son_issue_1 </span><br>
            <span style="font-size: 12px; font-weight:bold; color: #00BFFF;">2nd need: </span> <span style="font-size: 12px; color: #000000">@son_issue_2</span><br>
            <span style="font-size: 10px; font-weight:bold; color: #00BFFF;">3rd need: </span> <span style="font-size: 10px; color: #000000">@son_issue_3</span>
        </div>
    </div>
    """


# In[ ]:


def radio_handler(new):
    if new==0:
        #attr=radio_group.labels[new]
        source.data['X']=source.data['cd']
        color_mapper.low=min(source.data['cd'])
        color_mapper.high=max(source.data['cd'])
        hover.tooltips=TOOLTIPS
        layout.children[0].map_options.lng=-74.00712
        layout.children[0].map_options.lat=40.71455
        layout.children[0].width=1200
        layout.children[0].height=1000
        layout.children[0].map_options.zoom=11
    if new==1:
        source.data['X']=source.data['cd']
        color_mapper.low=min(source.data['cd'])
        color_mapper.high=max(source.data['cd'])
        hover.tooltips=TOOLTIPS_PRED
        layout.children[0].map_options.lng=-74.00712
        layout.children[0].map_options.lat=40.71455
        layout.children[0].width=1200
        layout.children[0].height=1000
        layout.children[0].map_options.zoom=11
    if new==2:
        source.data['X']=source.data['cd']
        color_mapper.low=min(source.data['cd'])
        color_mapper.high=max(source.data['cd'])
        hover.tooltips=TOOLTIPS_PRED
        layout.children[0].map_options.lng=-73.9712
        layout.children[0].map_options.lat=40.7831
        layout.children[0].width=600
        layout.children[0].height=1200
        layout.children[0].map_options.zoom=13



# In[ ]:


map_options=GMapOptions(lat=40.71455, lng=-74.00712,map_type="roadmap",zoom=11)
plot=GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options,width=1200,height=1000)
plot.api_key="AIzaSyAG6g5nqyGVnwHjvA-l4bpG0sBoOJZ75yA"


plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None

#Add patch renderers to figure. 
patch=Patches(xs='lon',ys='lat',fill_color={'field':'X', 'transform' : color_mapper},line_color = 'black', fill_alpha = 0.5)
plot.add_glyph(source,patch)

# patch_Pov_rate=Patches(xs='lon',ys='lat',legend='Poverty Rates',fill_color={'field':'PR', 'transform' : color_mapper_Pov_rate},line_color = 'black', fill_alpha = 0.5)
# plot.add_glyph(source_Pov_rate,patch_Pov_rate)

#Add hover tool
hover = HoverTool(tooltips=TOOLTIPS)
plot.add_tools(hover,WheelZoomTool(), PanTool(),BoxZoomTool())

#Adding Radio Group to switch glyphs
    
radio_group = RadioGroup(labels=["Current", "2024 Predictions",'Manhattan'],active=0)
radio_group.on_click(radio_handler)
# taptool=TapTool(callback=taptool_callback)
# plot.add_tools(taptool)
layout = column(plot,widgetbox(radio_group),sizing_mode='fixed')

curdoc().add_root(layout)
