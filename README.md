```bash

python -m venv .venv
source .venv/bin/activate
# ou .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Génération des données d'exemple

```bash
python generate_sample_data.py
```

### 3. Lancement des services

#### Interface Streamlit (Port 8790)

```bash
streamlit run app.py
```

#### API REST (Port 8987)

```bash
uvicorn api:app --host 0.0.0.0 --port 8987 --reload
```
