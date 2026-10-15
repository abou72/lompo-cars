import streamlit as st
import json

# Connexion Neon (lue depuis secrets.toml → [connections.neon])
conn = st.connection("neon", type="sql")


def init_db():
    """Les tables sont créées manuellement dans Neon.
    Cette fonction ne fait plus rien mais on la garde pour compatibilité."""
    pass


def add_car(data: dict):
    conn.query(
        """INSERT INTO cars
        (marque, modele, annee, prix_usd, prix_fcfa, kilometrage,
         etat, description, photo_principale, photos, statut)
        VALUES (:marque, :modele, :annee, :prix_usd, :prix_fcfa,
                :kilometrage, :etat, :description, :photo_principale,
                :photos, :statut)""",
        params={
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
    conn.query(
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
        params={
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
    conn.query("DELETE FROM cars WHERE id = :id", params={"id": int(car_id)})


def add_contact(data: dict):
    conn.query(
        """INSERT INTO contacts (nom, email, whatsapp, message, voiture_id)
           VALUES (:nom, :email, :whatsapp, :message, :voiture_id)""",
        params={
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