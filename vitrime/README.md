# Lompocars Export — site vitrine

Site Streamlit (une page + espace admin) : catalogue de voitures USA → Afrique de l'Ouest.

## Lancer en local
1. `pip install -r requirements.txt`
2. Copier `.streamlit/secrets.toml.example` en `.streamlit/secrets.toml` et le remplir
3. `streamlit run vitrime.py`

Les tables `cars` et `contacts` sont créées automatiquement dans Neon si elles n'existent pas.

## Où modifier quoi
- `config.py` : nom, numéro WhatsApp, e-mail, délais, étapes, arguments, pays desservis
- `styles.py` : couleurs et design (variables en haut du fichier)
- `ui.py` : composants HTML (hero, cartes, sections, pied de page)
- `vitrime.py` : page d'accueil — `pages/Admin.py` : espace admin (`/Admin`)

## Admin
Le mot de passe se définit dans les secrets (`ADMIN_PASSWORD`), jamais dans le code.
Ajouter / modifier / marquer « Vendu » / supprimer une voiture, lire les messages reçus.

## Sécurité
`.streamlit/secrets.toml` ne doit jamais être publié (GitHub, zip partagé). Il est dans `.gitignore`.
