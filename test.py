import numpy as np
from numpy.random import geometric
from scipy.stats import binom
import plotly.graph_objects as go
import numpy as np
from scipy.stats import geom
import pandas as pd
import matplotlib.pyplot as plt


# Ввод данных
N = int(input("Введите количество экспериментов N: "))
P = float(input("Введите вероятность генерации заданного числа P: "))

# Симуляция экспериментов
infected_counts = np.random.geometric(P, N)
infected_total = np.sum(infected_counts)

# Теоретические характеристики
E_eta = 1 / P  # Теоретическое математическое ожидание для геометрического распределения
D_eta = (1 - P) / (P ** 2)  # Теоретическая дисперсия

# Выборочные характеристики
sample_mean = np.mean(infected_counts)  # Выбоочное среднее
mean_diff = abs(E_eta - sample_mean)  # Отклонение среднего
sample_variance = np.var(infected_counts, ddof=0)  # Выборочная дисперсия
variance_diff = abs(D_eta - sample_variance)  # Разница дисперсий
median = np.median(infected_counts)  # Медиана

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

unique, counts = np.unique(infected_counts, return_counts=True)
frequency_table = pd.DataFrame({'Значение': unique, 'Частота': counts})

frequency_table['Теор вер'] = geom.pmf(frequency_table['Значение'], P)

# Отклонения между теоретической вероятностью и выборочной вероятностью
frequency_table['Выборочная вероятность'] = frequency_table['Частота'] / N
frequency_table['Отклонение'] = np.abs(frequency_table['Выборочная вероятность'] - frequency_table['Теор вер'])

print("\nТаблица частот с теоретическими вероятностями и отклонениями:")
print(frequency_table[['Значение', 'Частота', 'Теор вер', 'Выборочная вероятность', 'Отклонение']])

# Максимальное отклонение
max_deviation = frequency_table['Отклонение'].max()
print("\nМаксимальное отклонение:", max_deviation)

# Построение графиков
x_vals = np.arange(-1, 100)
F_theoretical = geom.cdf(x_vals, P)
F_empirical = [np.sum(infected_counts <= x + 1) / N for x in x_vals]

# Мера расхождения D
D = np.max(np.abs(np.array(F_theoretical) - np.array(F_empirical)))
print("Мера расхождения D:", D)

plt.figure(figsize=(12, 6))
plt.step(x_vals, F_theoretical, where="post", label="Теоретическая CDF")
plt.step(x_vals, F_empirical, where="post", label="Эмпирическая CDF", linestyle="--")
plt.xlabel("Количество чисел")
plt.ylabel("Функция распределения")
plt.title("Сравнение теоретической и эмпирической CDF")
plt.legend()
plt.grid()
plt.show()

# В данной задаче случайная величина, означающая количество искажённых сообщений, имеет биномиальное распределение
# Биномиальное распределение подходит здесь, так как:
# 1. Каждое сообщение может быть либо искажено, либо не искажено, что соответствует двум возможным исходам (искажено/не искажено) с фиксированной вероятностью искажения P.
# 2. Количество сообщений m фиксировано в каждом эксперименте.
# 3. Искажение каждого сообщения является независимым событием.