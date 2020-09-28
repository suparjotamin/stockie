# from Stockie.stockie import stockie
from .Candlestick import is_pattern
from .report import *
# from Stockie.stockie import stockie
import yfinance as yf
from IPython.core.display import display, HTML, clear_output
import pandas as pd
from mpl_finance import candlestick2_ochl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
import os

import matplotlib.pyplot as plt
import base64
from io import BytesIO


class stockie:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.data = {}

        for stock in self.stock_name:
            self.data[stock] = yf.download(stock).reset_index()
        clear_output()

        print('{} data loaded successfully'.format(stock_name))

        self.additional_pattern = {}

        self.single_pattern = ['doji', 'gravestone_doji', 'dragonfly_doji', 'bullish_spinning_top', 'bearish_spinning_top',
                          'inverted_Hammer', 'shootingstar', 'hanging_man', 'hammer', 'bullish_marubozu', 'bearish_marubozu',
                          'bullish_belt_hold', 'bearish_belt_hold']
        self.double_pattern = ['bullish_engulfing', 'bearish_engulfing', 'tweezer_top', 'tweezer_bottom','bullish_separating_line',
                          'bullish_separating_line', 'piercing_line', 'dark_cloud_cover', 'matching_high', 'matching_low',
                          'bullish_harami', 'bearish_harami', 'bullish_harami_cross', 'bearish_harami_cross', 'descending_hawk',
                          'homing_pigeon', 'bullish_in_neck', 'bearish_in_neck', 'bullish_on_neck','bearish_on_neck','bullish_kicking',
                          'bearish_kicking']
        self.triple_pattern = ['morning_star', 'evening_star', 'morning_doji_star', 'evening_doji_star', 'three_white_soldier', 'three_black_crow',
                          'three_inside_up', 'three_inside_down', 'deliberation', 'three_outside_up', 'three_outside_down', 'bullish_abandoned_baby',
                          'bearish_abandoned_baby', 'bullish_stick_sandwich', 'bearish_stick_sandwich', 'bullish_side_by_side_white_line', 
                          'bearish_side_by_side_black_line', 'bearish_side_by_side_white_line', 'bullish_side_by_side_black_line',
                          'upside_gap_three', 'downside_gap_three', 'upside_gap_two_crow', 'unique_three_river_bottom', 'bullish_tri_star', 
                          'bearish_tri_star', 'three_star_in_the_north', 'three_star_in_the_south']

        self.pattern = self.single_pattern + self.double_pattern + self.triple_pattern

    def add_pattern(self, name, function, type = 'I'):
        if (name not in self.pattern)|(name not in self.additional_pattern):
            self.additional_pattern[name] = function
        else:
            print('pattern name has been taken, try another one')

    def find_pattern(self, name ='all'):
        all_pattern_data = {}

        for data_key in self.data:
            data = self.data[data_key]

            open = data['Open'].values
            high = data['High'].values
            low = data['Low'].values
            close = data['Close'].values   

            open_h1 = data['Open'].shift(1).values
            high_h1 = data['High'].shift(1).values
            low_h1 = data['Low'].shift(1).values
            close_h1 = data['Close'].shift(1).values  

            open_h2 = data['Open'].shift(2).values
            high_h2 = data['High'].shift(2).values
            low_h2 = data['Low'].shift(2).values
            close_h2 = data['Close'].shift(2).values  
        

            if name == 'all':
                temp = data.copy()
                for i in self.pattern:
                    temp[i] = is_pattern(i, [open, high, low, close],
                                        [open_h1, high_h1, low_h1, close_h1],
                                        [open_h2, high_h2, low_h2, close_h2])
                for i in self.additional_pattern:
                    temp[i] = self.additional_pattern[i]()

            all_pattern_data[data_key] = temp
        return all_pattern_data

    def get_candlestick_report(self,shape=20, create_HTML_file = False, location = ''):
        clear_output()
        html_str = generate_HTML_CS_overview_new(self.find_pattern(), shape= 20)
        if create_HTML_file:
            with open(location, 'w') as f:
                f.write(html_str)
        return display(HTML(html_str))
