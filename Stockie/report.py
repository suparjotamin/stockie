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
import Stockie

#local_path = '/'.join(yf.__file__.split('/')[:-2]) + '/Stockie/'
local_path = Stockie.__file__[:-11]

def create_label(df, timegap):
    return np.array(((df['Close'].shift(-timegap) >= df['Close'])*1).tolist()[:-timegap] + timegap*[np.nan])
    
def create_rate(df, timegap):
    return np.array((df['Close'].shift(-timegap) - df['Close'])/df['Close'])

def transform(ma,mi,x):
    return -321*x/(ma-mi) + (45*mi - 366*ma)/(mi-ma)

def plot_ma_mi_scaler(data_temp, shape = 20):
    range = data_temp[['Open','High','Low','Close']].max().max() - data_temp[['Open','High','Low','Close']].min().min()
    if range >3000:
        scaler = 700
    elif range > 2000:
        scaler = 500
    elif range > 500:
        scaler = 50
    elif range > 100:
        scaler = 10
    elif range > 20:
        scaler = 5
    elif range > 5:
        scaler = 0.3
    else:
        scaler = 0.1
    return scaler

def generate_image(data, shape = 20, name = ""):
    data_temp = data.copy().tail(shape).reset_index()

    my_dpi = 144
    fig = plt.figure(figsize=(800/my_dpi, 400/my_dpi), dpi=my_dpi)
    ax = fig.add_subplot(1,1,1)
    fig.subplots_adjust(bottom=0.1,left=0.1,right=.9,top=.9)
    candlestick2_ochl(ax, data_temp['Open'], data_temp['Close'], data_temp['High'], data_temp['Low'], 
                    width = 0.5, colordown='r', colorup = 'g')
    plt.ylim([data_temp[['Open','High','Low','Close']].min().min() - plot_ma_mi_scaler(data_temp), 
              data_temp[['Open','High','Low','Close']].max().max() + plot_ma_mi_scaler(data_temp)])
    ax.yaxis.tick_right()
    
    # awas ini kalau ganti shape
    plt.xticks([0,5,10,15,19], data_temp.loc[[0,5,10,15,19],'Date'].astype('str').values.tolist(), fontsize=7)
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    plt.close()
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html ='<img src=\'data:image/png;base64,{encoded}\'>'.format(encoded = encoded, name = name)

    return html[:-1] + ' width="800" height="400" >'

