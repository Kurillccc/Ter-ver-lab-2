import random, math
import numpy as np
import matplotlib.pyplot as plt

N = int(input("Введите количество экспериментов N: "))
p = float(input("Введите вероятность генерации заданного числа P: "))

i = 1
x = [] # количество использованных отливок для каждого эксперимента
y = []
ni = []
ver = []

while i <= N:
    t = 1
    a = random.uniform(0, 1)
    while a > p:
        t += 1
        a = random.uniform(0, 1)
    x.append(t)
    i += 1

print(f"yi\tni\tni/N")
j = 1
while j <= max(x):
    t = x.count(j)
    if t > 0:
        print(f"{j}\t{t}\t{t/N}")
        y.append(j)
        ni.append(t)
        ver.append(t/N)
    j += 1

x.sort()
X = sum(x) / len(x) # выборочное среднее
S = 0
for i in range(0, len(x)):
    S += pow(x[i] - X, 2)
S = S / len(x) # выборочная дисперсия
R = x[len(x) - 1] - x[0] # размах выборки
if len(x) % 2 == 0:
    Me = (x[math.ceil(len(x)/2) - 1] + x[math.ceil(len(x)/2)]) / 2 # выборочная медиана
else:
    Me = x[math.ceil(len(x)/2) - 1] # выборочная медиана

tries = [] # количество попыток
if p <= 0.2 and y[len(y) - 1] + 1 < 30:
    tries = np.arange(1, 30)
elif p <= 0.4 and y[len(y) - 1] + 1 < 20:
    tries = np.arange(1, 20)
elif p <= 0.6 and y[len(y) - 1] + 1 < 15:
    tries = np.arange(1, 15)
elif p <= 0.8 and y[len(y) - 1] + 1 < 10:
    tries = np.arange(1, 10)
elif p <= 1 and y[len(y) - 1] + 1 < 5:
    tries = np.arange(1, 5)
else: tries = np.arange(1, y[len(y) - 1] + 5)

Ft = 1 - (1 - p) ** tries # значения теор ф р при разных к

P = p * (1 - p)**(tries - 1) # значения теор вероятностей при разных х

En = 1/p # мат ожидание
Dn = (1 - p)/ (p**2) # дисперсия

print(f"\nEn = ", round(En, 10))
print(f"x^ = ", X)
print(f"|En - x^| = ", round(abs(En - X), 10))
print(f"Dn = ", round(Dn, 10))
print(f"S^2 = ", S)
print(f"|Dn - S^2| = ", round(abs(Dn - S), 10))
print(f"Me^ = ", Me)
print(f"R^ = ", R)

ii = 0
ver_max = 0
max_o = 0
print(f"\nyi\tP(n = yi)\tni/N")
for i in range(0, len(y)):
    q = P[y[i] - 1]
    ver_max += sum(P[:y[i]])
    if abs(ver_max - ver[i]) > max_o:
        max_o = abs(ver_max - ver[i])
        ii = i
    print(f"{y[i]}\t{round(q, 10)}\t{ver[i]}")

print("\nМаксимальное отклонение: ", round(max_o, 10), " при  yi = ", y[ii])


plt.figure(figsize=(10, 6))

# Построение теоретической ф р
F = [0, 0]
kk = [-1, tries[0]]
plt.plot(kk, F, color='b', label = 'теоретическая ф. р.')
for i in range(0, len(tries)):
    F = [Ft[i], Ft[i]]
    kk = [tries[i], tries[i] + 1]
    plt.plot(kk, F, color='b')

# Построение выборочной ф р
kk = [-1, y[0]]
F = [0, 0]
plt.plot(kk, F, color='g', label = 'выборочная ф. р.')
a = 0
for i in range(0, len(y)):
    a += ver[i]
    F = [a, a]
    if i == (len(y) - 1):
        kk = [y[i], y[i] + 1]
    else: kk = [y[i], y[i + 1]]
    plt.plot(kk, F, color='g')
plt.title('Функция распределения')
plt.xlabel('Количество попыток')
plt.ylabel('Вероятность')
plt.xticks(kk)  # Отображение всех значений на оси X
plt.xlim(0, tries[len(tries) - 1] + 1)
plt.ylim(0, 1.2)
plt.axhline(y=0, color='k', linestyle='--', linewidth=0.7)
plt.axvline(x=0, color='k', linestyle='--', linewidth=0.7)
plt.legend()
plt.grid()
plt.show()