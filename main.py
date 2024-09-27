import matplotlib.pyplot as plt
from utils.utils import load_data
from technical_analysis.optimize import optimize
from technical_analysis.indicators import compute_indicators
from technical_analysis.backtest import backtest
import optuna

# Cargar el dataset de entrenamiento
train_data_path = r'C:\Users\52354\OneDrive\Documentos\TRADING\Proyecto2\data\aapl_5m_train.csv'

test_data_path = r'C:\Users\52354\OneDrive\Documentos\TRADING\Proyecto2\data\aapl_5m_test.csv'

# Cargar el dataset
test_data = load_data(test_data_path)
train_data = load_data(train_data_path).iloc[:20000,]

# Inicializar variables para guardar los mejores parámetros
best_sharpe_params = None
best_sharpe_value = -float('inf')
best_sharpe_combination = None

# Proceso de optimización para encontrar los mejores parámetros
for combination in range(1, 32):
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: optimize(trial, train_data, combination), n_trials=30)

    if study.best_value > best_sharpe_value:
        best_sharpe_value = study.best_value
        best_sharpe_params = study.best_params
        best_sharpe_combination = combination

print(f"Mejor Sharpe Ratio: {best_sharpe_value:.4f}")
print(f"Mejores parámetros para Sharpe Ratio: {best_sharpe_params}")
print(f"Mejor combinación de indicadores: {bin(best_sharpe_combination)}")

# Ejecutar el backtest final con los mejores parámetros
final_data = compute_indicators(train_data, best_sharpe_combination,
                                best_sharpe_params.get('BB_window', 0),
                                best_sharpe_params.get('SEWMA_window', 0),
                                best_sharpe_params.get('BEWMA_window', 0),
                                best_sharpe_params.get('rsi_window', 0),
                                best_sharpe_params.get('rsi_lower', 0),
                                best_sharpe_params.get('rsi_upper', 0),
                                best_sharpe_params.get('window_slow', 0),
                                best_sharpe_params.get('window_fast', 0),
                                best_sharpe_params.get('window_sign', 0),
                                best_sharpe_params.get('So_window', 0),
                                best_sharpe_params.get('So_smooth_window', 0),
                                best_sharpe_params.get('OSthreshold_low', 0),
                                best_sharpe_params.get('OSthreshold_high', 0))

# Ejecutar el backtest y obtener el valor del portafolio de la estrategia optimizada
sharpe, drawdown, win_loss, rend, porth = backtest(final_data,
                                                   best_sharpe_params['sl'],
                                                   best_sharpe_params['tp'],
                                                   best_sharpe_params['n_shares'],
                                                   rf=0.045 / 105120)

# Crear la gráfica de comparación
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(train_data['Close'], color='b', label='Inversión Pasiva (Precio Activo)')
ax1.set_ylabel('Precio Activo', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(porth, color='r', label='Portafolio Trading (Optimizado)')
ax2.set_ylabel('Valor del Portafolio', color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title('Comparación de Inversión Pasiva y Estrategia de Trading Optimizada')
fig.tight_layout()
plt.show()


# Ejecutar el backtest final con los mejores parámetros de Sharpe Ratio
final_data = compute_indicators(test_data, best_sharpe_combination,
                                best_sharpe_params.get('BB_window',0),
                                best_sharpe_params.get('SEWMA_window', 0),
                                best_sharpe_params.get('BEWMA_window', 0),
                                best_sharpe_params.get('rsi_window', 0),
                                best_sharpe_params.get('rsi_lower', 0),
                                best_sharpe_params.get('rsi_upper', 0),
                                best_sharpe_params.get('window_slow', 0),
                                best_sharpe_params.get('window_fast', 0),
                                best_sharpe_params.get('window_sign', 0),
                                best_sharpe_params.get('So_window', 0),
                                best_sharpe_params.get('So_smooth_window', 0),
                                best_sharpe_params.get('OSthreshold_low', 0),
                                best_sharpe_params.get('OSthreshold_high', 0))

# Ejecutar el backtest y obtener el valor del portafolio de la estrategia optimizada
sharpe, drawdown, win_loss, rend, porth = backtest(final_data,
                                                    best_sharpe_params['sl'],
                                                    best_sharpe_params['tp'],
                                                    best_sharpe_params['n_shares'],
                                                    rf=0.045 / 105120)

# Crear una Serie con el valor del portafolio (de la estrategia optimizada)

# Crear la gráfica
fig, ax1 = plt.subplots(figsize=(10, 6))

# Graficar la inversión pasiva (precios de cierre)
ax1.plot(test_data['Close'], color='b', label='Inversión Pasiva (Precio Activo)')
ax1.set_ylabel('Precio Activo', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Graficar el portafolio de la estrategia de trading optimizada en el mismo gráfico
ax2 = ax1.twinx()
ax2.plot(porth, color='r', label='Portafolio Trading (Optimizado)')
ax2.set_ylabel('Valor del Portafolio', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Títulos y leyendas
plt.title('Comparación de Inversión Pasiva y Estrategia de Trading Optimizada')
fig.tight_layout()

# Mostrar la gráfica
plt.show()