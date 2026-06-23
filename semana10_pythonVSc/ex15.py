def make_contador():
	n = 0                  # variável no escopo enclosing (persiste!)

	def contador():
		nonlocal n         # declara que n é do escopo enclosing (≡ static local)
		n += 1
		print(f"chamada número {n}")

	return contador

c = make_contador()
c()   # 1
c()   # 2
c()   # 3

contador = 0           # variável global

def incrementa():
	global contador    # sem isso, Python criaria local 'contador'
	contador += 1

incrementa()
incrementa()
incrementa()
print(contador)        # 3
