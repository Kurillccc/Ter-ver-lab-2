import random
import math
import numpy as np
import matplotlib.pyplot as plt

def first_part():
    # Ввод данных
    N = int(input("Введите кол-во экспериментов N: "))
    P = float(input("Введите вероятность генерации заданного числа P: "))
    print()

    # Проверка входных данных
    if N <= 0 or P < 0 or P > 1:
        print("Ошибка: Проверьте, что N >= 0, а P в пределах [0, 1]")
        exit(1)

    total_elements = 0
    frequency_table = {}

    for _ in range(N):
        count = 0

        while True:
            random_value = random.random()
            count += 1
            if random_value < P:
                break

        frequency_table[count] = frequency_table.get(count, 0) + 1
        total_elements += count

    # Среднее количество чисел
    avg_elements = total_elements / N
    print(f"Среднее кол-во чисел в последовательностях: {avg_elements}")

    # Таблица частот
    print("\nТаблица частот значений количества чисел в последовательностях:")
    print("Значение\tNi\tЧастота")
    for key, value in frequency_table.items():
        print(f"{key}\t\t{value}\t{value / N}")

    return frequency_table, total_elements, N, P


def second_part(frequency_table, total_elements, N):
    sample = [key for key, value in frequency_table.items() for _ in range(value)]
    sample_mean = total_elements / N

    theoretical_expectation = sum(key * (value / N) for key, value in frequency_table.items())
    theoretical_variance = sum(((key - theoretical_expectation) ** 2) * (value / N) for key, value in frequency_table.items())

    sample_variance = np.var(sample, ddof=1)
    median = np.median(sample)
    range_value = max(sample) - min(sample)

    print("\nЧисловые характеристики:")
    print(f"Теоретическое математическое ожидание (E[η]): {theoretical_expectation}")
    print(f"Теоретическая дисперсия (D[η]): {theoretical_variance}")
    print(f"Выборочное среднее (x̄): {sample_mean}")
    print(f"Выборочная дисперсия (S²): {sample_variance}")
    print(f"Медиана (Me): {median}")
    print(f"Размах (R): {range_value}")


def build_graphs_and_calculate_d(frequency_table, N, P):
    theoretical_cdf = {}
    empirical_cdf = {}

    # Теоретическая функция распределения
    cumulative_prob = 0.0
    for key in sorted(frequency_table.keys()):
        prob = (1 - P) ** (key - 1) * P
        cumulative_prob += prob
        theoretical_cdf[key] = cumulative_prob

    # Эмпирическая функция распределения
    cumulative_count = 0
    for key in sorted(frequency_table.keys()):
        cumulative_count += frequency_table[key]
        empirical_cdf[key] = cumulative_count / N

    # Построение графиков
    x = sorted(set(theoretical_cdf.keys()).union(empirical_cdf.keys()))
    theoretical_y = [theoretical_cdf.get(i, 0) for i in x]
    empirical_y = [empirical_cdf.get(i, 0) for i in x]

    plt.step(x, theoretical_y, where="post", label="Теоретическая CDF")
    plt.step(x, empirical_y, where="post", label="Эмпирическая CDF", linestyle="--")
    plt.xlabel("Количество чисел")
    plt.ylabel("Функция распределения")
    plt.title("Сравнение теоретической и эмпирической CDF")
    plt.legend()
    plt.grid()
    plt.show()

    # Вычисление меры расхождения D
    D = max(abs(theoretical_cdf.get(xi, 0) - empirical_cdf.get(xi, 0)) for xi in x)
    print(f"\nМера расхождения D: {D}")


if __name__ == "__main__":
    frequency_table, total_elements, N, P = first_part()
    second_part(frequency_table, total_elements, N)
    build_graphs_and_calculate_d(frequency_table, N, P)
