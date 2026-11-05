# Houtbeheer voor Home Assistant

Een lokale Home Assistant custom integratie inclusief bijhorende Lovelace dashboardkaart om het droogproces en vochtpercentage van brandhout per houthok op te volgen.

## Functionaliteiten

- **Flexibel aantal houthokken**: instelbaar bij installatie en later aanpasbaar via het tandwiel in de integratie.
- **Meerdere houtsoorten per hok**: kies uit een eigen lijst. Standaard: Den, Eik, Beuk, Laurier, Kastanje, Es, Haagbeuk, Berk, Appel, Acacia, Esdoorn, Spar, Populier, Wilg en Anders. De keuze wordt als lijst bewaard (attribuut `houtsoorten` van `sensor.houthok_N_houtsoorten`). Een leeg of net gereset hok staat op *Geen houtsoort*. Het vochtpercentage blijft per hok, niet per houtsoort.
- **Handmatige metingen met bevestiging**: stel het gemeten vochtpercentage in en klik op **Meting opslaan** om zowel de waarde als het exacte tijdstip vast te leggen.
- **Laatste 5 metingen per hok**: datum en percentage staan als lijst in het attribuut `metingen` van `sensor.houthok_N_opgeslagen_vochtgehalte`. De kaart toont ze als verloopgrafiek. Reset wist de geschiedenis.
- **Stookklaar-status**: automatische binary sensor die aangeeft of het hout onder 20% vocht zit.
- **Actief hok**: schakelaar per hok om aan te geven uit welk hok je hout mag nemen, los van het vochtpercentage. Meerdere hokken kunnen actief zijn.
- **Vuldatum**: per hok instelbaar, zonder tijdstip.
- **Reset**: knop die een hok leegmaakt (houtsoorten, invoer, meting, meetgeschiedenis, meetdatum, vuldatum en actief-status).
- **Hernoemen kan**: de kaart herkent de entiteiten aan vaste attributen, ook nadat je ze hernoemd hebt.
- **Eigen dashboardkaart**:
  - Duidelijk overzicht van alle hokken met houtsoort, actuele vochtigheid en stookstatus.
  - Snel schakelen tussen hokken en direct metingen doorvoeren.
  - GUI-instellingen om de titel aan te passen of de kaart in **Alleen-lezen** modus te zetten.

---

## Installatie

### 1. Integratie installeren
1. Kopieer de map `custom_components/houtbeheer` naar de map `/config/custom_components/` in je Home Assistant-omgeving.
2. Herstart Home Assistant volledig.
3. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**.
4. Zoek naar **Houtbeheer** en kies het aantal houthokken.

### 2. Dashboardkaart installeren
De kaart staat in een eigen repository: [homeassistant-houtbeheer_card](https://github.com/vermeerschn/homeassistant-houtbeheer_card). Daar vind je ook de installatie via HACS en alle kaartopties. Handmatig gaat het zo:

1. Download `houtbeheer-card.js` uit die repository en plaats het in de map `/config/www/` in Home Assistant.
2. Ga naar **Instellingen → Dashboards → Drie puntjes rechtsboven → Bronnen** *(of via Instellingen > Dashboards > Bronnen indien Geavanceerde modus aan staat)*.
3. Voeg een nieuwe bron toe:
   - **URL**: `/local/houtbeheer-card.js`
   - **Type**: `JavaScript-module`
4. Vernieuw je browser (`Ctrl + F5`).

---

## Houtsoorten instellen

Een Home Assistant-keuzelijst (`select`) kan maar één waarde bevatten. Daarom is de houtsoort een sensor met een lijst-attribuut, en stel je de keuze in via de actie `houtbeheer.set_wood_types`. De dashboardkaart doet dit voor je met aanvinkvakjes. Zelf aanroepen kan ook:

```yaml
action: houtbeheer.set_wood_types
data:
  shed: 1
  wood_types:
    - Eik
    - Beuk
```

Een lege lijst betekent *Geen houtsoort*. Dubbele waarden worden samengevoegd.

### De lijst met houtsoorten aanpassen
Ga naar **Instellingen → Apparaten & diensten → Houtbeheer → tandwiel** en pas het veld **Houtsoorten** aan. Typ een naam om een soort toe te voegen, of verwijder er een met het kruisje. De volgorde in het veld is de volgorde op de kaart.

- Een soort die nog in een hok zit, kan je niet verwijderen. Het scherm meldt in welke hokken ze zit; pas die eerst aan.
- Namen mogen maximaal 30 tekens zijn, zonder komma, en niet *Geen houtsoort*. Er kunnen maximaal 50 soorten in de lijst.
- Hernoemen kan niet rechtstreeks: voeg de nieuwe naam toe, zet de hokken om en verwijder daarna de oude.
- De actie `houtbeheer.set_wood_types` accepteert enkel soorten uit deze lijst.

### Upgraden van 1.4.1 of ouder
- `select.houthok_N_houtsoort` verdwijnt en wordt `sensor.houthok_N_houtsoorten`. Pas automatiseringen of dashboards aan die de oude entiteit gebruikten.
- Een bestaande enkele houtsoort wordt automatisch omgezet naar een lijst met één element. Die migratie is eenrichting.
- Werk de integratie en de dashboardkaart samen bij.

---

## Gebruik op het Dashboard

Voeg een handmatige kaart toe via de code-editor of gebruik de GUI-editor:

```yaml
type: custom:houtbeheer-card
title: Houtbeheer
read_only: false
```
