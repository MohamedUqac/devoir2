# Plan 1 - signer

Test command: python -m pytest test/test_state_machine.py -k signer -q

1. Lire la docstring complète de `signer` dans `code/state_machine.py` et tous les cas `test_signer_*` de `test/test_state_machine.py`.
2. Implémenter uniquement `signer` dans `code/state_machine.py`, en appliquant le signe avant/arrière à la magnitude linéaire et le signe horaire/antihoraire de REP-103 à la magnitude angulaire.
3. Lancer `python -m pytest test/test_state_machine.py -k signer -q`.
4. En cas d'échec, examiner l'assertion, apporter une correction minimale dans `code/state_machine.py`, puis relancer la même commande. Répéter au maximum trois fois; si le test échoue encore, indiquer dans `progress.md` que le plan est bloqué et consigner l'échec.