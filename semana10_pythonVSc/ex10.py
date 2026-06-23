a = [10, 20, 30]
b = a              # contagem de referências de [10,20,30] = 2
print(id(a), id(b))

b = None           # contagem cai para 1; objeto ainda vivo
print(a)           # [10, 20, 30]

a = None           # contagem cai para 0; GC pode coletar
# objeto [10,20,30] não é mais acessível

c = [1, 2]
del c              # equivale a c = None + remove nome do escopo
