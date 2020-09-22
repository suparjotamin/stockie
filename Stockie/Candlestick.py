import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def is_pattern(pattern, ohlc, ohlc_h1, ohlc_h2):
    open = ohlc[0]
    high = ohlc[1]
    low = ohlc[2]
    close = ohlc[3]

    open_h1 = ohlc_h1[0]
    high_h1 = ohlc_h1[1]
    low_h1 = ohlc_h1[2]
    close_h1 = ohlc_h1[3]

    open_h2 = ohlc_h2[0]
    high_h2 = ohlc_h2[1]
    low_h2 = ohlc_h2[2]
    close_h2 = ohlc_h2[3]

    if pattern == 'doji':
        return (abs(close - open) / (high - low) < 0.05) & \
        (4*(high - np.maximum(close, open)) > (high - low)) & \
        (4*(np.minimum(close, open) - low) > (high - low)) & \
        (high > low)
    else:
        pass

    if pattern == 'gravestone_doji':
        return (abs(close - open) / (high - low) < 0.05) & \
        (5*(high - np.maximum(close, open)) > (high - low)) & \
        (5*(np.minimum(close, open) - low) < (high - low)) & \
        (high > low)
    else:
        pass

    if pattern == 'dragonfly_doji':
        return (abs(close - open) / (high - low) < 0.05) & \
        (5*(high - np.maximum(close, open)) < (high - low)) & \
        (5*(np.minimum(close, open) - low) > (high - low)) & \
        (high > low)
    else:
        pass

    if pattern == 'bullish_spinning_top':
        return (abs(close - open) / (high - low) > 0.1) & \
        (abs(close - open) / (high - low) < 0.2) & \
        (5*(high - np.maximum(close, open)) > (high - low)) & \
        (5*(np.minimum(close, open) - low) > (high - low)) & \
        (close > open)
    else:
        pass

    if pattern == 'bearish_spinning_top':
        return (abs(close - open) / (high - low) > 0.1) & \
        (abs(close - open) / (high - low) < 0.2) & \
        (5*(high - np.maximum(close, open)) > (high - low)) & \
        (5*(np.minimum(close, open) - low) > (high - low)) & \
        (close < open)
    else:
        pass

    if pattern == 'inverted_Hammer':
        return (abs(close - open) / (high - low) > 0.1) & \
        (abs(close - open) / (high - low) < 0.3) & \
        (5*(high - np.maximum(close, open)) > (high - low)) & \
        (10*(np.minimum(close, open) - low) < (high - low)) & \
        (close > open)
    else:
        pass

    if pattern == 'shootingstar':
        return (abs(close - open) / (high - low) > 0.1) & \
        (abs(close - open) / (high - low) < 0.3) & \
        (5*(high - np.maximum(close, open)) > (high - low)) & \
        (10*(np.minimum(close, open) - low) < (high - low)) & \
        (close < open)
    else:
        pass

    if pattern == 'hanging_man':
        return (abs(close - open) / (high - low) > 0.1) & \
        (abs(close - open) / (high - low) < 0.3) & \
        (10*(high - np.maximum(close, open)) < (high - low)) & \
        (5*(np.minimum(close, open) - low) > (high - low)) & \
        (close < open)
    else:
        pass

    if pattern == 'hammer':
        return (abs(close - open) / (high - low) > 0.1) & \
        (abs(close - open) / (high - low) < 0.3) & \
        (10*(high - np.maximum(close, open)) < (high - low)) & \
        (5*(np.minimum(close, open) - low) > (high - low)) & \
        (close > open)
    else:
        pass

    if pattern == 'bullish_marubozu': 
        return (abs(close - open) >= 0.95*(high - low))& \
        (close > open)
    else:
        pass

    if pattern == 'bearish_marubozu':
        return (abs(close - open) >= 0.95*(high - low))& \
        (close < open)
    else:
        pass

    if pattern == 'bullish_belt_hold':
        return (abs(close - open) >= 0.90*(high - low))& \
        (abs(open - low)*100 < (high - low) ) & \
        (high > close) & \
        (close > open)
    else:
        pass

    if pattern == 'bearish_belt_hold':
        return (abs(close - open) >= 0.90*(high - low))& \
        (abs(open - high)*100 < (high - low)) & \
        (low < close) & \
        (close < open)
    else:
        pass

