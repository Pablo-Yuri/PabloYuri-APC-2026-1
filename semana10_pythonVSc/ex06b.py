def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)


valor = input("Digite um número para calcular o fatorial: ")
print(fatorial(int(valor)))   # 120