def create_pattern_info_dict(data, label_length = 10, name = " "):
    data_temp = data.copy()

    pattern = data_temp.columns.drop(['Date','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    for i in [1,2,3,4,5,6,7,8,9,10]:
        data_temp['label_{}'.format(i)] = create_label(data_temp, i) 
        data_temp['rate_{}'.format(i)] = create_rate(data_temp, i)

    pattern_info_dict = {}
    for i in pattern:
        try:
            pattern_info_dict[i+ " " + name] = [data_temp.groupby(i).count()['Date'][True]
                                    ,np.round(data_temp.groupby(i).mean()[['label_{}'.format(j) for j in range(1,label_length + 1)]].T[True].values*100,2).tolist()]
        except:
            continue

    return pattern_info_dict

def html_interactive_candlestick(data, top, left, shape = 20, name = ""):
    temp = data.copy().tail(shape).reset_index()
    mi ,ma = temp[['Open','High','Low','Close']].min().min() - plot_ma_mi_scaler(temp), temp[['Open','High','Low','Close']].max().max() + plot_ma_mi_scaler(temp)
    html_style_str = ''
    html_body_str = ''
    for i in range(shape):
        html_style_str += '''
.area-{name}-{label}{{
    height: {height};
    width: {width};
    top: {top};
    left: {left};
    border: {border};
    position: absolute;
}}
        '''.format(label = str(i+1),
           height = str(transform(ma,mi,temp.loc[i,'Low']) - transform(ma,mi,temp.loc[i,'High'])) + 'px',
           width = '13px',
           top = str(transform(ma,mi,temp.loc[i,'High']) + top) + 'px',
           left = str(107 + i*29.15 + left) + 'px',
           border = '0px solid #555',
           name = name)
        
        html_body_str += '''
<div class="invisible-area area-{name}-{label}">
    <div class="tooltip"><pre style="z-index:10;color:black;">
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
                   Open = np.round(temp.loc[i,'Open'],2),
                   High = np.round(temp.loc[i,'High'],2),
                   Low = np.round(temp.loc[i,'Low'],2),
                   Close = np.round(temp.loc[i,'Close'],2),
                   Vol = temp.loc[i,'Volume'],
                   name = name)

    return html_style_str, html_body_str

def create_pattern_det_dict(data, shape = 20, name = ""):
    data_temp = data.copy().tail(shape).reset_index()

    horizontal_sum = data_temp[data_temp.columns.drop(['index', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])].sum(axis = 1)

    pattern_det_dict = {}
    for i in range(shape):
        if horizontal_sum[i] != 0:
            pattern_det_dict[i] = (data_temp == True).iloc[i][(data_temp == True).iloc[i]==True].index.tolist()
        else:
            continue
    
    return pattern_det_dict

def pattern_detection(data,pat_dict, top, left, shape = 20, name = ""):
    
    with open(local_path + "pattern_img.json", 'r') as f:
        img_dict = json.load(f)
    with open(local_path + "pattern_type.json", 'r') as f:
        type_dict = json.load(f)    

    pattern_str_html_style = ''
    pattern_str_html_body = ''
    temp = data.copy().tail(shape).reset_index()
    mi ,ma = temp[['Open','High','Low','Close']].min().min() - plot_ma_mi_scaler(temp), temp[['Open','High','Low','Close']].max().max() + plot_ma_mi_scaler(temp)
    for i in pat_dict:
        pattern_str_html_style += """
.area-{name}-pattern-{label}{{
    height: {height};
    width: {width};
    top: {top};
    left: {left};
    border: {border};
    position: absolute;
}}
        """ .format(label = str(i+1),
           height = '30' + 'px',
           width = '13px',
           top = str(transform(ma,mi,temp.loc[i,'High']) - 30 + top) + 'px',
           left = str(107 + i*29.15 + left) + 'px',
           border = '0px solid #555',
           name = name)
        
        image_text = ''
        for pat in pat_dict[i]:
            if pat != pat_dict[i][0]:
                image_text += "<hr style=\"color:black;\">"

            image_text +="""
        <pr style="text-align:center;">
        <p style="text-align:center;width:150px;">
        <b>{pattern}</b><br>
        {image}<br>
        {types}<br>
        <div class="{pattern_id}" style="text-align:center;">{text}</div>
        </p>
        </pr>
            """.format(image = img_dict[pat][:-1] + ' style= "border:1px solid #555;margin-left:auto; margin-right:auto;">',
                       types = type_dict[pat].replace('BU', 'Bullish').replace('BE', 'Bearish').replace('CO', 'Continuation').replace('RE', 'Reversal').replace('I', 'Inconclusive'),
                   pattern = pat.replace("_", " "),
                   pattern_id = pat + " " + name,
                   text = ''
                   )

        pattern_str_html_body += """
<div class = "invisible-area area-{name}-pattern-{label}" ><p class = "pattern" style="text-align:center;" align="center"> ! </p>
    <div class="tooltip">
        {image_text}
    </div>
</div>
        """.format(label = str(i+1),
                   image_text = image_text,
                   name = name)
    return pattern_str_html_style, pattern_str_html_body

def create_stacked(real_html, body, pattern_body, style, pattern_style):
    full_style = ""
    full_overview_body = ""

    for i in real_html:
        full_style += style[i] + pattern_style[i] 
        full_overview_body += """
<div id = "{name}">
    {a}  
    {b}  
    {c} 
</div>
""".format(name = i,
           a = real_html[i],
           b = body[i],
           c = pattern_body[i])

    return full_style, full_overview_body

def create_option_image(data):
    option_image = '<select id="mySelect" onchange="changeimage(this.value)" style="position:absolute;;left:150px; top:14px;">'
    for name in data:
        option_image += '\n <option value="{name}">{name}</option>'.format(name = name)
    option_image += '\n </select>'
    return option_image

def get_recap_table(df):
    res = pd.DataFrame()
    for stock in df:
        temp_df = df[stock].tail(10).copy()
        temp_df = temp_df[temp_df.columns.drop(['Open','High','Low','Close','Adj Close','Volume'])].set_index('Date')
        temp_df = temp_df[temp_df==True].stack().reset_index().drop(0, axis = 1)
        temp_df['Stock'] = stock
        temp_dict = create_pattern_info_dict(df[stock])

        temp_df['Up Rate'] = [np.round(np.mean(temp_dict[i+'  '][1]),2) for i in temp_df['level_1']]
        temp_df['Count'] = [temp_dict[i+'  '][0] for i in temp_df['level_1']]
        temp_df['level_1'] = [i.replace('_', ' ') for i in temp_df['level_1']]
        res = pd.concat([res,temp_df], axis = 0)

    res = res.sort_values(['Up Rate', 'Date'], ascending = False)
    res.columns = ['Date', 'Pattern', 'Stock','Up Rate', 'Count']
    res = res.reset_index().drop('index', axis = 1)
    res['Date'] = [str(i)[:10] for i in res['Date']]
    res['Up Rate'] = [str(i) + '%' for i in res['Up Rate']] 
    return res

def create_table_html(res):
    html_str_table = '''
    <table>
    <tr>
    '''
    for col in res.columns:
        html_str_table += '<th>{col}</th>'.format(col = col)
    html_str_table += '</tr>'

    for row in range(res.shape[0]):
        html_str_table += '<tr>'
        for col in res.columns:
            html_str_table += '<td>{data}</td>'.format(data = res.loc[row,col])
        html_str_table += '</tr>'
    html_str_table += '</table>'
    return html_str_table


#data_full, shape = 20, top = 104, left = 13):
def generate_HTML_CS_overview_new(data_full, shape = 20, top = 0, left = 8):

    with open(local_path + "pattern_type.json", 'r') as f:
        type_dict = json.load(f)  

    real_html = {}
    pattern_info_dict = {}
    pattern_det_dict = {}
    style = {}
    body = {}
    pattern_style = {} 
    pattern_body = {}
    for stock_name1 in data_full:
        try:
            stock_name = stock_name1.split('.')[0]
            iden = '.' + stock_name1.split('.')[1]
        except:
            stock_name = stock_name1
            iden = ''

        stock_name = stock_name.replace(iden, '')
        df = data_full[stock_name + iden].copy()
        real_html[stock_name] = generate_image(df, shape = 20, name = stock_name)
        pattern_info_dict.update(create_pattern_info_dict(df, name = stock_name))
        pattern_det_dict[stock_name] = create_pattern_det_dict(df)
        style[stock_name], body[stock_name] = html_interactive_candlestick(data = df ,top = top, left = left, shape = 20, name = stock_name)
        pattern_style[stock_name], pattern_body[stock_name] = pattern_detection(data = df,pat_dict = pattern_det_dict[stock_name], 
                                                                                top = top, left = left, name = stock_name)
        
    stock_name_list = [i.split('.')[0] for i in list(data_full.keys())]
    option_image = create_option_image(data = stock_name_list)
    full_style, full_overview_body = create_stacked(real_html, body, pattern_body, style, pattern_style)

    res = get_recap_table(data_full)


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
            overflow:auto;
            min-height:450;
            max-height:500px;
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
        left: 120%;
        overflow:auto;
        max-height:200px;
        width:155px;
        opacity:100%;
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

        ''' + full_style +'''

        </style>
        
</head>
<body>

<h2>Report</h2>

<div class="tab">
    <button class="tablinks" onclick="openreport(event, 'Overview')">Overview</button>
    <button class="tablinks" onclick="openreport(event, 'Top Gain')">Happening </button>
</div>

<div id="Overview" class="tabcontent" style="position:relative">

''' + option_image +'''

''' + full_overview_body +'''

<p style ="position:absolute;left:105px; top:8px;" min="1">Stock</p>
<p style ="position:absolute;left:480px; top:10px;" min="1">Time-Gap</p>
<input type="range" name="rangeInput" style ="position:absolute;left:550px; top:14px;width:135px;" min="1" max="10" value = "5" onchange="updateTextInput(this.value);">
<input type="text" id="textInput" value="5" size="1" style ="position:absolute;left:690px; top:14px;" >



</div>
<div id="Top Gain" class="tabcontent">
    <h3>Happening Pattern</h3>
''' + create_table_html(res) +'''
</div>


<p id = "demo"><p>

<script>

var acc_dicts = ''' + str(pattern_info_dict) + ''';
var type_dicts = ''' + str(type_dict) + ''';
var stock_name = ''' + str(stock_name_list) + ''';

changeimage(stock_name[0])
updateTextInput(5)

function updateTextInput(val) {
    document.getElementById('textInput').value=val;
    for (var key in acc_dicts) {
        var x = document.getElementsByClassName(key);
        var i;
        for (i = 0; i < x.length; i++) {
            if ((type_dicts[key.split(" ")[0]] == "BU RE")||(type_dicts[key.split(" ")[0]] == "BU CO")||(type_dicts[key.split(" ")[0]] == "I")){
                x[i].innerHTML = "<p style='color:green;font-size:20px;text-align:center;'>&#10138;<span style='color:black;font-size:15px;'>" 
                + acc_dicts[key][1][val-1] + "%</span></p>" +  (acc_dicts[key][0]*acc_dicts[key][1][val-1]/100).toFixed(0) + 
                " <span style='color:green;font-weight:10px'>Up</span> out of " + acc_dicts[key][0];
                }
            else{
                x[i].innerHTML = "<p style='color:red;font-size:20px;text-align:center;'>&#10136;<span style='color:black;font-size:15px;'>" 
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

function changeimage(val){
    for (i = 0; i < stock_name.length; i++){
        document.getElementById(stock_name[i]).style.display = "none";
    }
    document.getElementById(val).style.display = "block";
}
</script>
   
</body>
</html> 

'''