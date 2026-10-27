# Plan 2 - evaluer

Test command: python -m pytest test/test_trajectory.py -q

1. Lire la docstring complète de `evaluer` dans `code/trajectory.py` et les cas pertinents de `test/test_trajectory.py`, y compris le test de position et de vitesse à l'intérieur de la phase de décélération.
2. Implémenter uniquement `evaluer` dans `code/trajectory.py` : borner les instants aux extrémités et calculer la position ainsi que la magnitude positive de la vitesse pendant les phases d'accélération, de plateau et de décélération.
3. Lancer `python -m pytest test/test_trajectory.py -q`.
4. En cas d'échec, utiliser le résultat du test pour apporter une correction minimale dans `code/trajectory.py`, puis relancer la même commande. Répéter au maximum trois fois; si les tests échouent encore, indiquer dans `progress.md` que le plan est bloqué et consigner l'échec.