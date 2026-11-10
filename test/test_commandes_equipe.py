"""
test_commandes_equipe.py - NOS commandes de test, par opposition a celles du
professeur (test_enregistrements_enseignant.py).

Le professeur a dicte UNE sequence valide, une confirmation et une phrase fausse.
Cela ne couvre ni le recul, ni la rotation a droite, ni la distance autre que 1 m
ou 2 m, ni les valeurs par defaut. Nous ecrivons donc nos propres phrases, avec
pour chacune le mouvement ATTENDU (nom, valeur, sens), et nous verifions deux choses
que les tests du professeur ne regardent pas :

  - la valeur demandee arrive jusqu'au mouvement (distance = vitesse x duree,
    angle = vitesse angulaire x duree) ;
  - un modele qui se trompe sur les nombres ou sur le sens est rattrape.

DEUX ETAGES, comme chez le professeur :

  HORS LIGNE : un faux modele « paresseux » rend toujours les valeurs par defaut
    (2 m, 90 deg, sens horaire). L'interprete doit quand meme produire le bon plan.
    Tourne sans Ollama, sans micro, sans ROS2.

  MATERIEL (@pytest.mark.hardware, hors suite par defaut) : le VRAI modele recoit
    nos phrases. C'est lui qui montre si le prompt tient. Lancer avec :

        $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"
        & $py -m pytest test/test_commandes_equipe.py -m hardware -q

Chaque cas : (phrase, [(action, grandeur, sens)]), ou grandeur est la distance en
metres (avancer, reculer), l'angle en degres (tourner) ou 0 (arreter), et sens vaut
True (droite), False (gauche) ou None (sans objet).
"""

from __future__ import annotations

import json
import math

import pytest

from faux_ollama import FauxOllama
from llm_interpreter import LlmInterpreter
from state_machine import Etat, MachineDialogue
from voice import ScriptedInput, SortieVocale
from voice_turtle import boucle
from ihr_ros.turtle_io import open_turtle

# Nos commandes. Les nombres explicites doivent etre respectes a la lettre ;
# « Tourne a gauche » n'en donne aucun et retombe sur le defaut de la configuration.
CAS = {
    "avancer_3m": ("Avance de 3 mètres.", [("avancer", 3.0, None)]),
    "tourner_30_droite": ("Tourne de 30 degrés à droite.", [("tourner", 30.0, True)]),
    "reculer_1m5": ("Recule de 1,5 mètre.", [("reculer", 1.5, None)]),
    "tourner_gauche_defaut": ("Tourne à gauche.", [("tourner", 90.0, False)]),
    "sequence_trois_etapes": (
        "Avance de 2 mètres, tourne de 90 degrés à gauche, puis recule d'un mètre.",
        [("avancer", 2.0, None), ("tourner", 90.0, False), ("reculer", 1.0, None)],
    ),
    "arreter": ("Arrête-toi.", [("arreter", 0.0, None)]),
}

CONFIRMATIONS_OUI = ["Oui.", "Oui, c'est correct.", "D'accord."]
PHRASE_FAUSSE = "Il fait très beau aujourd'hui."


def _etape_paresseuse(nom: str) -> dict:
    """Ce que rend un modele qui ne lit pas les nombres : les valeurs par defaut."""
    return {"action": nom, "distance_m": 2.0, "angle_deg": 90.0,
            "is_forward": nom != "reculer", "is_clockwise": True}


def _reponse_paresseuse(attendu) -> str:
    """JSON d'un modele paresseux pour un cas : bon NOM d'action, valeurs par defaut."""
    if len(attendu) == 1:
        return json.dumps({**_etape_paresseuse(attendu[0][0]), "justification": "x"})
    return json.dumps({**_etape_paresseuse("avancer"), "action": "sequence",
                       "etapes": [_etape_paresseuse(nom) for nom, _, _ in attendu],
                       "justification": "x"})


def _verifier_plan(plan, attendu) -> None:
    """Compare chaque etape du plan au triplet attendu, mouvement physique compris."""
    assert len(plan.etapes) == len(attendu)
    for action, (nom, grandeur, sens) in zip(plan.etapes, attendu):
        assert action.nom == nom
        if nom in ("avancer", "reculer"):
            assert action.distance_m == pytest.approx(grandeur)
            assert abs(action.linear) * action.duree_s == pytest.approx(grandeur, rel=1e-3)
            assert (action.linear < 0) == (nom == "reculer")
        elif nom == "tourner":
            assert action.angle_deg == pytest.approx(grandeur)
            assert action.is_clockwise is sens
            assert (action.angular < 0) == bool(sens)
            if grandeur != 90.0:  # 90 = defaut de la config, duree fixe de 1 s
                tourne = math.degrees(abs(action.angular) * action.duree_s)
                assert tourne == pytest.approx(grandeur, rel=1e-3)
        else:
            assert action.linear == 0 and action.angular == 0


