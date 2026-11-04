# Houtbeheer

Een lokale Home Assistant-integratie voor houthokken. Per hok krijg je een keuzelijst voor de houtsoort, een veld **Eigen houtsoort**, een invoerveld **Nieuwe vochtmeting**, de knop **Meting opslaan**, een sensor voor het opgeslagen vochtgehalte en een tijdstempel voor de laatste meting.

## Installeren
1. Plaats `installeer_houtbeheer.sh` in de map `/config` van Home Assistant.
2. Open Terminal & SSH, Terminal add-on, of voer op de host uit: `bash /config/installeer_houtbeheer.sh`.
3. Herstart Home Assistant volledig.
4. Ga naar **Instellingen > Apparaten & diensten > Integratie toevoegen**, zoek **Houtbeheer** en kies het aantal hokken.
5. Om dit later te wijzigen: open de integratie en kies **Configureren**.

## Gebruik
Kies bij een hok de houtsoort in de keuzelijst. Beschikbaar: den, eik, beuk, laurier, kastanje, es, haagbeuk, berk, appel, acacia, esdoorn, spar, populier, wilg en anders. Er is geen apart tekstveld. Vul bij **Nieuwe vochtmeting** de waarde in en druk pas daarna op **Meting opslaan**. Die knop legt de vochtwaarde én datum/tijd vast. Een hok is stookklaar onder 20%.
