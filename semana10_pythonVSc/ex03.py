a = [1, 2, 3]   # lista criada no heap; 'a' aponta para ela
b = a            # 'b' é outra etiqueta para o MESMO objeto
b.append(4)
print(a)         # [1, 2, 3, 4] — 'a' vê a mudança!

b = [9, 9]       # 'b' religar para nova lista; 'a' não muda
print(a)         # [1, 2, 3, 4]
print(b)         # [9, 9]