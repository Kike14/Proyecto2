import optuna
from technical_analysis.backtest import backtest
from technical_analysis.indicators import compute_indicators

def optimize(trial, data, combination):
    data = data.copy()

    sl = trial.suggest_float("sl", 0.01, 0.15)
    tp = trial.suggest_float("tp", 0.01, 0.15)
    n_shares = trial.suggest_int("n_shares", 40, 150)

    # Default params
    BB_window = 0
    SEWMA_window = 0
    BEWMA_window = 0
    rsi_window = 0
    rsi_lower = 0
    rsi_upper = 0
    window_slow = 0
    window_fast = 0
    window_sign = 0
    So_window = 0
    So_smooth_window = 0
    OSthreshold_low = 0
    OSthreshold_high = 0

    if combination & 0b00001:
        BB_window = trial.suggest_int("BB_window", 10, 50)

    if combination & 0b00010:
        SEWMA_window = trial.suggest_int("SEWMA_window", 7, 14)
        BEWMA_window = trial.suggest_int("BEWMA_window", 15, 25)

    if combination & 0b00100:
        rsi_window = trial.suggest_int("rsi_window", 5, 50)
        rsi_lower = trial.suggest_int("rsi_lower", 10, 40)
        rsi_upper = trial.suggest_int("rsi_upper", 60, 90)

    if combination & 0b01000:
        window_slow = trial.suggest_int("window_slow", 13, 26)
        window_fast = trial.suggest_int("window_fast", 6, 12)
        window_sign = trial.suggest_int("window_sign", 1, 9)

    if combination & 0b10000:
        So_window = trial.suggest_int("So_window", 5, 50)
        So_smooth_window = trial.suggest_int("So_smooth_window", 5, 50)
        OSthreshold_low = trial.suggest_int("OSthreshold_low", 10, 40)
        OSthreshold_high = trial.suggest_int("OSthreshold_high", 60, 90)

    sharpe, draw, win_loss, rend, porth = backtest(compute_indicators(data, combination, BB_window, SEWMA_window,
                                       BEWMA_window, rsi_window, rsi_lower, rsi_upper,
                                       window_slow, window_fast, window_sign, So_window,
                                       So_smooth_window, OSthreshold_low, OSthreshold_high), sl, tp, n_shares, rf = 0.045 / 105120)

    print(f'Esta es la estrategia numero: {combination}')

    return sharpe