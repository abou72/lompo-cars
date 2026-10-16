"""Accès à la base Neon (PostgreSQL) via st.connection.

Les lectures passent par conn.query() (mises en cache), les écritures par une
session SQLAlchemy avec commit explicite, puis le cache est vidé.
"""
from __future__ import annotations

import json
import logging

import pandas as pd
import streamlit as st
from sqlalchemy import text

log = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    marque TEXT NOT NULL,
    modele TEXT NOT NULL,
    annee INTEGER,
    prix_usd NUMERIC DEFAULT 0,
    prix_fcfa NUMERIC DEFAULT 0,
    kilometrage INTEGER DEFAULT 0,
    etat TEXT DEFAULT 'Occasion',
    description TEXT,
    photo_principale TEXT,
    photos JSONB DEFAULT '[]'::jsonb,
    statut TEXT DEFAULT 'Disponible',
    date_ajout TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    email TEXT,
    whatsapp TEXT,
    message TEXT,
    voiture_id INTEGER REFERENCES cars(id) ON DELETE SET NULL,
    date TIMESTAMPTZ DEFAULT now()
);
"""


def _db_url() -> str | None:
    """URL Neon des secrets, avec le pilote psycopg2 explicite.

    SQLAlchemy 2.1 choisit psycopg (v3) pour « postgresql:// » : on force
    psycopg2 (déjà dans requirements.txt) pour éviter « No module named psycopg ».
    """
    try:
        url = st.secrets["connections"]["neon"]["url"]
    except Exception:
        return None
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg2://" + url[len(prefix):]
    return url


def _conn():
    # pool_pre_ping / pool_recycle : Neon coupe les connexions inactives
    # (« SSL connection has been closed unexpectedly »), on les rouvre à la volée.
    kwargs = {"pool_pre_ping": True, "pool_recycle": 280}
    url = _db_url()
    if url:
        kwargs["url"] = url
    return st.connection("neon", type="sql", **kwargs)


def _records(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> liste de dicts, NaN/NaT remplacés par None."""
    if df.empty:
        return []
    return df.astype(object).where(df.notna(), None).to_dict("records")


def _execute(sql: str, params: dict) -> None:
    with _conn().session as s:
        s.execute(text(sql), params)
        s.commit()
    st.cache_data.clear()  # les listes mises en cache sont périmées


@st.cache_resource(show_spinner=False)
def _ensure_schema() -> bool:
    try:
        with _conn().session as s:
            for stmt in SCHEMA.split(";"):
                if stmt.strip():
                    s.execute(text(stmt))
            s.commit()
        return True
    except Exception:  # base SQLite de test, droits limités, etc.
        log.warning("Création du schéma ignorée", exc_info=True)
        return False


def init_db() -> None:
    """Crée les tables si elles n'existent pas (une seule fois par processus)."""
    _ensure_schema()


# ---------------------------------------------------------------- voitures
def get_cars(statut: str | None = None) -> list[dict]:
    if statut:
        df = _conn().query(
            "SELECT * FROM cars WHERE statut = :statut ORDER BY date_ajout DESC",
            params={"statut": statut}, ttl=30,
        )
    else:
        df = _conn().query("SELECT * FROM cars ORDER BY date_ajout DESC", ttl=30)
    return _records(df)


def _car_params(data: dict) -> dict:
    return {
        "marque": data["marque"].strip(),
        "modele": data["modele"].strip(),
        "annee": int(data["annee"]),
        "prix_usd": float(data["prix_usd"]),
        "prix_fcfa": float(data["prix_fcfa"]),
        "kilometrage": int(data["kilometrage"]),
        "etat": data["etat"],
        "description": (data.get("description") or "").strip(),
        "statut": data.get("statut", "Disponible"),
    }


def add_car(data: dict) -> None:
    params = _car_params(data)
    params["photo_principale"] = data["photo_principale"]
    params["photos"] = json.dumps(data["photos"])
    _execute(
        """INSERT INTO cars
           (marque, modele, annee, prix_usd, prix_fcfa, kilometrage,
            etat, description, photo_principale, photos, statut)
           VALUES (:marque, :modele, :annee, :prix_usd, :prix_fcfa, :kilometrage,
                   :etat, :description, :photo_principale, :photos, :statut)""",
        params,
    )


def update_car(car_id, data: dict) -> None:
    params = _car_params(data)
    params["id"] = int(car_id)
    _execute(
        """UPDATE cars SET
               marque = :marque, modele = :modele, annee = :annee,
               prix_usd = :prix_usd, prix_fcfa = :prix_fcfa,
               kilometrage = :kilometrage, etat = :etat,
               description = :description, statut = :statut
           WHERE id = :id""",
        params,
    )


def delete_car(car_id) -> None:
    _execute("DELETE FROM cars WHERE id = :id", {"id": int(car_id)})


# ---------------------------------------------------------------- contacts
def add_contact(data: dict) -> None:
    _execute(
        """INSERT INTO contacts (nom, email, whatsapp, message, voiture_id)
           VALUES (:nom, :email, :whatsapp, :message, :voiture_id)""",
        {
            "nom": data["nom"].strip(),
            "email": (data.get("email") or "").strip(),
            "whatsapp": (data.get("whatsapp") or "").strip(),
            "message": data["message"].strip(),
            "voiture_id": data.get("voiture_id"),
        },
    )


def get_contacts() -> list[dict]:
    df = _conn().query(
        """SELECT c.*, v.marque, v.modele, v.annee
           FROM contacts c LEFT JOIN cars v ON v.id = c.voiture_id
           ORDER BY c.date DESC""",
        ttl=30,
    )
    return _records(df)