# --------------------------------------------------------------------- hors ligne

@pytest.mark.parametrize("cle", sorted(CAS))
def test_un_modele_paresseux_est_rattrape_sur_chacune_de_nos_phrases(cfg, cle):
    """Valeurs par defaut rendues par le modele : le plan final respecte quand meme la phrase."""
    phrase, attendu = CAS[cle]
    interprete = LlmInterpreter(cfg, client=FauxOllama([_reponse_paresseuse(attendu)]))

    resultat = interprete.interpreter(phrase)

    assert resultat.ok, resultat.erreur
    _verifier_plan(resultat.plan, attendu)


@pytest.mark.parametrize("cle", sorted(CAS))
def test_chaque_phrase_traverse_la_machine_jusqu_a_l_execution(cfg, cle):
    """Phrase dictee, deux confirmations, execution : les actions envoyees sont celles attendues."""
    phrase, attendu = CAS[cle]
    machine = MachineDialogue(mots_accord=cfg["affirmative_words"],
                              mots_refus=cfg["negative_words"],
                              mots_sortie=cfg["quit_words"])
    entree = ScriptedInput([phrase, CONFIRMATIONS_OUI[0], CONFIRMATIONS_OUI[0]],
                           phrase_de_fin="Quitter.")
    interprete = LlmInterpreter(cfg, client=FauxOllama([_reponse_paresseuse(attendu)]))
    turtle = open_turtle("sim", with_window=False, announce=None)

    try:
        resume = boucle(machine, entree, SortieVocale(actif=False), interprete,
                        turtle, cfg, max_tours=20, sleep=lambda _: None)
    finally:
        turtle.close()

    assert resume["etat_final"] == Etat.ARRET.value
    assert resume["echecs_interpretation"] == []
    assert resume["actions_executees"] == [nom for nom, _, _ in attendu]


def test_une_phrase_hors_domaine_ne_produit_aucun_mouvement(cfg):
    """« Il fait tres beau » : le modele repond hors catalogue, rien n'est execute."""
    essais = int(cfg["llm_max_attempts"])
    machine = MachineDialogue(mots_accord=cfg["affirmative_words"],
                              mots_refus=cfg["negative_words"],
                              mots_sortie=cfg["quit_words"])
    entree = ScriptedInput([PHRASE_FAUSSE, CONFIRMATIONS_OUI[0]], phrase_de_fin="Quitter.")
    interprete = LlmInterpreter(
        cfg, client=FauxOllama(['{"action": "faire beau"}'] * essais))
    turtle = open_turtle("sim", with_window=False, announce=None)

    try:
        resume = boucle(machine, entree, SortieVocale(actif=False), interprete,
                        turtle, cfg, max_tours=20, sleep=lambda _: None)
    finally:
        turtle.close()

    assert resume["actions_executees"] == []
    assert len(resume["echecs_interpretation"]) == 1


@pytest.mark.parametrize("confirmation", CONFIRMATIONS_OUI)
def test_nos_confirmations_sont_des_accords(cfg, confirmation):
    """Nos formulations d'accord, ponctuation de la dictee comprise, valent ACCORD."""
    from state_machine import Reponse, interpreter_reponse

    assert interpreter_reponse(confirmation, cfg["affirmative_words"],
                               cfg["negative_words"], cfg["quit_words"]) is Reponse.ACCORD


# --------------------------------------------------------------------- materiel

@pytest.mark.hardware
@pytest.mark.parametrize("cle", sorted(CAS))
def test_le_vrai_modele_traduit_nos_phrases(cfg, cle):
    """
    Le VRAI modele (Ollama) recoit nos phrases. Saute si Ollama est indisponible.
    Echoue si le prompt ne suffit pas : c'est exactement le defaut qu'un faux modele
    ne peut pas reveler.
    """
    phrase, attendu = CAS[cle]
    resultat = LlmInterpreter(cfg).interpreter(phrase)

    if not resultat.ok and "llama" in str(resultat.erreur).lower():
        pytest.skip(f"Ollama indisponible : {resultat.erreur}")
    assert resultat.ok, f"{phrase!r} : {resultat.erreur}"
    _verifier_plan(resultat.plan, attendu)
