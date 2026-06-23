from enum import Enum

class DiaSemana(Enum):
	DOM=0; SEG=1; TER=2; QUA=3; QUI=4; SEX=5; SAB=6

def tipo_dia(d):
	match d:
		case DiaSemana.SAB | DiaSemana.DOM:
			return "Fim de semana"
		case _:
			return "Dia útil"

for d in DiaSemana:
	print(f"{d.name}: {tipo_dia(d)}")
