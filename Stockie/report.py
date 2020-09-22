# compilation 
import yfinance as yf
from IPython.core.display import display, HTML
import pandas as pd
from mpl_finance import candlestick2_ochl
import matplotlib.pyplot as plt
import json
import numpy as np
import os

import matplotlib.pyplot as plt
import base64
from io import BytesIO

local_path = '/'.join(yf.__file__.split('/')[:-2]) + '/Stockie/'

def create_label(df, timegap):
    return np.array(((df['Close'].shift(-timegap) >= df['Close'])*1).tolist()[:-timegap] + timegap*[np.nan])
    
def create_rate(df, timegap):
    return np.array((df['Close'].shift(-timegap) - df['Close'])/df['Close'])

def transform(ma,mi,x):
    return -321*x/(ma-mi) + (45*mi - 366*ma)/(mi-ma)

def generate_image(data, shape = 20):
    data_temp = data.copy().tail(shape).reset_index()

    my_dpi = 144
    fig = plt.figure(figsize=(800/my_dpi, 400/my_dpi), dpi=my_dpi)
    ax = fig.add_subplot(1,1,1)
    fig.subplots_adjust(bottom=0.1,left=0.1,right=.9,top=.9)
    candlestick2_ochl(ax, data_temp['Open'], data_temp['Close'], data_temp['High'], data_temp['Low'], 
                    width = 0.5, colordown='r', colorup = 'g')
    plt.ylim([data_temp[['Open','High','Low','Close']].min().min() - 30, data_temp[['Open','High','Low','Close']].max().max() + 30])
    ax.yaxis.tick_right()
    
    # awas ini kalau ganti shape
    plt.xticks([0,5,10,15,19], data_temp.loc[[0,5,10,15,19],'Date'].astype('str').values.tolist(), fontsize=7)
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    plt.close()
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html ='<img src=\'data:image/png;base64,{}\'>'.format(encoded)

    return html[:-1] + ' width="800" height="400" >'

