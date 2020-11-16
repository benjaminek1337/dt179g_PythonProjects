# Laboration 2
## Environment & Tools / Utvecklingsmiljö & Verktyg
Windows 10 version 2004, PyCharm 2020.2.3, Python 3.9, Git version 2.28.0.windows.1
## Purpose / Syfte
Syftet med laborationen är att behandla strängar, använda funktioner till att ta emot,
behandla och returnera värden, och att även validera dessa värden.
## Procedures / Genomförande
### Steg 1: 
Granska programkoden för att se förväntad funktionalitet genom pseudokod/förväntade 
utdata

### Steg 2: 
Modifiera funktionen authenticate_user till att splitta den inkommande strängen vid 
mellanslagen och skriva resultatet till en lista. 
Sedan skicka förnamn och efternamn f"{[0]} {[1]}" som inparametrar till funktion format_username,
samt skriva den output till user_tmp.
Samma process med lösenordet [2] till decrypt_password, och returnera till pass_tmp.

### Steg 3: 
Modifiera format_username. Splitta inkommande strängen vid mellanslaget.
Köra .capitalize() som tar emot ex "cHeVy" och returnerar "Chevy", på både [0] och [1],
sedan returnera f"{[0]}_{[1]}" som i fallet "chevy chase" returnerar "Chevy_Chase".

### Steg 4: 
Modifiera decrypt_password. Skriva en for-loop som utvärderar varje tecken i inparametern
password. Genom att vowels.find(password[i]) avgöra om ett tecken är en vokal. False ger värdet
-1. 
Avgöra om i % 2 = 0 för att bestämma om rot7 eller rot9 ska användas för att kryptera tecknet.
Slutligen använda de 2 parametrarna för att lägga till korrekt tecken till decrypted.
"lEeT" returnerar "s0N00l0]"

###Steg 5
I authenticate_user, jämföra username med user_tmp, och samma med password. Returnera det 
boolska värdet från jämförselsen för att avgöra om autenticeringen accepterats.

## Discussion / Diskussion
Att bolla värden in och ut från funktioner/metoder är en fundamental del av programmering.
Således har jag fått göra det rätt mycket tidigare i huvudsakligen C# och JavaScript. Inga
konstigheter. Inbyggda funktioner för att dela upp och formatera strängar är ej heller någon
större match att genomföra. 

Lösenordsdekrypteringen var en lite roligare utmaning. Inledningsvis många if-satser, gillar
inte riktigt det. Fick ned det till 4 rader kod innanför loopen genom ternary-operators.
Lite lurig uppgift, fick studera förväntad output mot förväntad input tills det dök upp ett "aha".

##### Fotnot: Vokalen Y saknas i vowels.