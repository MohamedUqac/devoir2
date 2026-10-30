import subprocess, re, sys

plans = [
    ("plan1.md", [sys.executable, "-m", "pytest", "test/test_state_machine.py", "-k", "signer", "-q"],
     ["Lire le contrat de `signer` et ses tests",
      "Implémenter `signer` dans `code/state_machine.py`",
      "Réussir les tests ciblés `test_signer_*`"]),
    ("plan2.md", [sys.executable, "-m", "pytest", "test/test_trajectory.py", "-q"],
     ["Lire le contrat de `evaluer` et ses tests",
      "Implémenter `evaluer` dans `code/trajectory.py`",
      "Réussir `test/test_trajectory.py`"]),
    ("plan3.md", [sys.executable, "-m", "pytest", "test/test_state_machine.py", "-k", "refus_en_confirmation", "-q"],
     ["Lire le contrat de `Transitions.repondu`, l'analyseur et les tests de refus",
      "Implémenter `Transitions.repondu` dans `code/state_machine.py`",
      "Réussir les tests ciblés de refus"]),
    ("plan4.md", [sys.executable, "-m", "pytest", "test/test_arcs.py", "-q"],
     ["Lire le contrat de `echantillonner_arc`, les fonctions utilitaires et les tests de collision",
      "Implémenter `echantillonner_arc` dans `code/arcs.py`",
      "Réussir `test/test_arcs.py`"]),
]

header = """# Progression

Utiliser `[x]` uniquement lorsque l'étape et ses tests ciblés réussissent. Si
trois tentatives de correction ne résolvent pas un échec, marquer l'étape
d'implémentation `[!]` et consigner le test en échec ainsi que le résultat
observé. Ne pas terminer les plans suivants tant qu'une dépendance ou une
régression reste non résolue.
"""

body = header

for plan_name, cmd, steps in plans:
    r = subprocess.run(cmd, capture_output=True, text=True)
    output = r.stdout + r.stderr
    m = re.search(r"(\d+) passed", output)
    passed = int(m.group(1)) if m else 0
    failed = "failed" in output
    mark = "[ ]" if failed else "[x]"
    body += f"\n## {plan_name}\n"
    for i, step in enumerate(steps):
        if i == len(steps) - 1:
            body += f"- {mark} {step} ({passed} passed)\n"
        else:
            body += f"- {mark} {step}\n"

# regression
r2 = subprocess.run([sys.executable, "-m", "pytest",
    "test/test_state_machine.py", "test/test_trajectory.py", "test/test_arcs.py", "-q"],
    capture_output=True, text=True)
m2 = re.search(r"(\d+) passed", r2.stdout + r2.stderr)
total = int(m2.group(1)) if m2 else 0
reg_mark = "[x]" if total == 54 else "[ ]"
body += f"\n## Régression\n- {reg_mark} Réussir les tests de régression combinés ({total}/54)\n"

with open("progress.md", "w", encoding="utf-8") as f:
    f.write(body)

print(f"progress.md mis a jour - {total}/54 tests passes")
