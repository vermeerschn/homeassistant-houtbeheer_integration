# Houtbeheer voor Home Assistant

Een lokale Home Assistant custom integratie inclusief bijhorende Lovelace dashboardkaart om het droogproces en vochtpercentage van brandhout per houthok op te volgen.

## Functionaliteiten

- **Flexibel aantal houthokken**: instelbaar bij installatie en later aanpasbaar via het tandwiel in de integratie.
- **Uitgebreide houtsoorten**: Den, Eik, Beuk, Laurier, Kastanje, Es, Haagbeuk, Berk, Appel, Acacia, Esdoorn, Spar, Populier, Wilg en Anders.
- **Handmatige metingen met bevestiging**: stel het gemeten vochtpercentage in en klik op **Meting opslaan** om zowel de waarde als het exacte tijdstip vast te leggen.
- **Stookklaar-status**: automatische binary sensor die aangeeft of het hout onder 20% vocht zit.
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
1. Kopieer het bestand `www/houtbeheer-card.js` naar de map `/config/www/` in Home Assistant.
2. Ga naar **Instellingen → Dashboards → Drie puntjes rechtsboven → Bronnen** *(of via Instellingen > Dashboards > Bronnen indien Geavanceerde modus aan staat)*.
3. Voeg een nieuwe bron toe:
   - **URL**: `/local/houtbeheer-card.js`
   - **Type**: `JavaScript-module`
4. Vernieuw je browser (`Ctrl + F5`).

---

## Gebruik op het Dashboard

Voeg een handmatige kaart toe via de code-editor of gebruik de GUI-editor:

```yaml
type: custom:houtbeheer-card
title: Houtbeheer
read_only: false
```
