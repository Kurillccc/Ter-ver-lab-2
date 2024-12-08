import random
import numpy as np
from scipy.stats import geom
import plotly.graph_objects as go
import pandas as pd

# Ввод данных
N = int(input("Введите количество запусков эксперимента (N): "))  # Количество экспериментов
P = float(input("Введите вероятность: "))  # Вероятность успеха

# Генерация выборки: количество попыток до первого успеха (геометрическое распределение)
attempts_until_success = np.random.geometric(P, N)

# total_elements = 0
# frequency_table = {}
#
# for _ in range(N):
#     count = 0
#
#     while True:
#         random_value = random.random()
#         count += 1
#         if random_value < P:
#             break
#
#     frequency_table[count] = frequency_table.get(count, 0) + 1
#     total_elements += count
#
# # Таблица частот
# print("\nТаблица частот значений количества чисел в последовательностях:")
# print("Значение\tNi\tЧастота")
# for key, value in frequency_table.items():
#     print(f"{key}\t\t{value}\t{value / N}")

# Теоретические характеристики
E_eta = 1 / P  # Теоретическое математическое ожидание для геометрического распределения
D_eta = (1 - P) / (P ** 2)  # Теоретическая дисперсия

# Выборочные характеристики
sample_mean = np.mean(attempts_until_success)  # Выборочное среднее
mean_diff = abs(E_eta - sample_mean)  # Отклонение среднего
sample_variance = np.var(attempts_until_success, ddof=0)  # Выборочная дисперсия
variance_diff = abs(D_eta - sample_variance)  # Разница дисперсий
median = np.median(attempts_until_success)  # Медиана

# Таблица характеристик
table = pd.DataFrame({
    'E(η)': [E_eta],
    'x̄': [sample_mean],
    '|E(η) - x̄|': [mean_diff],
    'D(η)': [D_eta],
    'S²': [sample_variance],
    '|D(η) - S²|': [variance_diff],
    'Me': [median]
})

print("\nТаблица характеристик:")
print(table)

# Таблица частот
unique, counts = np.unique(attempts_until_success, return_counts=True)
frequency_table = pd.DataFrame({'Количество попыток': unique, 'Частота': counts})
frequency_table['Теоретическая вероятность'] = geom.pmf(frequency_table['Количество попыток'], P)
frequency_table['Выборочная вероятность'] = frequency_table['Частота'] / N
frequency_table['Отклонение'] = abs(frequency_table['Выборочная вероятность'] - frequency_table['Теоретическая вероятность'])

print("\nЧастотная таблица:")
print(frequency_table[['Количество попыток', 'Частота', 'Теоретическая вероятность', 'Выборочная вероятность', 'Отклонение']])

# Максимальное отклонение
max_deviation = frequency_table['Отклонение'].max()
print("\nМаксимальное отклонение:", max_deviation)

# Мера расхождения D
x_vals = np.arange(1, max(attempts_until_success) + 2)
F_theoretical = geom.cdf(x_vals, P)
F_empirical = [np.sum(attempts_until_success <= x) / N for x in x_vals]
D = np.max(np.abs(np.array(F_theoretical) - np.array(F_empirical)))
print("Мера расхождения D:", D)

# Построение графиков
fig = go.Figure()

# Теоретическая функция распределения
fig.add_trace(go.Scatter(
    x=x_vals,
    y=F_theoretical,
    mode='lines',
    name='Теоретическая функция распределения',
    line=dict(color='blue'),
    line_shape='hv'
))

# Выборочная функция распределения
fig.add_trace(go.Scatter(
    x=x_vals,
    y=F_empirical,
    mode='lines',
    name='Выборочная функция распределения',
    line=dict(color='red', dash='dash'),
    line_shape='hv'
))

# Настройка графика
fig.update_layout(
    title="Функции распределения попыток до первого успеха",
    xaxis_title="Количество попыток",
    yaxis_title="F(x)",
    legend_title="Легенда",
    template="plotly_dark"
)

# Отображение графика
fig.show()
