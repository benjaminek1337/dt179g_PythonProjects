# Project
## Environment & Tools / Utvecklingsmiljö & Verktyg
Windows 10 version 2004, PyCharm 2020.3.2, Python 3.9, Git version 2.29.2.windows.3
## Purpose / Syfte
Syftet med projektuppgiften är att applicera alla kursens läromål till ett större
projekt.

## Procedures / Genomförande
Inledningsvis studerade jag uppgiftens instruktioner, samt de medföljande filerna
code_base.py samt gol.py för att få en uppfattning om hur dessa hänger ihop.

Jag implementerade lösningarna i princip samma ordning som beskrevs i
projektbeskrivningen, hela vägen från att tolka -ws parametrarna till init pop,
till uppdatering av populationen och hela vägen från basimplementationen till
betyg A. 

Inga konstigheter, jag följde instruktionerna i uppgiftsbeskrivningen, samt
pseudokoden för att nå det slutgiltiga resultatet.

## Discussion / Diskussion
Pseudokoden var lätt att följa, och ibland kändes det nästan "fuskigt" då jag 
tyckte att de beskrev det tänkta kodflödet i princip rad för rad, och jag hade
inga problem med att tolka dessa, eller instruktionerna i övrigt.
Jag upplevde det alltid vara klart vad varje funktion var tänkt att genomföra, och
hur jag skulle gå tillväga för att skapa funktionen, nästan till den grad att det
var för enkelt.

MEN ett problem gäckade mig en stund, jag råkade göra fel redan i början, då
x och y värdena de inkluderade seedsen hade sina x och y värden flippade, 
och jag löste det till en början med att själv invertera x och y-parametrarna 
användaren får specificera till world_size.
Det resulterade dock i gol-mönster som ej motsvarade de specificerade under
exemplen på moodle. Därför fick jag tänka om, och istället invertera de inkomna
x och y värdena från seedsen, det resulterade i en korrekt lösning i förhållande
till exemplena i moodle.

Implementationerna av högre betygsgrader gick smidigt nog, JSON-parsingen var
lite lurig en sekund, i hur man skulle parsa string till tuple. Men jag fick det
att fungera både med literal_eval och tuple() parsing.

Solutionen innehåller varje betygssteg som en separat branch. Jag valde att göra
så mest på grund av att betyg D skrivs över helt och hållet. Den mest aktuella 
versionen finns dock i master-branchen.

Jag anser att min lösning är lämplig i förhållande till de specificerade kraven,
hela vägen upp till A-nivå.