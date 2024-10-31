import tkinter as tk
from tkinter import ttk
import ccxt
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Функция для получения данных с биржи
def fetch_ohlcv(exchange_name, symbol, timeframe='1m', limit=100):
    if exchange_name == 'binance':
        exchange = ccxt.binance()
    elif exchange_name == 'bybit':
        exchange = ccxt.bybit()
    else:
        raise ValueError("Поддерживаются только 'binance' и 'bybit'")

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


# Функция для отображения графика
def plot_chart(df, chart_type='line', ax=None):
    ax.clear()  # Очистка графика перед перерисовкой
    if chart_type == 'line':
        ax.plot(df['timestamp'], df['close'], label='Цена закрытия')
        ax.set_title("Линейный график")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Цена")
        ax.legend()  # Добавляем легенду только для линейного графика
    elif chart_type == 'candlestick':
        mpf.plot(df.set_index('timestamp'), type='candle', style='charles', ax=ax)
    ax.figure.canvas.draw()  # Перерисовка графика


# Класс интерфейса приложения
class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Крипто Скринер")

        # Переменные для параметров
        self.exchange = tk.StringVar(value='binance')
        self.symbol = tk.StringVar(value='BTC/USDT')
        self.timeframe = tk.StringVar(value='1m')
        self.chart_type = tk.StringVar(value='line')

        # Настройка интерфейса
        self.setup_ui()

        # Запуск функции обновления графика
        self.update_chart()

    def setup_ui(self):
        # Элементы управления
        ttk.Label(self.root, text="Биржа:").grid(row=0, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.root, self.exchange, 'binance', 'binance', 'bybit').grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Пара:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.symbol).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Таймфрейм:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=self.timeframe).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Тип графика:").grid(row=3, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.root, self.chart_type, 'line', 'line', 'candlestick').grid(row=3, column=1, padx=5, pady=5)

        # Кнопка обновления
        ttk.Button(self.root, text="Обновить", command=self.update_chart).grid(row=4, column=0, columnspan=2, padx=5,
                                                                               pady=5)

        # Площадка для графика
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

    def update_chart(self):
        # Получение данных и обновление графика
        try:
            df = fetch_ohlcv(self.exchange.get(), self.symbol.get(), self.timeframe.get())
            plot_chart(df, self.chart_type.get(), self.ax)
        except Exception as e:
            print("Ошибка получения данных:", e)

        # Автоматическое обновление через 1 секунду
        self.root.after(1000, self.update_chart)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