# Double

    if pattern == 'bullish_engulfing':
        return (open_h1 > close_h1) & \
        (close > open) & \
        (open_h1 < close) & \
        (close_h1 > open) & \
        (high_h1 < high) & \
        (low_h1 > low)
    else:
        pass

    if pattern == 'bearish_engulfing':
        return (open_h1 < close_h1) & \
        (close < open) & \
        (open_h1 > close) & \
        (close_h1 < open) & \
        (high_h1 < high) & \
        (low_h1 > low)    
    else:
        pass

    if pattern == 'tweezer_top':
        return (open_h1 < close_h1) & \
        (close < open) & \
        (20*abs(high_h1 - high) < (high - low))
    else:
        pass

    if pattern == 'tweezer_bottom':
        return (open_h1 > close_h1) & \
        (close > open) & \
        (20*abs(low_h1 - low) < (high - low))
    else:
        pass

    if pattern == 'bullish_separating_line':
        return (open_h1 < open) & \
        (open_h1 > close_h1) & \
        (open < close)
    else:
        pass

    if pattern == 'bearish_separating_line':
        return (open_h1 > open) & \
        (open_h1 < close_h1) & \
        (open > close)
    else:
        pass

    if pattern == 'piercing_line':
        return (open_h1 > close_h1) & \
        (open < close) & \
        (close_h1 > open) & \
        (open_h1 > close) & \
        ((open_h1 - close_h1) < 2*(close - close_h1))
    else:
        pass

    if pattern == 'dark_cloud_cover':
        return (open_h1 < close_h1) & \
        (open > close) & \
        (close_h1 < open) & \
        (open_h1 < close) & \
        ((close_h1 - open_h1) < 2*(close_h1 - close))
    else:
        pass

    if pattern == 'mathing_high':
        return (open_h1 < close_h1) & \
        (close > open) & \
        (20*abs(high_h1 - high) < (high - low))
    else:
        pass

    if pattern == 'mathing_low':
        return (open_h1 > close_h1) & \
        (close < open) & \
        (20*abs(low_h1 - low) < (high - low))
    else:
        pass

    if pattern == 'bullish_harami':
        return (open_h1 > close_h1) &\
        (close > open) &\
        (open_h1 > close) &\
        (close_h1  < open) &\
        ((open_h1 - close_h1) > 4*(close - open))
    else:
        pass

    if pattern == 'bearish_harami':
        return (open_h1 < close_h1) &\
        (close < open) &\
        (open_h1 < close) &\
        (close_h1 > open) &\
        ((close_h1 - open_h1) > 4*(open - close))
    else:
        pass

    if pattern == 'bullish_harami_cross':
        return (open_h1 > close_h1) & \
        (open_h1 > close) & \
        (close_h1  < open) & \
        (abs(close - open) / (high - low) < 0.05) & \
        (4*(high - np.maximum(close, open)) > (high - low)) & \
        (4*(np.minimum(close, open) - low) > (high - low)) 
    else:
        pass

    if pattern == 'bearish_harami_cross':
        return (open_h1 < close_h1) & \
        (open_h1 < close) & \
        (close_h1  > open) & \
        (abs(close - open) / (high - low) < 0.05) & \
        (4*(high - np.maximum(close, open)) > (high - low)) & \
        (4*(np.minimum(close, open) - low) > (high - low))
    else:
        pass

    if pattern == 'descending_hawk':
        return (open_h1 < close_h1) & \
        (close > open) & \
        (open_h1 < open) & \
        (close_h1  > close) 
    else:
        pass

    if pattern == 'homing_pigeon':
        return (open_h1 > close_h1) & \
        (close < open) & \
        (open_h1 > open) & \
        (close_h1 < close) 
    else:
        pass


    if pattern == 'bullish_in_neck':
        return (open_h1 < close_h1) & \
        (close < open) & \
        (20*abs(close_h1 - close) < (high - low_h1)) 
    else:
        pass

    if pattern == 'bearish_in_neck':
        return (open_h1 > close_h1) & \
        (close > open) & \
        (20*abs(close_h1 - close) < (high_h1 - low)) 
    else:
        pass

    if pattern == 'bullish_on_neck':
        return (open_h1 < close_h1) & \
        (close < open) & \
        (20*abs(high_h1 - low) < (high - low_h1)) 
    else:
        pass

    if pattern == 'bearish_on_neck':
        return (open_h1 > close_h1) & \
        (close > open) & \
        (20*abs(low_h1 - high) < (high_h1 - low)) 
    else:
        pass

    if pattern == 'bullish_kicking':
        return (open_h1 > close_h1) & \
        (open < close) & \
        ((open_h1 - close_h1) > 0.9*(high_h1 - low_h1)) & \
        ((close_h1 - open_h1) > 0.9*(high - low)) & \
        (open_h1 < open)
    else:
        pass

    if pattern == 'bearish_kicking':
        return (open_h1 < close_h1) & \
        (open > close) & \
        ((close_h1 - open_h1) > 0.9*(high_h1 - low_h1)) & \
        ((open - close) > 0.9*(high - low)) & \
        (open_h1 > open)
    else:
        pass

