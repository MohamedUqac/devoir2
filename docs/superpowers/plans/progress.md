# Progression

Utiliser `[x]` uniquement lorsque l'étape et ses tests ciblés réussissent. Si
trois tentatives de correction ne résolvent pas un échec, marquer l'étape
d'implémentation `[!]` et consigner le test en échec ainsi que le résultat
observé. Ne pas terminer les plans suivants tant qu'une dépendance ou une
régression reste non résolue.

## plan1.md
- [x] Lire le contrat de `signer` et ses tests
- [x] Implémenter `signer` dans `code/state_machine.py`
- [x] Réussir les tests ciblés `test_signer_*` (4 passed)

## plan2.md
- [x] Lire le contrat de `evaluer` et ses tests
- [x] Implémenter `evaluer` dans `code/trajectory.py`
- [x] Réussir `test/test_trajectory.py` (14 passed)

## plan3.md
- [x] Lire le contrat de `Transitions.repondu`, l'analyseur et les tests de refus
- [x] Implémenter `Transitions.repondu` dans `code/state_machine.py`
- [x] Réussir les tests ciblés de refus (2 passed)

## plan4.md
- [x] Lire le contrat de `echantillonner_arc`, les fonctions utilitaires et les tests de collision
- [x] Implémenter `echantillonner_arc` dans `code/arcs.py`
- [x] Réussir `test/test_arcs.py` (10 passed)

## Régression
- [x] Réussir les tests de régression combinés (54/54)