def create_pattern_info_dict(data, label_length = 10):
    data_temp = data.copy()

    pattern = data_temp.columns.drop(['Date','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    for i in [1,2,3,4,5,6,7,8,9,10]:
        data_temp['label_{}'.format(i)] = create_label(data_temp, i) 
        data_temp['rate_{}'.format(i)] = create_rate(data_temp, i)

    pattern_info_dict = {}
    for i in pattern:
        try:
            pattern_info_dict[i] = [data_temp.groupby(i).count()['Date'][True]
                                    ,np.round(data_temp.groupby(i).mean()[['label_{}'.format(j) for j in range(1,label_length + 1)]].T[True].values*100,2).tolist()]
        except:
            continue

    return pattern_info_dict

def html_interactive_candlestick(data, top, left, shape = 20):
    temp = data.copy().tail(shape).reset_index()
    mi ,ma = temp[['Open','High','Low','Close']].min().min() - 30, temp[['Open','High','Low','Close']].max().max() + 30
    html_style_str = ''
    html_body_str = ''
    for i in range(shape):
        html_style_str += '''
.area-{label}{{
    height: {height};
    width: {width};
    top: {top};
    left: {left};
    border: {border}
}}
        '''.format(label = str(i+1),
           height = str(transform(ma,mi,temp.loc[i,'Low']) - transform(ma,mi,temp.loc[i,'High'])) + 'px',
           width = '13px',
           top = str(transform(ma,mi,temp.loc[i,'High']) + top) + 'px',
           left = str(107 + i*29.15 + left) + 'px',
           border = '0px solid #555')
        
        html_body_str += '''
<div class="invisible-area area-{label}">
    <div class="tooltip"><pre>
Date :{Date}
Open :{Open}
High :{High}
Low  :{Low}
Close:{Close}
Vol  :{Vol}</pre>
    </div>
</div>
        '''.format(label = str(i+1),
                   Date = str(temp.loc[i,'Date'])[:10],
                   Open = temp.loc[i,'Open'],
                   High = temp.loc[i,'High'],
                   Low = temp.loc[i,'Low'],
                   Close = temp.loc[i,'Close'],
                   Vol = temp.loc[i,'Volume'])

    return html_style_str, html_body_str

def create_pattern_det_dict(data, shape = 20):
    data_temp = data.copy().tail(shape).reset_index()

    horizontal_sum = data_temp[data_temp.columns.drop(['index', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])].sum(axis = 1)

    pattern_det_dict = {}
    for i in range(shape):
        if horizontal_sum[i] != 0:
            pattern_det_dict[i] = (data_temp == True).iloc[i][(data_temp == True).iloc[i]==True].index.tolist()
        else:
            continue
    
    return pattern_det_dict

def pattern_detection(data,pat_dict, top, left, shape = 20):
    
    with open(local_path + "pattern_img.json", 'r') as f:
        img_dict = json.load(f)
    with open(local_path + "pattern_type.json", 'r') as f:
        type_dict = json.load(f)    

    pattern_str_html_style = ''
    pattern_str_html_body = ''
    temp = data.copy().tail(shape).reset_index()
    mi ,ma = temp[['Open','High','Low','Close']].min().min() - 30, temp[['Open','High','Low','Close']].max().max() + 30
    for i in pat_dict:
        pattern_str_html_style += """
.area-pattern-{label}{{
    height: {height};
    width: {width};
    top: {top};
    left: {left};
    border: {border}
}}
        """ .format(label = str(i+1),
           height = '30' + 'px',
           width = '13px',
           top = str(transform(ma,mi,temp.loc[i,'High']) - 30 + top) + 'px',
           left = str(107 + i*29.15 + left) + 'px',
           border = '0px solid #555')
        
        image_text = ''
        for pat in pat_dict[i]:
            image_text +="""
        <pr>
        <p style="text-align:center;width:150px;">
        {pattern}<br>
        {image}<br>
        {types}<br>
        <p class="{pattern_id}" style="text-align:center">{text}</p>
        </p>
        </pr>
            """.format(image = img_dict[pat][:-1] + ' style= "border:1px solid #555">',
                       types = type_dict[pat].replace('BU', 'Bullish').replace('BE', 'Bearish').replace('CO', 'Continuation').replace('RE', 'Reversal').replace('I', 'Inconclusive'),
                   pattern = pat.replace("_", " "),
                   pattern_id = pat,
                   text = ''
                   )

        pattern_str_html_body += """
<div class = "invisible-area area-pattern-{label}" ><p class = "pattern"> ! </p>
    <div class="tooltip">
        {image_text}
    </div>
</div>
        """.format(label = str(i+1),
                   image_text = image_text)
    return pattern_str_html_style, pattern_str_html_body



def generate_HTML_CS_overview(data_full_pattern, shape = 20, top = 104, left = 13):
    with open(local_path + "pattern_type.json", 'r') as f:
        type_dict = json.load(f)   
        
    df = data_full_pattern.copy()
    real_html = generate_image(df, shape = 20)
    pattern_info_dict = create_pattern_info_dict(df)
    pattern_det_dict = create_pattern_det_dict(df)
    style, body = html_interactive_candlestick(data = df ,top = top, left = left, shape = 20)
    pattern_style, pattern_body = pattern_detection(data = df,pat_dict = pattern_det_dict, top = top, left = left)
    
    return '''
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body {font-family: Arial;}
        /* Style the tab */
        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
            }
        /* Style the buttons inside the tab */
        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
            }

        /* Change background color of buttons on hover */
        .tab button:hover {
            background-color: #ddd;
            }

        /* Create an active/current tablink class */
        .tab button.active {
            background-color: #ccc;
            }

        /* Style the tab content */
        .tabcontent {
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
            }
        table {
            width: border-collapse: collapse;
            border : 1px solid #ddd
            }
        tr:nth-child(even) {
            background-color: #dddddd;
            }
        th {
            padding: 10px;
            text-align: left;
            background-color: #4CAF50
            }
        td {
            padding: 10px;
            text-align: left;
            }
        
        .invisible-area {
            position: absolute;
            }

        .tooltip {
        display: none;
        background: white;
        border-radius: 5px;
        border: 1px black solid;
        position: absolute;
        background-color: white;
        border-radius: 5px;
        padding: 1px;
        z-index: 1;
        top: 0px;
        left: 150%;
        }

        .invisible-area .tooltip::after {
        content: "";
        position: absolute;
        top: 50%;
        right: 100%;
        margin-top: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: transparent black transparent transparent;
        
        }

        .invisible-area:hover .tooltip {
        display: block;
        }

        .pattern {
            background-color:powderblue;
            border-radius: 5px;
            text-align:center;
        }

        ''' + style + pattern_style +'''

        </style>
        
</head>
<body>

<h2>Report</h2>

<div class="tab">
    <button class="tablinks" onclick="openreport(event, 'Overview')">Overview</button>
    <button class="tablinks" onclick="openreport(event, 'Top Gain')">Top Gain</button>
    <button class="tablinks" onclick="openreport(event, 'Top Loss')">Top Loss</button>
</div>

<div id="Overview" class="tabcontent">
    ''' + real_html + body + pattern_body + '''
<input type="range" name="rangeInput" style ="position:absolute;left:93px; top:124px;" min="1" max="10" value = "5" onchange="updateTextInput(this.value);">
<input type="text" id="textInput" value="5" size="1" style ="position:absolute;left:233px; top:124px;" >

</div>
<div id="Top Gain" class="tabcontent">
    <h3>Top Gain</h3>
    <table>
        <tr>
            <th>Pattern</th>
            <th>Accuracy</th>
            <th>Rate</th>
        </tr>
        </tr>
    </table>
</div>

<div id="Top Loss" class="tabcontent">
    <h3>Top Loss</h3>
    <table>
        <tr>
            <th>Pattern</th>
            <th>Accuracy</th>
            <th>Rate</th>
        </tr>
    </table>
</div>

<script>


var acc_dicts = ''' + str(pattern_info_dict) + ''';
var type_dicts = ''' + str(type_dict) + ''';

updateTextInput(5)

function updateTextInput(val) {
    document.getElementById('textInput').value=val;
    for (var key in acc_dicts) {
        var x = document.getElementsByClassName(key);
        var i;
        for (i = 0; i < x.length; i++) {
            if ((type_dicts[key] == "BU RE")||(type_dicts[key] == "BU CO")||(type_dicts[key] == "I")){
                x[i].innerHTML = "<p style='color:green;font-size:20px;'>&#10138;<span style='color:black;font-size:15px;'>" 
                + acc_dicts[key][1][val-1] + "%</span></p>" +  (acc_dicts[key][0]*acc_dicts[key][1][val-1]/100).toFixed(0) + 
                " <span style='color:green;font-weight:10px'>Up</span> out of " + acc_dicts[key][0];
                }
            else{
                x[i].innerHTML = "<p style='color:red;font-size:20px;'>&#10136;<span style='color:black;font-size:15px;'>" 
                + (100 - acc_dicts[key][1][val-1]).toFixed(2) + "%</span></p>" +(acc_dicts[key][0]*(100-acc_dicts[key][1][val-1])/100).toFixed(0) + 
                " <span style='color:red;font-weight:10px'>Down</span> out of " + acc_dicts[key][0];
            }
            }
    }
        }

function openreport(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
</script>
   
</body>
</html> 

'''
