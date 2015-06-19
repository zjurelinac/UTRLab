import sys

savUlaz = sys.stdin.readlines()
procitaniUlaz = []
for line in savUlaz:
	line = line.strip() 
	if (len(line) > 0):
		procitaniUlaz.append(line)

ulazniNizovi = procitaniUlaz[0].split("|")
stanja = procitaniUlaz[1].split(",")
stanja.append("#")
abeceda = procitaniUlaz[2].split(",")
abeceda.append("$")
pocetnoStanje = procitaniUlaz[4].split(",")

def mapiraj(linije,stanja,abeceda):
	tablica = {}
	for stanje in stanja:
		for znak in abeceda:
			tablica[(stanje,znak)] = "#"
	for linija in linije:
		linija = linija.split("->")
		arguments = linija[0].split(",")
		state = arguments[0]
		znak = arguments[1]
		novaStanja = linija[1].split(",")
		tablica[(state,znak)] = novaStanja
	return tablica

def addEpsilon(tablica,trenutnaStanja):
	tempStanja = []
	biloEpsilona = True
	for stanje in trenutnaStanja:
		tempStanja.append(stanje)

	while(biloEpsilona):
		biloEpsilona = False
		stanje = []
		for stanje in trenutnaStanja:
				prijelazi = tablica.get((stanje,"$"),[])
				for prijelaz in prijelazi:
					if( prijelaz != "#"):
						if (prijelaz not in tempStanja):
							biloEpsilona = True
							tempStanja.append(prijelaz)
		trenutnaStanja = []
		for state in tempStanja:
			if(state not in trenutnaStanja):
				trenutnaStanja.append(state)
	return sorted(tempStanja)

def magic(tablica,ulazniNizovi,pocetnoStanje):
	for ulaz in ulazniNizovi:
		printBuffer = ""
		trenutnaStanja = []
		pocetnaStanja = addEpsilon(tablica,pocetnoStanje)

		for stanje in pocetnaStanja:		
			trenutnaStanja.append(stanje)
			printBuffer+=stanje
			printBuffer+=","

		printBuffer+="|"
		splitUlaz = ulaz.split(",")
		
		for znak in splitUlaz:
			novaStanja = []
			for state in trenutnaStanja:
				tempPrijelazi = tablica.get((state,znak),[])
				tempPrijelazi = addEpsilon(tablica,tempPrijelazi)
				for tempPrijelaz in tempPrijelazi:
					if((tempPrijelaz != "#") and (tempPrijelaz not in novaStanja)):
						novaStanja.append(tempPrijelaz)
			
			for new in novaStanja:
				if(new != "#"):
					printBuffer+=new
					printBuffer+=","
			
			trenutnaStanja = novaStanja
			printBuffer+="|"
		print ispis(printBuffer)

	return

def ispis(buffer):
	odvojeniNizovi = buffer.split("|")
	gotovNiz  = ""
	brojac = 1
	duljina = len(odvojeniNizovi)
	for box in odvojeniNizovi:
		if((box == "")):
			gotovNiz+="#"
		else:
			stanja = box.split(",")
			sortirano = sorted(stanja)
			length = len(stanja)
			i=1
			for stanje in sortirano:
				gotovNiz+=stanje
				if((i < length) and (i!=1)):
					gotovNiz+=","
				i+=1
		if(brojac < duljina-1):
			gotovNiz+="|"
		brojac+=1
		if(brojac == duljina):
			break
	return gotovNiz



tablica = mapiraj(procitaniUlaz[5:],stanja,abeceda)
magic(tablica,ulazniNizovi,pocetnoStanje)