import streamlit as st
from database import init_db, get_cars, add_car, update_car, delete_car, get_contacts
from cloudinary_helper import upload_image

st.set_page_config(page_title="Admin — Lompocars", page_icon="🔒", layout="wide")
init_db()

# ---- AUTH ----
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Espace Admin — Lompocars")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if pwd == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")
    st.stop()

# ---- DÉCONNEXION ----
c1, c2 = st.columns([4, 1])
with c1:
    st.title("🔒 Gestion Lompocars Export")
with c2:
    if st.button("🚪 Déconnexion"):
        st.session_state.auth = False
        st.rerun()

tab1, tab2 = st.tabs(["🚗 Voitures", "📩 Messages reçus"])

# ============ TAB VOITURES ============
with tab1:
    with st.expander("➕ Ajouter une voiture", expanded=False):
        with st.form("add_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            marque = c1.text_input("Marque *")
            modele = c2.text_input("Modèle *")
            annee  = c3.number_input("Année", 1990, 2030, 2020)

            c4, c5, c6 = st.columns(3)
            prix_usd  = c4.number_input("Prix USD *", 0.0, step=100.0)
            prix_fcfa = c5.number_input("Prix FCFA *", 0.0, step=1000.0)
            km        = c6.number_input("Kilométrage", 0, step=1000)

            etat = st.selectbox("État", ["Occasion", "Neuf"])
            desc = st.text_area("Description")

            photos_files = st.file_uploader(
                "Photos (la 1ère sera la photo principale)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True
            )

            submitted = st.form_submit_button("💾 Enregistrer", use_container_width=True)

            if submitted:
                if not marque or not modele:
                    st.error("Marque et modèle obligatoires.")
                elif not photos_files:
                    st.error("Ajoutez au moins une photo.")
                else:
                    with st.spinner("Upload des photos sur Cloudinary..."):
                        urls = []
                        for f in photos_files:
                            try:
                                urls.append(upload_image(f))
                            except Exception as e:
                                st.error(f"Erreur upload {f.name}: {e}")

                    if urls:
                        add_car({
                            "marque": marque, "modele": modele, "annee": annee,
                            "prix_usd": prix_usd, "prix_fcfa": prix_fcfa,
                            "kilometrage": km, "etat": etat, "description": desc,
                            "photo_principale": urls[0],
                            "photos": urls,
                            "statut": "Disponible"
                        })
                        st.success("✅ Voiture ajoutée !")
                        st.rerun()

    st.divider()
    st.subheader("📋 Voitures existantes")

    cars = get_cars()
    if not cars:
        st.info("Aucune voiture pour le moment.")
    else:
        for car in cars:
            emoji = "❌" if car["statut"] == "Vendu" else "✅"
            with st.expander(f"{emoji} {car['marque']} {car['modele']} ({car['annee']}) — #{car['id']}"):
                c1, c2 = st.columns([1, 2])
                with c1:
                    if car["photo_principale"]:
                        st.image(car["photo_principale"], use_container_width=True)
                with c2:
                    statut = st.selectbox(
                        "Statut", ["Disponible", "Vendu"],
                        index=0 if car["statut"] == "Disponible" else 1,
                        key=f"st_{car['id']}"
                    )
                    desc = st.text_area("Description",
                                        car["description"] or "",
                                        key=f"desc_{car['id']}")
                    c3, c4 = st.columns(2)
                    prix_usd = c3.number_input("Prix USD",
                        value=float(car["prix_usd"] or 0),
                        key=f"pu_{car['id']}")
                    prix_fcfa = c4.number_input("Prix FCFA",
                        value=float(car["prix_fcfa"] or 0),
                        key=f"pf_{car['id']}")

                    b1, b2 = st.columns(2)
                    if b1.button("💾 Mettre à jour", key=f"up_{car['id']}",
                                 use_container_width=True):
                        d = dict(car)
                        d.update({"statut": statut, "description": desc,
                                  "prix_usd": prix_usd, "prix_fcfa": prix_fcfa})
                        update_car(car["id"], d)
                        st.success("✅ Mis à jour")
                        st.rerun()

                    if b2.button("🗑️ Supprimer", key=f"del_{car['id']}",
                                 use_container_width=True):
                        delete_car(car["id"])
                        st.warning("🗑️ Supprimée")
                        st.rerun()

# ============ TAB MESSAGES ============
with tab2:
    st.subheader("📩 Messages reçus")
    contacts = get_contacts()
    if not contacts:
        st.info("Aucun message pour le moment.")
    else:
        for ct in contacts:
            with st.expander(f"👤 {ct['nom']} — {ct['date']}"):
                st.write(f"**Email** : {ct['email']}")
                st.write(f"**WhatsApp** : {ct['whatsapp']}")
                st.write(f"**Voiture ID** : {ct['voiture_id']}")
                st.write(f"**Message** : {ct['message']}")
                if ct["whatsapp"]:
                    wa_link = f"https://wa.me/{ct['whatsapp'].replace('+','').replace(' ','')}"
                    st.link_button("📱 Répondre sur WhatsApp", wa_link)