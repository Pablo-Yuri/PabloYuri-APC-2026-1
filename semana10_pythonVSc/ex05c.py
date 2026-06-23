dia = 3   # 1=Seg ... 7=Dom

match dia:
    case 1 | 2 | 3 | 4 | 5:
        print("Dia útil")
    case 6 | 7:
        print("Fim de semana")
    case _:
        print("Inválido")