#triple

    if pattern == 'morning_star':
        return (open_h2 > close_h2) &\
        (3*abs(close_h1 - open_h1) < abs(close_h2 - open_h2)) &\
        (3*abs(close_h1 - open_h1) < abs(close - open)) &\
        (np.maximum(open_h1, close_h1) < close_h2) &\
        (np.maximum(open_h1, close_h1) < open) &\
        (high_h1 > low_h1) &\
        (close > open)
    else:
        pass

    if pattern == 'evening_star':
        return (open_h2 < close_h2) &\
        (3*abs(close_h1 - open_h1) < abs(close_h2 - open_h2)) &\
        (3*abs(close_h1 - open_h1) < abs(close - open)) &\
        (np.minimum(open_h1, close_h1) > close_h2) &\
        (np.minimum(open_h1, close_h1) > open) &\
        (high_h1 > low_h1) &\
        (close < open)
    else:
        pass

    if pattern == 'morning_doji_star':
        return (open_h2 > close_h2) &\
        (abs(close_h1 - open_h1)/(high_h1 - low_h1) < 0.05) &\
        (np.minimum(open_h1, close_h1) < close_h2) &\
        (np.minimum(open_h1, close_h1) < open) &\
        (close > open)
    else:
        pass

    if pattern == 'evening_doji_star':
        return (open_h2 < close_h2) &\
        (abs(close_h1 - open_h1)/(high_h1 - low_h1) < 0.05) &\
        (np.minimum(open_h1, close_h1) > close_h2) &\
        (np.minimum(open_h1, close_h1) > open) &\
        (close < open)
    else:
        pass

    if pattern == 'three_white_soldier':
        return (open_h2 < close_h2) &\
        (2*abs(close_h2 - open_h2) > (high_h2 - low_h2)) &\
        (open_h1 < close_h1) &\
        (2*abs(close_h1 - open_h1) > (high_h1 - low_h1)) &\
        (open < close) &\
        (2*abs(close - open) > (high - low)) &\
        (0.5*(close_h2 + open_h2) < 0.5*(close_h1 + open_h1)) &\
        (0.5*(close_h1 + open_h1) < 0.5*(close + open)) &\
        (close_h1 > close_h2) &\
        (close > close_h1)
    else:
        pass

    if pattern == 'three_black_crow':
        return (open_h2 > close_h2) &\
        (2*abs(close_h2 - open_h2) > (high_h2 - low_h2)) &\
        (open_h1 > close_h1) &\
        (2*abs(close_h1 - open_h1) > (high_h1 - low_h1)) &\
        (open > close) &\
        (2*abs(close - open) > (high - low)) &\
        (0.5*(close_h2 + open_h2) > 0.5*(close_h1 + open_h1)) &\
        (0.5*(close_h1 + open_h1) > 0.5*(close + open)) &\
        (close_h1 < close_h2) &\
        (close < close_h1)
    else:
        pass

    if pattern == 'three_inside_up':
        return (open_h2 > close_h2) &\
        (open_h1 < close_h1) &\
        (open < close) &\
        (open_h1 < open) &\
        ((open + close) > (open_h1 + close_h1)) &\
        (open_h2 > close_h1) &\
        (close_h2 < open_h1)
    else:
        pass

    if pattern == 'three_inside_down':
        return (open_h2 < close_h2) &\
        (open_h1 > close_h1) &\
        (open > close) &\
        (open_h1 > open) &\
        ((open + close) < (open_h1 + close_h1))&\
        (close_h2 > open_h1) &\
        (open_h2 < close_h1)
    else:
        pass

    if pattern == 'deliberation':
        return (open_h2 < close_h2) &\
        (2*abs(close_h2 - open_h2) > (high_h2 - low_h2)) &\
        (open_h1 < close_h1) &\
        (2*abs(close_h1 - open_h1) > (high_h1 - low_h1)) &\
        (open < close) &\
        (3*abs(close - open) < abs(close_h1 - open_h1)) &\
        (0.5*(close_h2 + open_h2) < 0.5*(close_h1 + open_h1)) &\
        (0.5*(close_h1 + open_h1) < 0.5*(close + open)) &\
        (close_h1 > close_h2) &\
        (close > close_h1)
    else:
        pass

    if pattern == 'three_outside_up':
        return (open_h2 > close_h2) &\
        (open_h1 < close_h1) &\
        (open < close) &\
        (open_h1 < open) &\
        ((open + close) > (open_h1 + close_h1)) &\
        (open_h2 < close_h1) &\
        (close_h2 > open_h1)
    else:
        pass

    if pattern == 'three_outside_down':
        return (open_h2 < close_h2) &\
        (open_h1 > close_h1) &\
        (open > close) &\
        (open_h1 > open) &\
        ((open + close) < (open_h1 + close_h1))&\
        (close_h2 < open_h1) &\
        (open_h2 > close_h1)
    else:
        pass

    if pattern == 'bullish_abandoned_baby':
        return (open_h2 > close_h2) &\
        (3*abs(close_h1 - open_h1) < abs(close_h2 - open_h2)) &\
        (3*abs(close_h1 - open_h1) < abs(close - open)) &\
        (np.maximum(open_h1, close_h1) < close_h2) &\
        (np.maximum(open_h1, close_h1) < open) &\
        (high_h1 > low_h1) &\
        (high_h1 < low_h2) &\
        (high_h1 < low) &\
        (close > open)
    else:
        pass

    if pattern == 'bearish_abandoned_baby':
        return (open_h2 < close_h2) &\
        (3*abs(close_h1 - open_h1) < abs(close_h2 - open_h2)) &\
        (3*abs(close_h1 - open_h1) < abs(close - open)) &\
        (np.minimum(open_h1, close_h1) > close_h2) &\
        (np.minimum(open_h1, close_h1) > open) &\
        (high_h1 > low_h1) &\
        (low_h1 > high_h2) &\
        (low_h1 > high) &\
        (close < open)
    else:
        pass

    if pattern == 'bullish_stick_sandwich':
        return (open_h2 > close_h2) &\
        (open_h1 < close_h1) &\
        (open > close) &\
        (open_h1 > close_h2) &\
        (open_h2 < close_h1) &\
        (open > close_h1) &\
        (close < open_h1) &\
        (2*(open_h2 - close_h2) > (high_h2 - low_h2)) &\
        (2*(open - close) > (high - low)) &\
        (20*abs(close_h2 - close) < (high - np.minimum(low_h2,low)))
    else:
        pass

    if pattern == 'bearish_stick_sandwich':
        return (open_h2 < close_h2) &\
        (open_h1 > close_h1) &\
        (open < close) &\
        (open_h1 < close_h2) &\
        (open_h2 > close_h1) &\
        (open < close_h1) &\
        (close > open_h1) &\
        (2*(close_h2 - open_h2) > (high_h2 - low_h2)) &\
        (2*(close - open) > (high - low)) &\
        (20*abs(close_h2 - close) < (low - np.maximum(high_h2, high)))
    else:
        pass
         
    if pattern == 'bullish_side_by_side_white_line':
        return (open_h2 < close_h2) &\
        (open_h1 < close_h1) &\
        (open < close) &\
        (2*(close_h2 - open_h2) > (high_h2 - low_h2)) &\
        (2*(close_h1 - open_h1) > (high_h1 - low_h1)) &\
        (2*(close - open) > (high - low)) &\
        (open_h1 > close_h2) &\
        (20*abs(close_h1 - close) < (np.maximum(high, high_h1)-np.minimum(low, low_h1))) &\
        (20*abs(open_h1 - open) < (np.maximum(high, high_h1)-np.minimum(low, low_h1)))
    else:
        pass

    if pattern == 'bearish_side_by_side_black_line':
        return (open_h2 > close_h2) &\
        (open_h1 > close_h1) &\
        (open > close) &\
        (2*(open_h2 - close_h2) > (high_h2 - low_h2)) &\
        (2*(open_h1 - close_h1) > (high_h1 - low_h1)) &\
        (2*(open - close) > (high - low)) &\
        (open_h1 < close_h2) &\
        (20*abs(close_h1 - close) < (np.maximum(high, high_h1)-np.minimum(low, low_h1))) &\
        (20*abs(open_h1 - open) < (np.maximum(high, high_h1)-np.minimum(low, low_h1)))
    else:
        pass

    if pattern == 'bearish_side_by_side_white_line':
        return (open_h2 > close_h2) &\
        (open_h1 < close_h1) &\
        (open < close) &\
        (2*(open_h2 - close_h2) > (high_h2 - low_h2)) &\
        (2*(close_h1 - open_h1) > (high_h1 - low_h1)) &\
        (2*(close - open) > (high - low)) &\
        (close_h1 < close_h2) &\
        (20*abs(close_h1 - close) < (np.maximum(high, high_h1)-np.minimum(low, low_h1))) &\
        (20*abs(open_h1 - open) < (np.maximum(high, high_h1)-np.minimum(low, low_h1)))
    else:
        pass

    if pattern == 'bullish_side_by_side_black_line':
        return (open_h2 < close_h2) &\
        (open_h1 > close_h1) &\
        (open > close) &\
        (2*(close_h2 - open_h2) > (high_h2 - low_h2)) &\
        (2*(open_h1 - close_h1) > (high_h1 - low_h1)) &\
        (2*(open - close) > (high - low)) &\
        (close_h1 > close_h2) &\
        (20*abs(close_h1 - close) < (np.maximum(high, high_h1)-np.minimum(low, low_h1))) &\
        (20*abs(open_h1 - open) < (np.maximum(high, high_h1)-np.minimum(low, low_h1)))
    else:
        pass
         
    if pattern == 'upside_gap_three':
        return (open_h2 < close_h2) &\
        (open_h1 < close_h1) &\
        (open > close) &\
        (close_h2 < open_h1) &\
        (open > open_h1) &\
        (close < close_h2)
    else:
        pass

    if pattern == 'downside_gap_three':
        return (open_h2 > close_h2) &\
        (open_h1 > close_h1) &\
        (open < close) &\
        (close_h2 > open_h1) &\
        (open < open_h1) &\
        (close > close_h2)
    else:
        pass
         
    if pattern == 'upside_gap_two_crow':
        return (open_h2 < close_h2) &\
        (open_h1 > close_h1) &\
        (open > close) &\
        (open_h1 < open) &\
        (close_h1 > close) &\
        (close_h2 < close) 
    else:
        pass

    if pattern == 'unique_three_river_bottom':
        return (open_h2 > close_h2) &\
        (open_h1 > close_h1) &\
        (open < close) &\
        ((close_h1 - low_h1) > 2*(open_h1 - close_h1)) &\
        (close < close_h1)&\
        (open > low_h1)
    else:
        pass
         
    if pattern == 'bullish_tri_star':
        return (abs(close - open) / (high - low) < 0.05) & \
        (4*(high - np.maximum(close, open)) > (high - low)) & \
        (4*(np.minimum(close, open) - low) > (high - low)) & \
        (high > low)& \
        (abs(close_h1 - open_h1) / (high_h1 - low_h1) < 0.05) & \
        (4*(high_h1 - np.maximum(close_h1, open_h1)) > (high_h1 - low_h1)) & \
        (4*(np.minimum(close_h1, open_h1) - low_h1) > (high_h1 - low_h1)) & \
        (high_h1 > low_h1)& \
        (abs(close_h2 - open_h2) / (high_h2 - low_h2) < 0.05) & \
        (4*(high_h2 - np.maximum(close_h2, open_h2)) > (high_h2 - low_h2)) & \
        (4*(np.minimum(close_h2, open_h2) - low_h2) > (high_h2 - low_h2)) & \
        (high_h2 > low_h2) & \
        (close_h2 > close_h1) & \
        (close > close_h1)
    else:
        pass

    if pattern == 'bearish_tri_star':
        return (abs(close - open) / (high - low) < 0.05) & \
        (4*(high - np.maximum(close, open)) > (high - low)) & \
        (4*(np.minimum(close, open) - low) > (high - low)) & \
        (high > low)& \
        (abs(close_h1 - open_h1) / (high_h1 - low_h1) < 0.05) & \
        (4*(high_h1 - np.maximum(close_h1, open_h1)) > (high_h1 - low_h1)) & \
        (4*(np.minimum(close_h1, open_h1) - low_h1) > (high_h1 - low_h1)) & \
        (high_h1 > low_h1)& \
        (abs(close_h2 - open_h2) / (high_h2 - low_h2) < 0.05) & \
        (4*(high_h2 - np.maximum(close_h2, open_h2)) > (high_h2 - low_h2)) & \
        (4*(np.minimum(close_h2, open_h2) - low_h2) > (high_h2 - low_h2)) & \
        (high_h2 > low_h2) & \
        (close_h2 < close_h1) & \
        (close < close_h1)
    else:
        pass
         
    if pattern == 'three_star_in_the_north':
        return (close_h2 > open_h2) & \
        (close_h1 > open_h1) & \
        (close > open) & \
        (close_h2 - open_h2 > close_h1 - open_h1) & \
        (close_h1 - open_h1 > close - open) & \
        (close_h2 < close_h1) & \
        (close_h1 < close)
    else:
        pass
         
    if pattern == 'three_star_in_the_south':
        return (close_h2 < open_h2) & \
        (close_h1 < open_h1) & \
        (close < open) & \
        (close_h2 - open_h2 < close_h1 - open_h1) & \
        (close_h1 - open_h1 < close - open) & \
        (close_h2 > close_h1) & \
        (close_h1 > close)
    else:
        pass

