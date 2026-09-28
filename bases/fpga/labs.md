# Labos et encadrants potentiels

Équipes repérées dans les papiers du corpus, en vue d'une candidature de thèse. Chaque entrée
cite les `paper_id` qui la justifient et distingue ce qui est lu dans le papier (affiliation,
auteurs) de ce qui est déduit (rattachement à un labo, thématique d'équipe).

Format d'une entrée :

```
### <labo / équipe>, <ville>
- Personnes : noms tels que dans les papiers.
- Lu : affiliation telle qu'imprimée (paper_id, en-tête).
- Déduit : rattachement, équipe, thématique — à vérifier sur le site du labo.
- Lien avec la thèse : axe ou gap couvert.
- À faire : vérification, prise de contact.
```

---

## France

### INSA Rennes (IETR ?), Rennes
- Personnes : Daniel Menard, Glenn Herrou, Christophe El Zeinaty ; Wassim Hamidouche
  (co-auteur).
- Lu : affiliations « INSA Rennes, Rennes, France » pour El Zeinaty, Herrou et Menard ;
  « Khalifa University of Science and Technology, Abu Dhabi » pour Hamidouche, et aussi pour
  El Zeinaty en double affiliation. Contact imprimé : daniel.menard@insa-rennes.fr
  (2025-el-zeinaty-designing-object-detection-models-tinyml, en-tête GROBID).
- Lu, travaux de l'équipe (fiche du 24/09/2026) :
  - survey de la détection d'objets sur MCU (quantification, pruning, KD, NAS) ;
  - propre travail cité en [164] : NAS guidée par LLM, avec distillation depuis un ViT,
    déployée sur STM32H7 avec 320 KB de SRAM (§6.4.2).
  Périmètre : MCU et TinyML. Le FPGA n'est cité qu'en perspective (CFU Playground, §8).
- Déduit : INSA Rennes est une tutelle de l'IETR (UMR CNRS 6164), et D. Menard y
  travaillerait sur l'arithmétique approximative et la compression de réseaux pour
  l'embarqué. L'IETR n'est **pas** imprimé dans le papier et l'équipe exacte n'y est pas
  donnée : à vérifier.
- Lien avec la thèse :
  - détection d'objets sur MCU, NAS « hardware-aware », co-design matériel-logiciel ;
  - axes `platforms` et `surveys` ;
  - complément « bas de gamme » d'une thèse FPGA, par exemple une comparaison MCU ↔ FPGA
    à mAP égale (gap déduit) ;
  - l'IETR figure dans la liste de départ (CLAUDE.md).
- À faire :
  - vérifier l'équipe IETR et les offres de thèse sur le site du labo ;
  - récupérer le dépôt public annoncé dans l'abstract (lien perdu à l'extraction) ;
  - lire [164] (NAS par LLM) : référence dans `papers/2025-el-zeinaty-…/refs.jsonl`.

## Hors France

Aucune entrée pour l'instant.
