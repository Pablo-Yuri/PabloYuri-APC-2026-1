# tuple como array imutável (equivale a const int v[] em C)
PRIMOS = (2, 3, 5, 7, 11, 13)
print(PRIMOS[0])

try:
	PRIMOS[0] = 99    # TypeError — imutável
except TypeError as e:
	print("Imutável:", e)

# iteração segura sobre arquivo (sem fopen/fclose explícito)
# (PythonTutor não suporta I/O de arquivo — simulamos com lista)
linhas = ["linha 1\n", "linha 2\n", "linha 3\n"]
for linha in linhas:
	print(linha.strip())
