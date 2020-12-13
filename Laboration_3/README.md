# Laboration 3
## Environment & Tools / Utvecklingsmiljö & Verktyg
Windows 10 version 2004, PyCharm 2020.2.3, Python 3.9, Git version 2.28.0.windows.1
## Purpose / Syfte
Syftet med laborationen var att bland annat prova på att arbeta med rekursiva funktioner, 
dekoratorer(wrappers), filhantering och loggning. Samt att hålla koden välstrukturerad, 
där en funktion bör fylla ett syfte. 

## Procedures / Genomförande
### Steg 1: 
Granska programkoden, främst main, för att avgöra programmets flöde.

### Steg 2: 
Anpassa LOGGER genom att importera config från den bifogade json-filen. Samt modifiera 
den filen i enighet med uppgiftsbeskrivnignen.

### Steg 3: 
Skriva wrappern. Den tar emot en siffra att utgå från, och därför fick jag räkna ned från
den siffran, dvs loopa från nth_nmb till 0. Spara output från funktion, och logga varje resultat från 
nth_nmb jämnt delbart med 5. Mäta tidsåtgången från start till slut genom timer(), samt till sist
returnera en tuple med tidsåtgången och fibonaccisekvensen.
Vid det här laget klistrade jag in den den iterativa fibonacci-kalkylatorn till memory bara
för att få in korrekt data till resten av funktionerna. Memory-funktionen tog jag hand om 
sist.

### Steg 4: 
Skriva print_statistics funktionen. Skapa en nästlad lista över alla tidsåtgångar(använda
duration_format) för de olika fibonacci-funktionerna. Formatera och presentera den listan.

### Steg 5
Skriva write_to_file. Loopa igenom dicten, skapa filnamn baserat på nyckeln, öppna filen
och skriva till den. Innan dess - reversa talföljden så det stämmer övererns med förväntad
output.

### Steg 6
Skriva den där hemska fib_memory-funktionen.

## Discussion / Diskussion
Detta var lite mer av en utmaning. Filhantering i python var enkelt nog, och det var dessutom
tacksamt att en logger-config följde med. Wrapper-funktioner känner jag till visserligen, men
blev lite förvirrad över decoratorn en sekund. Gick dock någorlunda snabbt att nysta ut vad
den var till för.
Att formatera outputen i print_statistics var lite, inte nödvändigtvis svårt, men klurigt. Åtminstone
att få till en någorlunda clean lösning, istället för att rakt upp och ned skriva 12 st
table.data.append([duration_format(fib_details["fib recursion"][0], "Seconds"), osv osv osv.... ], ...
men jag tycker att jag fick till en godtagbar lösning.
Skriva till fil var inga konstigheter iaf.
Knepigast var att få till fib_memory. Googlade mig galen, hittade inga rekursiva funktioner med cache som
utgick från en omvänd fibonacci-sekvens så att säga, utan de utgick från en 1-n. Men de stod som inspiration
för att få till fib_memory-funktionen.
