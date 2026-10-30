# Plan 4 - echantillonner_arc

Test command: python -m pytest test/test_arcs.py -q

1. Lire la docstring complète de `echantillonner_arc` dans `code/arcs.py`, les fonctions utilitaires et les classes de données de l'arc, ainsi que les trois tests de collision dans `test/test_arcs.py`.
2. Implémenter uniquement `echantillonner_arc` dans `code/arcs.py` : évaluer les deux profils à chaque pas de temps, appliquer leurs signes directionnels, intégrer `(x, y, theta)` avec le modèle unicycle et s'arrêter à la première collision. Respecter le comportement documenté en l'absence d'obstacle et valider l'implémentation avec les tests existants, sans les affaiblir.
3. Lancer `python -m pytest test/test_arcs.py -q`.
4. En cas d'échec, utiliser le résultat du test pour apporter une correction minimale dans `code/arcs.py`, puis relancer la même commande. Répéter au maximum trois fois; si les tests échouent encore, indiquer dans `progress.md` que le plan est bloqué et consigner l'échec.
