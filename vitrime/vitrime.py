import streamlit as st

# DOIT être la toute première commande Streamlit
st.set_page_config(
    page_title="Lompocars Export — Voitures USA → Afrique de l'Ouest",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import logging
import re
import time

import config as cfg
import ui
from database import add_contact, get_cars, init_db

log = logging.getLogger(__name__)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TRIS = ["Plus récentes", "Prix croissant", "Prix décroissant", "Année (récentes d'abord)"]

init_db()
ui.inject_css()
ui.nav_and_hero()

# ------------------------------------------------------------ catalogue
try:
    cars = get_cars()
except Exception:
    log.exception("Chargement du catalogue impossible")
    cars = []
    st.warning("Le catalogue est momentanément indisponible. Contactez-nous sur WhatsApp en attendant.")

ui.section_header("catalogue", "Le catalogue",
                  "Photos réelles, prix en dollars et en FCFA. Cliquez sur WhatsApp pour réserver ou poser une question.")

if cars:
    marques = ["Toutes"] + sorted({c["marque"] for c in cars if c["marque"]})
    etats = ["Tous"] + sorted({c["etat"] for c in cars if c["etat"]})

    f1, f2, f3, f4 = st.columns([2.2, 1.2, 1.2, 1.5])
    q = f1.text_input("Rechercher", placeholder="Ex. Camry, Highlander…").strip().lower()
    marque_f = f2.selectbox("Marque", marques)
    etat_f = f3.selectbox("État", etats)
    tri = f4.selectbox("Trier par", TRIS)

    filtered = [
        c for c in cars
        if (marque_f == "Toutes" or c["marque"] == marque_f)
        and (etat_f == "Tous" or c["etat"] == etat_f)
        and (not q or q in f"{c['marque']} {c['modele']} {c.get('annee') or ''}".lower())
    ]
    prix = lambda c: float(c.get("prix_usd") or 0)
    annee = lambda c: int(c.get("annee") or 0)
    if tri == "Prix croissant":
        filtered.sort(key=prix)
    elif tri == "Prix décroissant":
        filtered.sort(key=prix, reverse=True)
    elif tri.startswith("Année"):
        filtered.sort(key=annee, reverse=True)
    filtered.sort(key=lambda c: c.get("statut") == "Vendu")  # vendus en dernier (tri stable)

    # pagination : on repart de zéro dès que les filtres changent
    signature = (q, marque_f, etat_f, tri)
    if st.session_state.get("sig") != signature:
        st.session_state.sig = signature
        st.session_state.shown = cfg.PAGE_SIZE
    shown = st.session_state.get("shown", cfg.PAGE_SIZE)

    if filtered:
        n = len(filtered)
        st.markdown(f'<div class="vt"><p class="count">{n} véhicule{"s" if n > 1 else ""}</p></div>',
                    unsafe_allow_html=True)
        ui.render_grid(filtered[:shown])
        if n > shown:
            _, mid, _ = st.columns([1, 1, 1])
            if mid.button("Afficher plus de véhicules", use_container_width=True):
                st.session_state.shown = shown + cfg.PAGE_SIZE
                st.rerun()
    else:
        ui.md('<div class="empty"><strong>Aucun véhicule ne correspond.</strong>'
              'Modifiez les filtres ou écrivez-nous : nous cherchons votre modèle sur demande.</div>')
elif cars == []:
    ui.md('<div class="empty"><strong>Le catalogue se remplit.</strong>'
          'Écrivez-nous sur WhatsApp pour connaître les arrivages.</div>')

# ------------------------------------------------------------ process / confiance / zones
ui.process_and_why()

# ------------------------------------------------------------ contact
left, right = st.columns([5, 6], gap="large")
with left:
    ui.contact_side()
with right:
    st.markdown('<div style="height:4.2rem"></div>', unsafe_allow_html=True)
    options = {"Autre / sur demande": None}
    for c in cars:
        if c.get("statut") != "Vendu":
            options[f"{c['marque']} {c['modele']} {c.get('annee') or ''} (#{c['id']})".replace("  ", " ")] = c["id"]
    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Votre nom *")
        c1, c2 = st.columns(2)
        email = c1.text_input("E-mail")
        wa = c2.text_input("WhatsApp", placeholder="+225 …")
        voiture = st.selectbox("Véhicule concerné", list(options))
        message = st.text_area("Votre message *", height=110)
        envoyer = st.form_submit_button("Envoyer ma demande", type="primary", use_container_width=True)

    if envoyer:
        if not nom.strip() or not message.strip():
            st.error("Indiquez votre nom et votre message.")
        elif not email.strip() and not wa.strip():
            st.error("Laissez un e-mail ou un numéro WhatsApp pour que nous puissions vous répondre.")
        elif email.strip() and not EMAIL_RE.match(email.strip()):
            st.error("Cette adresse e-mail ne semble pas valide.")
        elif time.time() - st.session_state.get("last_contact", 0) < 20:
            st.warning("Votre demande vient d'être envoyée. Patientez quelques secondes avant d'en envoyer une autre.")
        else:
            try:
                add_contact({"nom": nom, "email": email, "whatsapp": wa,
                             "message": message, "voiture_id": options[voiture]})
                st.session_state.last_contact = time.time()
                st.success("Demande envoyée. Nous vous recontactons très vite.")
            except Exception:
                log.exception("Enregistrement du contact impossible")
                st.error("L'envoi a échoué. Écrivez-nous directement sur WhatsApp.")

ui.footer()
