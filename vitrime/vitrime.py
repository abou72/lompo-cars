import streamlit as st

# ⚠️ DOIT être la toute première commande Streamlit
st.set_page_config(
    page_title="Lompocars Export — Voitures USA → Afrique",
    page_icon="🚗",
    layout="wide",
)

# Maintenant on peut importer le reste
import json
from database import init_db, get_cars, add_contact

init_db()

# ================== CONFIG ==================
WHATSAPP_NUM = "13476326546"
EMAIL_CONTACT = "contact@lompocars.com"
NOM_BOUTIQUE = "Lompocars Export"
DEVISE_2 = "FCFA"
# ============================================
# ================== CONFIG ==================
WHATSAPP_NUM = "13476326546"          # (347) 632-6546
EMAIL_CONTACT = "contact@lompocars.com"  # à changer plus tard
NOM_BOUTIQUE = "Lompocars Export"
DEVISE_2 = "FCFA"
# ============================================

# ---- CSS personnalisé ----
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #FFC107 0%, #FFD54F 100%);
    padding: 3rem 2rem; border-radius: 16px;
    text-align: center; margin-bottom: 2rem;
}
.hero h1 { color: #1A1A1A; font-size: 2.8rem; margin: 0; }
.hero p  { color: #333; font-size: 1.2rem; margin-top: 0.5rem; }
.badge {
    display:inline-block; background:#1A1A1A; color:#FFC107;
    padding:4px 12px; border-radius:20px; font-size:0.85rem;
    font-weight:bold; margin-bottom:10px;
}
.prix { color: #FF6B00; font-weight: bold; font-size: 1.3rem; }
</style>
""", unsafe_allow_html=True)

# ---- HERO ----
st.markdown(f"""
<div class="hero">
    <span class="badge">🇺🇸 USA → 🌍 AFRIQUE DE L'OUEST</span>
    <h1>🚗 {NOM_BOUTIQUE}</h1>
    <p>Votre voiture des USA livrée en Afrique de l'Ouest — Fiable, rapide, transparent</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.link_button(
        "📱 WhatsApp — (347) 632-6546",
        f"https://wa.me/{WHATSAPP_NUM}",
        use_container_width=True,
    )
with c2:
    st.link_button(
        "✉️ Nous écrire",
        f"mailto:{EMAIL_CONTACT}",
        use_container_width=True,
    )

st.divider()

# ---- CATALOGUE ----
st.markdown("## 🚙 Notre catalogue")

cars = get_cars()
if not cars:
    st.info("Aucune voiture disponible pour le moment. Revenez bientôt !")
    st.stop()

# Filtres
marques = ["Toutes"] + sorted({c["marque"] for c in cars if c["marque"]})
etats = ["Tous", "Neuf", "Occasion"]

f1, f2 = st.columns(2)
with f1:
    marque_f = st.selectbox("Marque", marques)
with f2:
    etat_f = st.selectbox("État", etats)

filtered = [
    c for c in cars
    if (marque_f == "Toutes" or c["marque"] == marque_f)
    and (etat_f == "Tous" or c["etat"] == etat_f)
]

# Grille
cols = st.columns(3)
for i, car in enumerate(filtered):
    with cols[i % 3]:
        with st.container(border=True):
            img = car["photo_principale"] or "https://via.placeholder.com/400x250?text=Lompocars"
            st.image(img, use_container_width=True)

            st.markdown(f"### {car['marque']} {car['modele']}")
            st.caption(f"📅 {car['annee']} • 🛣️ {car['kilometrage']:,} km • {car['etat']}")

            st.markdown(
                f"<p class='prix'>{car['prix_usd']:,.0f} $ "
                f"<small>(≈ {car['prix_fcfa']:,.0f} {DEVISE_2})</small></p>",
                unsafe_allow_html=True,
            )

            if car["statut"] == "Vendu":
                st.error("❌ VENDU")
            else:
                msg = (
                    f"Bonjour Lompocars, je suis intéressé par la "
                    f"{car['marque']} {car['modele']} {car['annee']} "
                    f"(réf. #{car['id']})"
                )
                wa_url = f"https://wa.me/{WHATSAPP_NUM}?text={msg.replace(' ', '%20')}"
                st.link_button("📱 Contacter sur WhatsApp", wa_url, use_container_width=True)

            with st.expander("Voir plus / Demander info"):
                st.write(car["description"] or "Pas de description.")

                # Photos supplémentaires (JSONB → liste Python)
                photos = car.get("photos")
                if isinstance(photos, str):
                    try:
                        photos = json.loads(photos)
                    except Exception:
                        photos = []
                if photos and len(photos) > 1:
                    st.write("**Autres photos :**")
                    for p in photos[1:]:
                        st.image(p, use_container_width=True)

                with st.form(f"contact_{car['id']}"):
                    st.write("**Vous êtes intéressé ? Laissez vos coordonnées :**")
                    nom = st.text_input("Votre nom")
                    email = st.text_input("Email")
                    wa = st.text_input("WhatsApp")
                    msg2 = st.text_area("Message")
                    if st.form_submit_button("📩 Envoyer"):
                        add_contact({
                            "nom": nom,
                            "email": email,
                            "whatsapp": wa,
                            "message": msg2,
                            "voiture_id": car["id"],
                        })
                        st.success("✅ Message envoyé ! Nous vous recontactons vite.")

st.divider()
st.caption(
    f"© {NOM_BOUTIQUE} — Export USA → Afrique de l'Ouest • "
    f"WhatsApp : (347) 632-6546"
)