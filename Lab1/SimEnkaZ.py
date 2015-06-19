import sys

savUlaz = sys.stdin.readlines()
procitaniUlaz = []
for line in savUlaz:
	line = line.strip()
	if (len(line) > 0):
		procitaniUlaz.append(line)

ulazniNizovi = procitaniUlaz[0].split("|")
stanja = procitaniUlaz[1].split(",")
#stanja.append("#")
abeceda = procitaniUlaz[2].split(",")
#abeceda.append("$")
pocetnoStanje = procitaniUlaz[4].split(",")

def mapiraj(linije,stanja,abeceda):
	tablica = {}
	#for stanje in stanja:
	#	for znak in abeceda:
	#		tablica[(stanje,znak)] = "#"
	for linija in linije:
		linija = linija.split("->")
		arguments = linija[0].split(",")
		state = arguments[0]
		znak = arguments[1]

		if linija[1] != '#':
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
		trenutnaStanja = addEpsilon(tablica,pocetnoStanje)
		# modifikacija
		printBuffer = ','.join( trenutnaStanja )

		splitUlaz = ulaz.split(",")

		for znak in splitUlaz:
			#print( trenutnaStanja, '\n\t', printBuffer )
			novaStanja = []
			for state in trenutnaStanja:
				tempPrijelazi = tablica.get((state,znak),[])
				tempPrijelazi = addEpsilon(tablica,tempPrijelazi)
				for tempPrijelaz in tempPrijelazi:
					if((tempPrijelaz != "#") and (tempPrijelaz not in novaStanja)):
						novaStanja.append(tempPrijelaz)

			# modifikacija
			if novaStanja:
				printBuffer += '|' + ','.join( novaStanja )
			else:
				printBuffer += '|#'

			trenutnaStanja = novaStanja

		#print( trenutnaStanja, '\n\t', printBuffer )
		#print( ispis(printBuffer) )
		print( printBuffer )
		#print( '-'*20 )

	return

def ispis(buffer):
	odvojeniNizovi = buffer.split("|")
	gotovNiz  = ""
	for box in odvojeniNizovi:
		stanja = box.split(",")
		if((box == "") or (stanja == "")):
			gotovNiz+="#"
		else:
			sortirano = sorted(stanja)
			for stanje in stanja:
				gotovNiz+=stanje
				if(stanje != stanja[len(stanja)-1]):
					gotovNiz+=","
		if(box != odvojeniNizovi[len(odvojeniNizovi)-1]):
			gotovNiz+="|"

	return gotovNiz



tablica = mapiraj(procitaniUlaz[5:],stanja,abeceda)
magic(tablica,ulazniNizovi,pocetnoStanje)
