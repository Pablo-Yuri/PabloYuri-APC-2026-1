a, b = 17, 5

print(a / b)     # 3.4  — float! (C daria 3)
print(a // b)    # 3    — equivale ao / inteiro de C
print(a % b)     # 2

x = 3
x += 1           # x = 4 (religar para novo objeto int(4))
print(x)

maximo = a if a > b else b
print("max =", maximo)

# is vs ==
p = [1, 2]
q = [1, 2]
print(p == q)    # True  — mesmos valores
print(p is q)    # False — objetos distintos no heap