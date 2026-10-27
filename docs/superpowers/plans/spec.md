# Spécification

Implémenter les quatre fonctions incomplètes du Devoir 2, chacune dans son
propre plan : `signer`, `evaluer`, `Transitions.repondu` et
`echantillonner_arc`. Préserver les signatures publiques et respecter les
docstrings complètes ainsi que les tests existants dans `code/` et `test/`.

`signer` est le seul endroit où le signe des vitesses est appliqué : avancer
donne une vitesse positive et reculer une vitesse négative; la vitesse
angulaire antihoraire est positive et la vitesse horaire est négative
(REP-103). `evaluer` retourne la position et la magnitude positive de la
vitesse pendant l'accélération, le plateau et la décélération; il borne les
instants hors du profil à ses extrémités. `Transitions.repondu` doit utiliser
l'état de confirmation courant pour décider où mène un refus, et traiter les
réponses de sortie ou indécises avant les réponses ordinaires oui/non.
`echantillonner_arc` intègre simultanément les profils linéaire et angulaire
selon le modèle unicycle, et ne retourne des échantillons que jusqu'à la fin de
l'étape ou jusqu'à la première collision.

Ne pas supprimer, affaiblir ni réécrire les tests existants. Limiter chaque
modification à la fonction visée et à son module de tests correspondant. Après
chaque plan, lancer la commande de test ciblée qui y est indiquée. En cas
d'échec, s'appuyer sur le résultat du test pour corriger l'implémentation et
relancer les tests, au maximum trois fois. Si les tests échouent encore,
indiquer que le plan est bloqué dans `progress.md` et décrire l'échec restant;
ne pas prétendre que le travail est réussi et ne pas recommencer indéfiniment.
Lorsque les quatre plans réussissent, lancer cette commande de régression
combinée depuis la racine du projet `dev2` :
`python -m pytest test/test_state_machine.py test/test_trajectory.py test/test_arcs.py -q`.