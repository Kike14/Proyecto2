import ta
import pandas as pd



def compute_indicators(data: pd.DataFrame, combination: int, BB_window: int, SEWMA_window: int, BEWMA_window: int,
                       rsi_window: int,
                       rsi_lower: int, rsi_upper: int, window_slow: int, window_fast: int, window_sign: int,
                       So_window: int, So_smooth_window: int, OSthreshold_low: int,
                       OSthreshold_high: int) -> pd.DataFrame:
    trading_data = data.copy()

    ### lONGGGGGGGGGGGGG

    # Bollinger Bands
    if combination & 0b00001:
        bollinger = ta.volatility.BollingerBands(close=data.Close, window=BB_window)
        trading_data['BB_Buy'] = bollinger.bollinger_lband_indicator()

    # EWMA
    if combination & 0b00010:
        bewma = ta.trend.EMAIndicator(close=data.Close, window=BEWMA_window)
        sewma = ta.trend.EMAIndicator(close=data.Close, window=SEWMA_window)
        trading_data['EWMAH'] = bewma.ema_indicator()
        trading_data['EWMAL'] = sewma.ema_indicator()

        trading_data['EWMA_Buy'] = (trading_data['EWMAL'] > trading_data['EWMAH'])

        trading_data = trading_data.drop(['EWMAH', 'EWMAL'], axis=1)

    # RSI
    if combination & 0b00100:
        rsi = ta.momentum.RSIIndicator(close=data.Close, window=rsi_window)
        trading_data['RSI'] = rsi.rsi()
        trading_data['RSI_Buy'] = 0

        trading_data.loc[trading_data['RSI'] < rsi_lower, 'RSI_Buy'] = True

        trading_data = trading_data.drop(['RSI'], axis=1)

    # MACD
    if combination & 0b01000:
        macd = ta.trend.MACD(close=data.Close, window_slow=window_slow, window_fast=window_fast,
                             window_sign=window_sign)
        trading_data['MACD'] = macd.macd()
        trading_data['Signal_Line'] = macd.macd_signal()
        trading_data['MACD_Buy'] = 0

        trading_data.loc[(trading_data['MACD'] > trading_data['Signal_Line']) &
                         (trading_data['MACD'].shift(1) <= trading_data['Signal_Line'].shift(
                             1)), 'MACD_Buy'] = True

        trading_data = trading_data.drop(['MACD', 'Signal_Line'], axis=1)

    # Stochastic Oscillator

    if combination & 0b10000:
        stoch = ta.momentum.StochasticOscillator(high=data.High, low=data.Low, close=data.Close,
                                                 window=So_window, smooth_window=So_smooth_window)
        trading_data['%K'] = stoch.stoch()
        trading_data['%D'] = stoch.stoch_signal()
        trading_data['OS_Buy'] = 0

        trading_data.loc[(trading_data['%K'] < OSthreshold_low) & (
                trading_data['%K'] > trading_data['%D']), 'OS_Buy'] = True

        trading_data = trading_data.drop(['%K', '%D'], axis=1)

        ############ SHORTTTTTTTTTTTTTTTTTTTTTTTTTTT

        ## Bollinger

    if combination & 0b00001:
        bollinger = ta.volatility.BollingerBands(close=data.Close, window=BB_window)
        trading_data['BB_Sell'] = bollinger.bollinger_hband_indicator()

        # EWMA

    if combination & 0b00010:
        bewma = ta.trend.EMAIndicator(close=data.Close, window=BEWMA_window)
        sewma = ta.trend.EMAIndicator(close=data.Close, window=SEWMA_window)
        trading_data['EWMAH'] = bewma.ema_indicator()
        trading_data['EWMAL'] = sewma.ema_indicator()

        trading_data['EWMA_Sell'] = (trading_data['EWMAL'] < trading_data['EWMAH'])

        trading_data = trading_data.drop(['EWMAH', 'EWMAL'], axis=1)

        # RSI

    if combination & 0b00100:
        rsi = ta.momentum.RSIIndicator(close=data.Close, window=rsi_window)
        trading_data['RSI'] = rsi.rsi()
        trading_data['RSI_Sell'] = 0

        trading_data.loc[trading_data['RSI'] > rsi_upper, 'RSI_Sell'] = True

        trading_data = trading_data.drop(['RSI'], axis=1)

        # MACD

    if combination & 0b01000:
        macd = ta.trend.MACD(close=data.Close, window_slow=window_slow, window_fast=window_fast,
                             window_sign=window_sign)
        trading_data['MACD'] = macd.macd()
        trading_data['Signal_Line'] = macd.macd_signal()
        trading_data['MACD_Sell'] = 0

        trading_data.loc[(trading_data['MACD'] < trading_data['Signal_Line']) &
                         (trading_data['MACD'].shift(1) >= trading_data['Signal_Line'].shift(
                             1)), 'MACD_Sell'] = True

        trading_data = trading_data.drop(['MACD', 'Signal_Line'], axis=1)

    # Stochastic Oscillator

    if combination & 0b10000:
        stoch = ta.momentum.StochasticOscillator(high=data.High, low=data.Low, close=data.Close,
                                                 window=So_window, smooth_window=So_smooth_window)
        trading_data['%K'] = stoch.stoch()
        trading_data['%D'] = stoch.stoch_signal()
        trading_data['OS_Sell'] = 0

        trading_data.loc[(trading_data['%K'] > OSthreshold_high) & (
                trading_data['%K'] < trading_data['%D']), 'OS_Sell'] = True

        trading_data = trading_data.drop(['%K', '%D'], axis=1)

    return trading_data.dropna()