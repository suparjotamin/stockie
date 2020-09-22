from .Candlestick import is_pattern
from .report import *
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

class stockie:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.data = yf.download(stock_name).reset_index()
        data = self.data
        for i in ['Open','High','Low','Close']:
            if i not in data.columns:
                break
                raise exception('{} is not in table\'s columns'.format(i))
            else:
                continue
        self.open = data['Open'].values
        self.high = data['High'].values
        self.low = data['Low'].values
        self.close = data['Close'].values   

        self.open_h1 = data['Open'].shift(1).values
        self.high_h1 = data['High'].shift(1).values
        self.low_h1 = data['Low'].shift(1).values
        self.close_h1 = data['Close'].shift(1).values  

        self.open_h2 = data['Open'].shift(2).values
        self.high_h2 = data['High'].shift(2).values
        self.low_h2 = data['Low'].shift(2).values
        self.close_h2 = data['Close'].shift(2).values  

        print('{} data loaded successfully'.format(stock_name))
        print(os.getcwd())

    def find_pattern(self, name ='all'):
        
        single_pattern = ['doji', 'gravestone_doji', 'dragonfly_doji', 'bullish_spinning_top', 'bearish_spinning_top',
                          'inverted_Hammer', 'shootingstar', 'hanging_man', 'hammer', 'bullish_marubozu', 'bearish_marubozu',
                          'bullish_belt_hold', 'bearish_belt_hold']
        double_pattern = ['bullish_engulfing', 'bearish_engulfing', 'tweezer_top', 'tweezer_bottom','bullish_separating_line',
                          'bullish_separating_line', 'piercing_line', 'dark_cloud_cover', 'matching_high', 'matching_low',
                          'bullish_harami', 'bearish_harami', 'bullish_harami_cross', 'bearish_harami_cross', 'descending_hawk',
                          'homing_pigeon', 'bullish_in_neck', 'bearish_in_neck', 'bullish_on_neck','bearish_on_neck','bullish_kicking',
                          'bearish_kicking']
        triple_pattern = ['morning_star', 'evening_star', 'morning_doji_star', 'evening_doji_star', 'three_white_soldier', 'three_black_crow',
                          'three_inside_up', 'three_inside_down', 'deliberation', 'three_outside_up', 'three_outside_down', 'bullish_abandoned_baby',
                          'bearish_abandoned_baby', 'bullish_stick_sandwich', 'bearish_stick_sandwich', 'bullish_side_by_side_white_line', 
                          'bearish_side_by_side_black_line', 'bearish_side_by_side_white_line', 'bullish_side_by_side_black_line',
                          'upside_gap_three', 'downside_gap_three', 'upside_gap_two_crow', 'unique_three_river_bottom', 'bullish_tri_star', 
                          'bearish_tri_star', 'three_star_in_the_north', 'three_star_in_the_south']

        
        if name == 'single':
            temp = self.data.copy()
            for i in single_pattern:
                temp[i] = is_pattern(i, [self.open, self.high, self.low, self.close],
                                     [self.open_h1, self.high_h1, self.low_h1, self.close_h1],
                                     [self.open_h2, self.high_h2, self.low_h2, self.close_h2])
                
        if name == 'double':
            temp = self.data.copy()
            for i in double_pattern:
                temp[i] = is_pattern(i, [self.open, self.high, self.low, self.close],
                                     [self.open_h1, self.high_h1, self.low_h1, self.close_h1],
                                     [self.open_h2, self.high_h2, self.low_h2, self.close_h2])
            return temp

        if name == 'triple':
            temp = self.data.copy()
            for i in triple_pattern:
                temp[i] = is_pattern(i, [self.open, self.high, self.low, self.close],
                                     [self.open_h1, self.high_h1, self.low_h1, self.close_h1],
                                     [self.open_h2, self.high_h2, self.low_h2, self.close_h2])
            return temp

        if name == 'all':
            temp = self.data.copy()
            for i in single_pattern + double_pattern + triple_pattern:
                temp[i] = is_pattern(i, [self.open, self.high, self.low, self.close],
                                     [self.open_h1, self.high_h1, self.low_h1, self.close_h1],
                                     [self.open_h2, self.high_h2, self.low_h2, self.close_h2])
            return temp

    def get_candlestick_report(self,shape=20):

        return display(HTML(generate_HTML_CS_overview(self.find_pattern(), shape= 20)))
