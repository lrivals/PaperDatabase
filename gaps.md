# Carte des gaps

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent et
distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

---

## Autoencodeurs

### Autoencodeurs sur FPGA appliqués aux images
- Constat : dans la bibliographie de départ (`basicStart.txt`, résumés seulement), les
  autoencodeurs sur FPGA portent surtout sur des séries temporelles et la physique des
  particules ; le seul cas « image » cité passe par des scalogrammes de signaux 1D (CAE sur
  PYNQ-Z2).
- Ce qui manque : CAE/VAE sur images ou vidéo réelles (compression, détection d'anomalies
  visuelle) avec mesures de latence et de puissance sur FPGA embarqué.
- Statut : hypothèse — à étayer par des fiches `done`.
- Piste : recherches ciblées « convolutional autoencoder image FPGA », « VAE video anomaly
  detection FPGA ».
