---
description: Précise le profil thématique de la base (profile.md, axes et règles de base.json) ; propose, n'applique qu'après accord
argument-hint: [thème ou consigne] (vide : traiter les suggestions en attente)
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(bin/pdb base info:*), Bash(bin/pdb base check:*), Bash(bin/pdb base list), Bash(bin/pdb reindex), Bash(bin/pdb paper:*), Bash(mkdir -p .cache)
---

Précise le profil thématique de la base courante. Argument : `$ARGUMENTS`.

Le profil a deux faces (DATA_MODEL §11) :
- `profile.md`, pour l'humain et le LLM : thème donné par l'utilisateur, précisions, inclus,
  exclus, vocabulaire, suggestions en attente, historique ;
- `base.json`, pour le code : `axes` ({id: titre}), `axis_rules` ({axe: regex}, axes devinés à
  l'ingestion), `axis_queries` ({axe: requête OpenAlex}), `hardware_axes`, `topic_re`,
  `title_topic_re`, `topic_min_hits` (critère « dans le sujet » de `discover` et de
  `pdb base scan`), `tag_rules` ([[regex, tag], …]).

**Règle absolue : tu proposes, l'utilisateur décide.** Rien n'est écrit dans `profile.md` ni
dans `base.json` avant son accord explicite. La section « Thème (utilisateur) » n'est jamais
réécrite par toi : seul l'utilisateur la change, ou dicte le nouveau texte.

## 1. État des lieux

`bin/pdb base info`, puis lis `profile.md`, `base.json` et `INDEX.md`. S'il y a des fiches
`done`, parcours leurs sections « Problème » et « Pertinence » (pas le texte intégral), et le
haut d'`external_refs.csv`.

Trois situations :
- **`profile.md` absent** (base créée avant les profils) : rédige-le depuis `base.json` et le
  début de `CLAUDE.md`. Le texte de présentation de `CLAUDE.md` va, mot pour mot, dans
  « Thème (utilisateur) ». Fais-le valider comme une proposition (étape 3).
- **Base neuve** (un seul axe `surveys`, pas de règles) : pars du thème, et de `$ARGUMENTS` s'il
  en donne davantage. Si le thème est trop vague pour découper des axes, pose au plus 3
  questions courtes (sous-thèmes, ce qui est hors sujet, finalité : thèse, veille…) avant de
  proposer.
- **Base en cours** : traite les « Suggestions en attente », les papiers sans axe, les axes
  sans règle ou vides, et `$ARGUMENTS` s'il demande un changement.

## 2. Proposition

Construis :
- **Axes** : 4 à 9, plus `surveys`. Identifiants courts en kebab-case, titres en français.
  Un axe doit pouvoir regrouper plusieurs papiers : pas d'axe pour un papier isolé. Ne renomme
  ni ne supprime un axe porté par des papiers sans le dire (il faudrait alors corriger leurs
  `metadata.json` : propose-le explicitement, avec la liste).
- **`axis_rules`** : regex Python insensibles à la casse, sur titre + résumé. Bornes de mot
  (`\b`, écrit `\\b` dans le JSON) sur les sigles, alternatives pour les variantes (`auto-?encoder`). Préfère une règle
  un peu stricte : un axe manqué se corrige dans `/paper-fiche`, un axe faux pollue `INDEX.md`.
- **`axis_queries`** : une requête OpenAlex en anglais par axe.
- **`topic_re` / `title_topic_re` / `hardware_axes`** : seulement si le thème a un contexte
  obligatoire (ex. « sur matériel embarqué »). Sinon laisse-les vides : tout candidat est alors
  dans le sujet.
- **`tag_rules`** : étiquettes utiles au filtrage (plateformes, méthodes, datasets).
- **`profile.md`** : « Précisions » (périmètre, questions de recherche), « Inclus »,
  « Exclus », « Vocabulaire ». Chaque suggestion traitée sort de « Suggestions en attente ».

Écris le `base.json` proposé dans `.cache/base.proposed.json` (après `mkdir -p .cache` ; ce
fichier-là seulement), puis `bin/pdb base check --config .cache/base.proposed.json` : il valide
les regex et montre les papiers dont les axes devinés changeraient. Des fiches `done` touchées,
c'est normal : leurs axes, confirmés à la lecture, priment et ne changent pas.
Un « ATTENTION axe non déclaré » bloque : corrige la proposition.

## 3. Présentation

Montre :
1. un tableau des axes : id, titre, règle, effectif actuel → effectif estimé (d'après `check`) ;
2. le diff de `profile.md` (sections modifiées seulement) ;
3. les autres changements de `base.json` (topic, tags, requêtes) ;
4. pour chaque suggestion en attente : retenue, écartée ou reportée, avec la raison.

Puis demande l'accord. L'utilisateur peut tout accepter, accepter en partie ou corriger.

## 4. Application (après accord seulement)

- Remplace `base.json` par la proposition acceptée (avec les corrections de l'utilisateur).
- Mets à jour `profile.md` et ajoute sous « Historique » une ligne datée par changement :
  `- AAAA-MM-JJ — <changement> — <raison>`.
- `bin/pdb base check`, puis `bin/pdb reindex` : les deux doivent passer sans erreur.
- Supprime `.cache/base.proposed.json`.

Les axes des papiers existants ne sont pas recalculés automatiquement. Liste les papiers `todo`
dont `check` montre un changement, et propose `/paper-fiche` pour ceux dont le classement
compte.

Réponds en français, brièvement. Termine par 2-3 pistes : `bin/pdb base scan` ou
`/paper-discover <axe>` sur l'axe le plus maigre, papiers à relire, gap à creuser.
