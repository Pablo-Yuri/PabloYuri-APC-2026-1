# modulo.py — tudo no nível de módulo é executado na importação
print("executado sempre")

# guarda de entrada: executado só quando rodado diretamente
if __name__ == "__main__":
    print("ponto de entrada principal")