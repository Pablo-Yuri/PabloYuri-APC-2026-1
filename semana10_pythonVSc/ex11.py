class Complexo:
	def __init__(self, re, im):
		self.re = re
		self.im = im

	def modulo_sq(self):       # equivale a função que recebe struct* em C
		return self.re**2 + self.im**2

	def __repr__(self):
		return f"{self.re} + {self.im}i"

c1 = Complexo(3.0, 4.0)
c2 = c1              # c2 é outra referência para o MESMO objeto
c2.re = 0.0
print(c1)            # 0.0 + 4.0i — c1 vê a mudança (mesma semântica de pp->re=0)
print(c1.modulo_sq())
