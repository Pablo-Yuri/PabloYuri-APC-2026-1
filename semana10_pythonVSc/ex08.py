 s = "Brasilia"
print(f"Comprimento: {len(s)}")

for i, c in enumerate(s):
	print(f"s[{i}] = '{c}'  (ord={ord(c)})")   # ord() ≡ valor ASCII

# comparação — equivale a strcmp
t = "Brasilia"
print(s == t)        # True
print(s is t)        # pode ser True (interning) ou False

# tentativa de mutação
try:
	s[0] = 'b'       # TypeError!
except TypeError as e:
	print("Erro:", e)
