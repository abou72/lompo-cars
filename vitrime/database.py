import streamlit as st
import json
from sqlalchemy import text

# Connexion Neon
conn = st.connection("neon", type="sql")


def _execute(sql: str, params: dict = None):
    """Exécute une requête d'écriture (INSERT/UPDATE/DELETE) via transaction."""
    engine = conn.engine  # accès à l'engine SQLAlchemy sous-jacent
    with engine.begin() as connection:  # commit automatique à la sortie
        connection.execute(text(sql), params or {})


def init_db():
    """Les tables sont créées manuellement dans Neon."""
    pass


# ==================== CARS ====================

def add_car(data: dict):
    _execute(
        """INSERT INTO cars
        (marque, modele, annee, prix_usd, prix_fcfa, kilometrage,
         etat, description, photo_principale, photos, statut)
        VALUES (:marque, :modele, :annee, :prix_usd, :prix_fcfa,
                :kilometrage, :etat, :description, :photo_principale,
                :photos, :statut)""",
        {
            "marque": data["marque"],
            "modele": data["modele"],
            "annee": int(data["annee"]),
            "prix_usd": float(data["prix_usd"]),
            "prix_fcfa": float(data["prix_fcfa"]),
            "kilometrage": int(data["kilometrage"]),
            "etat": data["etat"],
            "description": data["description"],
            "photo_principale": data["photo_principale"],
            "photos": json.dumps(data["photos"]),
            "statut": data.get("statut", "Disponible"),
        },
    )


def get_cars(statut=None):
    if statut:
        df = conn.query(
            "SELECT * FROM cars WHERE statut = :statut ORDER BY date_ajout DESC",
            params={"statut": statut},
            ttl=5,
        )
    else:
        df = conn.query(
            "SELECT * FROM cars ORDER BY date_ajout DESC",
            ttl=5,
        )
    return df.to_dict("records")


def update_car(car_id, data: dict):
    _execute(
        """UPDATE cars SET
            marque = :marque,
            modele = :modele,
            annee = :annee,
            prix_usd = :prix_usd,
            prix_fcfa = :prix_fcfa,
            kilometrage = :kilometrage,
            etat = :etat,
            description = :description,
            statut = :statut
        WHERE id = :id""",
        {
            "marque": data["marque"],
            "modele": data["modele"],
            "annee": int(data["annee"]),
            "prix_usd": float(data["prix_usd"]),
            "prix_fcfa": float(data["prix_fcfa"]),
            "kilometrage": int(data["kilometrage"]),
            "etat": data["etat"],
            "description": data["description"],
            "statut": data["statut"],
            "id": int(car_id),
        },
    )


def delete_car(car_id):
    _execute("DELETE FROM cars WHERE id = :id", {"id": int(car_id)})


# ==================== CONTACTS ====================

def add_contact(data: dict):
    _execute(
        """INSERT INTO contacts (nom, email, whatsapp, message, voiture_id)
           VALUES (:nom, :email, :whatsapp, :message, :voiture_id)""",
        {
            "nom": data["nom"],
            "email": data["email"],
            "whatsapp": data["whatsapp"],
            "message": data["message"],
            "voiture_id": data.get("voiture_id"),
        },
    )


def get_contacts():
    df = conn.query("SELECT * FROM contacts ORDER BY date DESC", ttl=5)
    return df.to_dict("records")