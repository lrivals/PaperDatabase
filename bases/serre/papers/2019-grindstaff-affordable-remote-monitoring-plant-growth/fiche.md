---
id: 2019-grindstaff-affordable-remote-monitoring-plant-growth
fiche: done
date: 2026-11-03
benchmarks: none
---

# Affordable remote monitoring of plant growth in facilities using Raspberry Pi computers

Brandin Grindstaff, Makenzie E Mabry, Paul D Blischak, Micheal Quinn, J Chris Pires, Applications in Plant Sciences 7(8), e11280, 2019. https://doi.org/10.1002/aps3.11280
Type : article de revue (journal), de type protocole / note méthodologique (Methods and Results + 3 appendices d'installation).

## Problème

Les paramètres d'une chambre de culture fluctuent et nuisent à la reproductibilité des expériences ; la meilleure parade est de les mesurer et de les enregistrer (Introduction). Les solutions commerciales (Argus) coûtent de 10 000 à plus de 1 000 000 USD (Methods, « Raspberry Pi and peripheries »). Les auteurs veulent un système de surveillance abordable, ouvert, utilisable par des chercheurs peu familiers du génie logiciel.

## Méthode

Growth Monitor pi (GMpi) : un Raspberry Pi avec un capteur température/humidité DHT22, un capteur de lumière TSL2591 (lux, visible et infrarouge, plage 0,000118 à 88 000 lux) et une caméra CSI-2 (Methods). Le logiciel GMPi_Pack (7 scripts Python/shell) lit les capteurs, prend des photos et envoie données et images vers un cloud (Google Drive via Rclone), le tout planifié par cron (exemple : lecture toutes les 2 minutes, Appendix 3). Des alertes sont envoyées sur Slack par webhook quand température, humidité ou lumière sortent des plages fixées dans `config.txt` (Methods, « Remote monitoring »). Les seuils sont fixes (règles), sans modèle ni apprentissage.

## Plateforme et implémentation

- Plateforme : Raspberry Pi « Model B+ » (sous-modèle exact n/r), Raspbian Stretch 4.14.50-v7+ (Methods). Pas de NPU, pas d'inférence.
- Puissance : n/r. Fréquence, mémoire : n/r.
- Coût : environ 200 USD (Methods).
- Code : publié sous GPL v3, https://github.com/BrandinGrindstaff/GMpi (Methods, « GMpi software dependencies »). Dépendances : Adafruit_DHT, python-tsl2591, Rclone.
- Mise à l'échelle : plusieurs Pi avec identifiants uniques écrivant dans un dossier cloud commun (Protocol feasibility) ; non testée.

## Résultats

Aucun résultat quantitatif de performance. Seuls chiffres : coût d'environ 200 USD contre 10 000 à plus de 1 000 000 USD pour Argus (Methods) ; Fig. 3 montre environ un mois de données (lumière, température, humidité en boîtes à moustaches) sans valeur numérique lisible dans le texte. La précision du DHT22 a été « déterminée » par comparaison au thermostat et à l'hygromètre analogique de la chambre (Methods), mais aucune valeur n'est rapportée (n/r).
→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`) ; le papier ne rapporte aucune métrique de performance (précision, FPS, latence, puissance) ni de comparaison mesurée, seulement un coût.

## Limites et critique

- Pas de validation : précision des capteurs, fiabilité des alertes, taux de fausses alertes, durée de fonctionnement ne sont pas quantifiés.
- Étalonnage du DHT22 contre un thermostat et un hygromètre analogiques de la chambre, eux-mêmes peu précis ; résultat non chiffré.
- Lumière en lux, et non en PAR : inadapté à la mesure d'un DLI ou d'une photosynthèse (les auteurs le justifient par le suivi de l'usure des tubes fluorescents).
- Surveillance seule : aucun actionneur ni boucle de commande. Pas de CO₂, pH, EC, ni humidité du substrat. Pas de MQTT (cron + cloud + Slack) ; pas de support hors ligne décrit.
- La caméra sert à l'observation à distance ; l'analyse d'images (plantCV, diagnostic de maladies) est seulement suggérée, non réalisée (Protocol feasibility).
- Soudure nécessaire (DHT22, en-tête TSL2591), configuration réseau dépendante de l'institution (Appendix 2).
- Dépendance à des services tiers (Google Drive, Slack) ; sécurité du webhook non discutée.

## Pertinence pour la thèse

Pertinence modérée pour SerreIA. Elle porte sur l'axe `iot-greenhouse` : exemple minimal d'un nœud Pi avec capteurs T/HR/lumière, journalisation cloud et alertes par seuil, à comparer à l'architecture ESP32 + MQTT + Raspberry Pi 5 du projet. L'idée des alertes hors plage dans un canal de messagerie est transférable à la validation humaine de l'agent. Pour l'axe `growth`, c'est seulement la capture d'images périodique, sans mesure de croissance. Rien sur l'inférence edge (axe `edge-inference` retiré), le contrôle, la prévision ou les consignes.

## Gaps identifiés

- Pas de comparaison quantifiée entre capteurs bas coût (DHT22, TSL2591) et capteurs de référence en serre.
- Pas de combinaison surveillance + analyse d'images embarquée sur ce type de nœud Pi bas coût.
- Pas de mesure de fiabilité de longue durée (dérive des capteurs, pannes) ni de taux de fausses alertes.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction GROBID, `extraction.ok: true`). Le texte de la Conclusion est tronqué par l'extraction (phrase coupée) et les Appendices 1-3 sont partiellement fragmentés ; Fig. 1 et 3 vues seulement par leur légende.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de contrôle/actionneurs et de MQTT (constatée par absence dans le texte) ; l'inadéquation du lux pour un DLI ; la pertinence pour SerreIA.
