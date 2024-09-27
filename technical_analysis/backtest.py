class Position:
    def __init__(self, ticker, price, n_shares, timestamp):
        self.ticker = ticker
        self.price = price
        self.n_shares = n_shares
        self.timestamp = timestamp


def backtest(data: pd.DataFrame, sl: float, tp: float,
             n_shares: int, rf: float) -> float:
    data = data.copy()

    ind = data.iloc[:, 9:]

    len_ = int(len(ind.columns) / 2)
    data['allones_buy'] = (ind.iloc[:, :len_] == 1).all(axis=1)
    data['allones_sell'] = (ind.iloc[:, len_:] == 1).all(axis=1)

    # Margin requirements
    initial_margin = 1.28
    maintenance_margin = 1.25

    capital = 1_000_000
    margin_acc = 0
    COM = 0.125 / 100  # Commission percentage
    active_long_positions = []
    active_short_positions = []
    portfolio_value = [capital]
    equity = capital
    margin_calls = []
    nfm = []

    wins = 0  # Contador de operaciones ganadoras
    losses = 0  # Contador de operaciones perdedoras

    # Iterar sobre los datos del mercado
    for i, row in data.iterrows():
        long_signal = row.allones_buy  # Señal de compra
        short_signal = row.allones_sell  # Señal de venta

        # Entrada de posición larga
        if long_signal:
            cost = row.Close * n_shares * (1 + COM)
            if capital > cost and len(active_long_positions) < 100:
                capital -= row.Close * n_shares * (1 + COM)
                active_long_positions.append(
                    Position(ticker="APPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

        # Entrada de posición corta
        if short_signal:
            short_sell = row.Close * n_shares
            required_margin = short_sell * initial_margin
            if capital >= required_margin:
                capital -= short_sell * COM + required_margin
                margin_acc += required_margin
                active_short_positions.append(
                    Position(ticker="AAPL", price=row.Close, n_shares=n_shares, timestamp=row.Timestamp))

        # Cierre de posiciones largas
        for position in active_long_positions.copy():
            if row.Close > position.price * (1 + tp):
                capital += row.Close * position.n_shares * (1 - COM)
                wins += 1  # Operación ganadora
                active_long_positions.remove(position)
            elif row.Close < position.price * (1 - sl):
                capital += row.Close * position.n_shares * (1 - COM)
                losses += 1  # Operación perdedora
                active_long_positions.remove(position)

        # Cierre de posiciones cortas
        for position in active_short_positions.copy():
            if row.Close < position.price * (1 - tp):
                short_profit = (-row.Close * (1 + COM) + position.price) * n_shares
                capital += short_profit + margin_acc / len(active_short_positions)
                wins += 1  # Operación ganadora
                margin_acc -= margin_acc / len(active_short_positions)
                active_short_positions.remove(position)
            elif row.Close > position.price * (1 + sl):
                short_loss = (-row.Close * (1 + COM) + position.price) * n_shares
                capital += short_loss + margin_acc / len(active_short_positions)
                losses += 1  # Operación perdedora
                margin_acc -= margin_acc / len(active_short_positions)
                active_short_positions.remove(position)

        # Calcular el valor del portafolio
        long_value = sum([position.n_shares * row.Close for position in active_long_positions])
        short_value = sum([position.n_shares * (position.price - row.Close) for position in active_short_positions])
        short_value_margin = sum([position.n_shares * row.Close for position in active_short_positions])
        equity = capital + long_value - short_value
        portfolio_value.append(equity)

        # Check for margin call
        if margin_acc < (short_value_margin * maintenance_margin):
            short_close = active_short_positions[0].price - row.Close * (1 + COM)
            margin_calls.append(short_close)
            active_short_positions.pop(0)
            capital += short_close
        else:
            nfm.append(short_signal)