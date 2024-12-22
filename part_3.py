import math

from scipy.stats import chi2

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
    k, z_values = input_intervals()
    q_values = calculate_theoretical_probabilities(z_values, P)
    alpha = float(input("Введите уровень значимости α: "))

    print("\nТеоретические вероятности для интервалов:")
    for i, q in enumerate(q_values, start=1):
        print(f"q{i}: {q:.4f}")

    # Проверка гипотезы
    chi_square_test(frequency_table, k, z_values, q_values, N, alpha)