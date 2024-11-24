import random
import math
import numpy as np
import matplotlib
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
    sample_sred = total_elements / N

    math_exp = sum(key * (value / N) for key, value in frequency_table.items())
    disper = sum(((key - math_exp) ** 2) * (value / N) for key, value in frequency_table.items())

    sample_disper = np.var(sample, ddof=1)
    median = np.median(sample)
    range_val = max(sample) - min(sample)

    print("\nЧисловые характеристики:")

    print(f"Математическое ожидание (E[η]): {math_exp}")
    print(f"Выборочное среднее (x̄): {sample_sred}")
    res = math_exp - sample_sred
    print(f"|E[η] - x̄| : {abs(res)}")

    print(f"Дисперсия (D[η]): {disper}")
    print(f"Выборочная дисперсия (S²): {sample_disper}")
    res = disper - sample_disper
    print(f"|D[η] - S²| : {abs(res)}")
    
    print(f"Медиана (Me): {median}")
    print(f"Размах (R): {range_val}")


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

# Вычислить теоретические вероятности, отклонения и максимальное отклонение.
def compute_deviations(frequency_table, N, P):
    ter_ver = {}
    deviations = {}

    # Вычисляем теоретические вероятности
    for yj in frequency_table:
        ter_ver[yj] = (1 - P) ** (yj - 1) * P
    # relative_frequency - относительная частота
    # Вычисляем отклонения nj / n - P({η = yj})
    for yj, nj in frequency_table.items():
        relative_frequency = nj / N  # nj / n
        deviations[yj] = relative_frequency - ter_ver[yj]

    # Максимальное отклонение
    max_deviation = max(abs(dev) for dev in deviations.values())

    print("\nТаблица отклонений:")
    print("yj\t\tnj\t\tP({η = yj})\t\tnj/n\t\tОтклонение")
    for yj, nj in frequency_table.items():
        print(f"{yj}\t\t{nj}\t\t{ter_ver[yj]:.5f}\t\t{nj / N:.5f}\t\t{deviations[yj]:.5f}")

    print(f"\nМаксимальное отклонение: {max_deviation:.5f}")

# def third_part()

if __name__ == "__main__":
    frequency_table, total_elements, N, P = first_part()

    second_part(frequency_table, total_elements, N)
    compute_deviations(frequency_table, N, P)
    build_graphs_and_calculate_d(frequency_table, N, P)


