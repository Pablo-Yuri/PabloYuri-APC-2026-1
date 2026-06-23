for i in range(10):
    if i % 2 == 0:
        continue        # pula pares
    if i == 7:
        break           # para no 7
    print(i)
else:
    print("laço completo sem break")  # NÃO impresso (houve break)

# equivalente ao while de C com contador
n = 1
while (n < 32):
    print(n)
    n *= 2
