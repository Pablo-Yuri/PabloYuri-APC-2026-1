# imutável: int — comportamento parece "por valor" (como C)
def dobra_int(x):
    x *= 2       # x religar para novo int — original não muda
    print("dentro:", x)

v = 7
dobra_int(v)
print("fora:", v)   # ainda 7!

# mutável: lista — comportamento parece "por referência" (como ponteiro C)
def dobra_lista(lst):
    for i in range(len(lst)):
        lst[i] *= 2   # modifica o objeto existente

nums = [1, 2, 3]
dobra_lista(nums)
print(nums)   # [2, 4, 6] — alterado!