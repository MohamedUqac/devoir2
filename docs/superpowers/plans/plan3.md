# Plan 3 - Transitions.repondu

Test command: python -m pytest test/test_state_machine.py -k refus_en_confirmation -q

1. Lire la docstring complète de `Transitions.repondu` dans `code/state_machine.py`, l'analyseur de réponses qu'elle appelle et les deux tests de refus dans `test/test_state_machine.py`.
2. Implémenter uniquement `Transitions.repondu` dans `code/state_machine.py`. Traiter les réponses de sortie et indécises avant les réponses ordinaires oui/non; en cas de refus, revenir à `ECOUTE` depuis `CONFIRMATION_COMMANDE` et à `INTERPRETATION` depuis `CONFIRMATION_ACTION`, en préservant la commande ou le plan attendu dans chaque cas.
3. Lancer `python -m pytest test/test_state_machine.py -k refus_en_confirmation -q`.
4. En cas d'échec, utiliser le résultat du test pour apporter une correction minimale dans `code/state_machine.py`, puis relancer la même commande. Répéter au maximum trois fois; si les tests échouent encore, indiquer dans `progress.md` que le plan est bloqué et consigner l'échec.