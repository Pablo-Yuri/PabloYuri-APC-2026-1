i    = 255
f    = 3.14159
c    = 'Z'
s    = "Brasilia"

print(f"Decimal:     {i}")
print(f"Hexadecimal: {i:x}")     # ff
print(f"Float 2dec:  {f:.2f}")
print(f"Char:        {c}")
print(f"String:      {s}")
print(f"Endereco:    {id(s)}")   # equivale a %p
print(f"Unicode ord: {ord(c)}")  # equivale ao valor ASCII do char
