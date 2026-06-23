v = [10, 20, 30, 40, 50]

soma = 0
for x in v:
    soma += x
print("soma =", soma)   # 150
print("soma =", sum(v))    # 150 — função built-in

# aliasing (equivale a dois ponteiros C para o mesmo bloco)
a = [1, 2, 3]
b = a            # mesma lista!
b.append(99)
print(a)         # [1, 2, 3, 99]

# cópia rasa — objetos distintos
c = a.copy()     # ou a[:]
c.append(0)
print(a)         # [1, 2, 3, 99] — não afetado