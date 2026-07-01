"""Exercicio 3.4 - Comparar contagens dos algoritmos de ordenacao."""

from pdad_utils import load_moradores, valid_age_mask


def bubble_sort_conta(lista):
    lst = lista[:]
    comparacoes = 0
    n = len(lst)
    for i in range(n):
        for j in range(n - i - 1):
            comparacoes += 1
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst, comparacoes


def selection_sort_conta(lista):
    lst = lista[:]
    comparacoes = 0
    n = len(lst)
    for i in range(n):
        idx_min = i
        for j in range(i + 1, n):
            comparacoes += 1
            if lst[j] < lst[idx_min]:
                idx_min = j
        lst[i], lst[idx_min] = lst[idx_min], lst[i]
    return lst, comparacoes


def insertion_sort_conta(lista):
    lst = lista[:]
    comparacoes = 0
    for i in range(1, len(lst)):
        chave = lst[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if lst[j] <= chave:
                break
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = chave
    return lst, comparacoes


def main():
    moradores = load_moradores()
    validos = moradores[valid_age_mask(moradores)]
    idades_base = validos["idade_calculada"].tolist()

    ordenada, c_bubble = bubble_sort_conta(idades_base)
    _, c_selection = selection_sort_conta(idades_base)
    _, c_insertion = insertion_sort_conta(idades_base)
    _, c_bubble_sorted = bubble_sort_conta(ordenada)
    _, c_selection_sorted = selection_sort_conta(ordenada)
    _, c_insertion_sorted = insertion_sort_conta(ordenada)
    _, c_bubble_reverse = bubble_sort_conta(list(reversed(ordenada)))
    _, c_selection_reverse = selection_sort_conta(list(reversed(ordenada)))
    _, c_insertion_reverse = insertion_sort_conta(list(reversed(ordenada)))

    n = len(idades_base)
    print(f"Ordenando {n} elementos (idades dos moradores):")
    print(f"  Bubble Sort:    {c_bubble} comparacoes")
    print(f"  Selection Sort: {c_selection} comparacoes")
    print(f"  Insertion Sort: {c_insertion} comparacoes")
    print(f"  Teorico O(n^2):  {n * n}  (n={n}, n^2={n}^2)")
    print()
    print("Lista ja ordenada:")
    print(f"  Bubble Sort:    {c_bubble_sorted} comparacoes")
    print(f"  Selection Sort: {c_selection_sorted} comparacoes")
    print(f"  Insertion Sort: {c_insertion_sorted} comparacoes")
    print()
    print("Lista em ordem inversa:")
    print(f"  Bubble Sort:    {c_bubble_reverse} comparacoes")
    print(f"  Selection Sort: {c_selection_reverse} comparacoes")
    print(f"  Insertion Sort: {c_insertion_reverse} comparacoes")


if __name__ == "__main__":
    main()
