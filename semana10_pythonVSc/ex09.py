import copy

# cópia rasa (shallow copy) — equivale a copiar array de ponteiros, não o conteúdo
original = [[1, 2], [3, 4]]
rasa = original.copy()
rasa[0].append(99)
print(original)    # [[1, 2, 99], [3, 4]] — sublista compartilhada!

# cópia profunda (deep copy) — equivale a duplicar toda a estrutura heap
original2 = [[1, 2], [3, 4]]
profunda = copy.deepcopy(original2)
profunda[0].append(99)
print(original2)   # [[1, 2], [3, 4]] — intacto
