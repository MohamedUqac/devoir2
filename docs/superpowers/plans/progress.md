# Progression

Utiliser `[x]` uniquement lorsque l'étape et ses tests ciblés réussissent. Si
trois tentatives de correction ne résolvent pas un échec, marquer l'étape
d'implémentation `[!]` et consigner le test en échec ainsi que le résultat
observé. Ne pas terminer les plans suivants tant qu'une dépendance ou une
régression reste non résolue.

## plan1.md
- [ ] Lire le contrat de `signer` et ses tests
- [ ] Implémenter `signer` dans `code/state_machine.py`
- [ ] Réussir les tests ciblés `test_signer_*`

## plan2.md
- [ ] Lire le contrat de `evaluer` et ses tests
- [ ] Implémenter `evaluer` dans `code/trajectory.py`
- [ ] Réussir `test/test_trajectory.py`

## plan3.md
- [ ] Lire le contrat de `Transitions.repondu`, l'analyseur et les tests de refus
- [ ] Implémenter `Transitions.repondu` dans `code/state_machine.py`
- [ ] Réussir les tests ciblés de refus

## plan4.md
- [ ] Lire le contrat de `echantillonner_arc`, les fonctions utilitaires et les tests de collision
- [ ] Implémenter `echantillonner_arc` dans `code/arcs.py`
- [ ] Réussir `test/test_arcs.py`
- [ ] Réussir les tests de régression combinés de la machine d'état, des trajectoires et des arcs