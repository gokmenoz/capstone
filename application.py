from flask import Flask,render_template,request
import os
import geopandas as gpd
import pandas as pd
import json
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.embed import components
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column

#def map(findbyzip):
    

#pulling needs data
df=pd.read_csv('static/Data.csv')
df=df[['borocd','cd_short_title','son_issue_1','son_issue_2','son_issue_3']]
df['borocd']

#pulling shapefile
shapefile = 'static/nyc_geo/geo_export_6a5c9ed9-28b9-4120-bf21-93cf6790c332.shp'
gdf = gpd.read_file(shapefile)
gdf['boro_cd']=gdf['boro_cd'].astype('int')

#merging the needs with the shapes and making it json
merged = gdf.merge(df, left_on = 'boro_cd', right_on = 'borocd')

#building the map
def map(merged):
    temp=json.loads(merged.to_json())
    merged_geojson=json.dumps(temp)
    geosource = GeoJSONDataSource(geojson = merged_geojson)
    #Define a sequential multi-hue color palette.
    palette = brewer['Pastel2'][5]
    #Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette = palette, low = 100, high = 500, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}
    #Add hover tool
    TOOLTIPS="""
    <div>
        <div>
            <span style="font-size: 16px; font-weight:bold; color: #00BFFF">District:</span> <span style="font-size: 16px; color: #000000">@cd_short_title</span><br>
            <span style="font-size: 14px; font-weight:bold; color: #00BFFF;">1st need:</span> <span style="font-size: 14px; color: #000000"> @son_issue_1 </span><br>
            <span style="font-size: 12px; font-weight:bold; color: #00BFFF;">2nd need: </span> <span style="font-size: 12px; color: #000000">@son_issue_2</span><br>
            <span style="font-size: 10px; font-weight:bold; color: #00BFFF;">3rd need: </span> <span style="font-size: 10px; color: #000000">@son_issue_3</span>
        </div>
    </div>
    """
    hover = HoverTool(tooltips = TOOLTIPS)
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    #Create figure object.
    p = figure(title = 'NYC Districts', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'borocd', 'transform' : color_mapper},line_color = 'black', line_width = 0.25, fill_alpha = 1)
    return components(p)
    

app = Flask(__name__)

@app.route('/')
def index_lulu():
    script,div=map(merged)
    return render_template('capstone.html',div=div,script=script)
    
@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(os.path.join('static', path))

if __name__ == "__main__":
    app.debug=False
    app.run(host='0.0.0.0')
