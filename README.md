# Ceux qui se marient

Papeterie du mariage d'Arnaud et Emily, le vendredi 7 mai 2027 au Château Eyparsac, à Beyssac en Corrèze.

## Les pages

| Fichier | À qui |
|---|---|
| `index.html` | Les propositions de save the date, à partager pour choisir |
| `imprimeur.html` | La version retenue avec fond perdu et repères de coupe |

Chaque page se règle en direct : la langue, le registre des prénoms, et le programme annoncé.

## Comment c'est fait

Les cartes ne sont pas du HTML écrit à la main, elles sont générées. Un seul script produit les deux pages :

```bash
python3 build/gen_print.py
```

- `build/gen_print.py` construit les compositions et les deux pages
- `build/gen_palettes.py` définit les palettes et les géométries de fleurs, et sert de bibliothèque au précédent
- `build/*_shell.html` sont les gabarits de page autour des cartes

Aucune dépendance, aucune étape de build. Python 3 seul suffit.

## Le format

A6 paysage, 148 × 105 mm, avec 3 mm de fond perdu sur chaque bord, soit 154 × 111 mm au total. Le SVG exporté est vectoriel et dimensionné en millimètres, c'est le fichier à donner à un imprimeur. Le PNG sort à 300 dpi.

## Ce qui n'est pas ici, et ne doit pas y venir

La liste des invités et les liens personnalisés par groupe restent en dehors de ce dépôt, qui est public.
