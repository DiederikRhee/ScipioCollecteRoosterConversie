# Broncode voor conversie van collecte rooster (excel bestand) naar csv bestanden t.b.v. Scipio app.

De conversie bestaat uit twee delen: 
1. Bepalen alle collectes per dag per wijkgemeente. Tussenresultaat wordt opgeslaan als excel bestand
2. Genereren van Scipio csv bestand. Hierbij zit de intelligentie hoelang een collecte moet doorlopen/zichtbaar zijn.

## Bepalen alle collectes per dag per wijkgemeente
Dit stuk code zet het excel bestand om naar een los bestand per wijk. De implementatie zal mogelijk elk jaar iets anders zijn i.v.m. kleine formaat wijzigingen in het collecte rooster. Belangrijke punten voor de conversie:
- K&E wordt volledig uitgeschreven: Kerk en Eredienst
- Doelen met de naam: Wel samenkomst, geen collecte, worden genegeerd
- Elk doel krijgt een prefix. Bijvoorbeeld: Col-1, Col-2, etc
- Er zijn alleen unieke collecte doelen per samenkomst dag
- Bij bijvoorbeeld een zondag met een cantatedienst in OH, zijn er twee 3e collectes (in cantatedienst is de cantatedienst het doel van de derde collecte)

## Genereren van Scipio csv bestanden per wijkgemeente
Dit stuk code maakt een Scipio csv bestand. Als input leest hij de excel in van alles collectes van deze wijkgemeente per dag. Belangrijke punten voor de conversie:
1. In principe begint de collecte twee dagen voor de dag van de viering (dus op vrijdagochtend 00.00 voor een viering op zondag)
2. In principe eindigt de collecte vier dagen na de dag van de viering (dus op donderdagavond 23.59 voor een viering op zondag)
3. Er worden altijd alleen maar de collectes weergegeven van 1 viering. Dus bij vieringen korter op elkaar dan 1 week, worden de bovenstaande start/eind tijden aangepast


## Hoe te gebruiken
1. Installeer uv (zie: https://docs.astral.sh/uv/getting-started/installation/)
2. Clone of download deze repo
3. Zet het collecterooster in de map: input
4. Draai main.py (uv run main.py)
5. Resultaten staan in output map
