import math

PI     = math.pi
R      = 5.0

area   = PI * R ** 2
print(f"Área do círculo r=5: {area:.2f}")

def quadrado(x):
	return x * x

print(f"quadrado(7+1) = {quadrado(7+1)}")   # 64 — sem armadilha de macro

# math.factorial() — equivale a implementar fatorial em C
print(f"10! = {math.factorial(10)}")
