import numpy as np
from scipy.stats import binom, chi2
import pandas as pd
from scipy.stats import geom


# Ввод данных
N = int(input("Введите количество экспериментов N: "))
P = float(input("Введите вероятность P: "))

prinyat = 0
otklonit = 0

# Ввод уровня значимости
alpha = float(input("\nВведите уровень значимости α: "))

# Ввод интервалов
k = int(input("Введите количество интервалов k: "))
if k <= 1:
    print("Ошибка: Число интервалов должно быть больше 1.")
    exit(1)

z = []  # Список для границ интервалов
print(f"Введите границы интервалов z1, z2, ..., z{k - 1}:")
for i in range(1, k):
    # Ввод границ интервалов
    z_i = float(input(f"Введите z{i}: "))
    z.append(z_i)

# Добавляем "минус бесконечность" и "плюс бесконечность" к границам
intervals = [-np.inf] + z + [np.inf]

for o in range(100):
    # Симуляция экспериментов
    infected_counts = np.random.geometric(P, N)
    infected_total = np.sum(infected_counts)

    # Подсчёт частот попадания в интервалы
    interval_counts = np.histogram(infected_counts, bins=intervals)[0]
    interval_frequencies = interval_counts / N

    # Теоретические вероятности
    a_vals = np.arange(0, 1000)
    p_vals = geom.pmf(a_vals, P)

    q = []  # Список для теоретических вероятностей q_j
    for j in range(k):
        lower_bound = intervals[j]
        upper_bound = intervals[j + 1]
        q_j = np.sum(p_vals[(a_vals >= lower_bound) & (a_vals < upper_bound)])
        q.append(q_j)

    # Формируем таблицу интервалов
    interval_table = pd.DataFrame({
        'Интервал': [f"({intervals[i]}, {intervals[i + 1]})" for i in range(k)],
        'Частота n(j)': interval_counts,
        'Выборочная вероятность': interval_frequencies,
        'Теоретическая вероятность q(j)': q,
        'Ожидаемое n*q(j)': [N * q_j for q_j in q]})

    print("\nТаблица интервалов:")
    print(interval_table)

    # Вычисление статистики R0
    expected_counts = interval_table['Ожидаемое n*q(j)']
    R0 = np.sum((interval_counts - expected_counts) ** 2 / expected_counts)

    # Вычисление значения F отрицание для R0
    k_minus_1 = k - 1  # Степени свободы
    F_bar_R0 = 1 - chi2.cdf(R0, k_minus_1)

    # Пороговое значение F отрицание
    F_bar_critical = alpha

    # Решение о гипотезе H0
    hypothesis_decision = "Принять гипотезу H0" if F_bar_R0 >= F_bar_critical else "Отклонить гипотезу H0"

    if (hypothesis_decision == "Принять гипотезу H0"):
        prinyat += 1

    if (hypothesis_decision == "Отклонить гипотезу H0"):
        otklonit += 1

    # Вывод результатов
    print("\nРезультаты проверки гипотезы:")
    print(f"R0 = {R0:.5f}")
    print(f"F с отрицание(R0) = {F_bar_R0:.5f}")
    print(f"Пороговое значение F отрицание = α = {F_bar_critical:.5f}")
    print(f"Решение: {hypothesis_decision}")

print("\nСколько раз гипотеза была принята:")
print(prinyat)
print("\nСколько раз гипотеза была отклонена:")
print(otklonit)