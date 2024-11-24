import random
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from scipy.stats import chi2

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


# третья часть
def input_intervals():
    """Ввод числа интервалов и их границ."""
    k = int(input("Введите число интервалов k: "))
    if k <= 1:
        print("Число интервалов должно быть больше 1.")
        exit(1)

    z_values = []
    print("Введите границы интервалов z1, z2, ..., zk-1 через пробел:")
    z_values = list(map(float, input().split()))

    if len(z_values) != k - 1:
        print("Ошибка: количество границ интервалов должно быть равно k - 1.")
        exit(1)

    return k, z_values


def calculate_theoretical_probabilities(z_values, P):
    """Вычисление теоретических вероятностей q1, q2, ..., qk."""
    q_values = []
    cumulative_prob = 0

    # Теоретическая вероятность для первого интервала (-∞, z1)
    q_values.append(1 - math.exp(-z_values[0] * P))

    # Для интервалов [z1, z2), [z2, z3), ...
    for i in range(1, len(z_values)):
        prob = math.exp(-z_values[i - 1] * P) - math.exp(-z_values[i] * P)
        q_values.append(prob)

    # Для последнего интервала [zk-1, ∞)
    q_values.append(math.exp(-z_values[-1] * P))

    return q_values


def chi_square_test(frequency_table, k, z_values, q_values, N, alpha):
    """Вычисление статистики критерия хи-квадрат и принятие гипотезы."""
    observed_counts = []
    z_intervals = [-math.inf] + z_values + [math.inf]

    # Сопоставление наблюдаемых данных интервалам
    for i in range(k):
        lower = z_intervals[i]
        upper = z_intervals[i + 1]
        count = sum(
            frequency_table[key] for key in frequency_table if lower <= key < upper
        )
        observed_counts.append(count)

    # Вычисление статистики хи-квадрат
    chi_square_stat = sum(
        (observed_counts[i] - N * q_values[i]) ** 2 / (N * q_values[i])
        for i in range(k)
        if q_values[i] > 0
    )

    # Вычисление критического значения
    critical_value = chi2.ppf(1 - alpha, df=k - 1)

    print("\nРезультаты проверки гипотезы:")
    print(f"Наблюдаемая статистика хи-квадрат: {chi_square_stat:.4f}")
    print(f"Критическое значение для уровня значимости {alpha}: {critical_value:.4f}")

    if chi_square_stat <= critical_value:
        print("Гипотеза H0 принимается: наблюдения соответствуют теоретическим вероятностям.")
    else:
        print("Гипотеза H0 отвергается: наблюдения не соответствуют теоретическим вероятностям.")


if __name__ == "__main__":
    frequency_table, total_elements, N, P = first_part()

    second_part(frequency_table, total_elements, N)
    compute_deviations(frequency_table, N, P)
    build_graphs_and_calculate_d(frequency_table, N, P)

    # Часть 3
    k, z_values = input_intervals()
    q_values = calculate_theoretical_probabilities(z_values, P)
    alpha = float(input("Введите уровень значимости α: "))

    print("\nТеоретические вероятности для интервалов:")
    for i, q in enumerate(q_values, start=1):
        print(f"q{i}: {q:.4f}")

    # Проверка гипотезы
    chi_square_test(frequency_table, k, z_values, q_values, N, alpha)