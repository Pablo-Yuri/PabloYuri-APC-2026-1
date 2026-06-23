x = 42
print(type(x))      # <class 'int'>
print(id(x))        # endereço do objeto no heap (como %p em C)

x = "agora sou str" # reatribuição: x aponta para outro objeto
print(type(x))      # <class 'str'>

a = 1000
b = 1100
print(a == b)       # True  — mesmo valor
print(a is b)       # pode ser False — objetos diferentes no heap