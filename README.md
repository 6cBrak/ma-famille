# Ma Famille — MVP API

API FastAPI minimale pour gérer un arbre généalogique collaboratif :
- création de compte,
- création de famille + invitation,
- ajout de personnes,
- ajout de relations (`PARENT_OF`, `SPOUSE_OF`),
- lecture d'un arbre par `family_id`.

## Lancer

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```
