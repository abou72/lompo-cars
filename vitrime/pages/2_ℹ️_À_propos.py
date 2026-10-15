import streamlit as st

st.set_page_config(page_title="À propos — Lompocars Export",
                   page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
.section {
    background:#FFF9E6; padding:1.5rem; border-radius:12px;
    border-left:5px solid #FFC107; margin-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("ℹ️ À propos de Lompocars Export")

st.markdown("""
### 🌍 Qui sommes-nous ?

**Lompocars Export** est votre partenaire de confiance pour l'achat
et l'exportation de véhicules depuis les États-Unis vers l'Afrique de l'Ouest.

Nous sélectionnons rigoureusement chaque véhicule, gérons toute la logistique
et vous accompagnons jusqu'à la livraison dans votre pays.
""")

st.divider()
st.subheader("📦 Notre processus en 4 étapes")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="section">
        <h3>1️⃣ Choix</h3>
        <p>Vous choisissez votre voiture dans notre catalogue ou sur demande.</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="section">
        <h3>2️⃣ Achat USA</h3>
        <p>Nous achetons et inspectons le véhicule aux États-Unis.</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="section">
        <h3>3️⃣ Transport</h3>
        <p>Mise en container et expédition maritime vers le port de destination.</p>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="section">
        <h3>4️⃣ Livraison</h3>
        <p>Dédouanement et remise des clés dans votre pays.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("✅ Pourquoi nous faire confiance ?")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - 🚗 **Véhicules inspectés** avant expédition
    - 📸 **Photos réelles** et transparentes
    - 💬 **Communication directe** par WhatsApp
    - 🌍 **Réseau logistique** éprouvé USA → Afrique
    """)
with col2:
    st.markdown("""
    - ⏱️ **Délais respectés** (4 à 8 semaines selon destination)
    - 💰 **Prix clairs**, sans frais cachés
    - 🤝 **Accompagnement personnalisé** du début à la fin
    - 📦 **Suivi du container** jusqu'à l'arrivée
    """)

st.divider()
st.subheader("📍 Zones desservies")
st.markdown("""
🇨🇮 Côte d'Ivoire • 🇸🇳 Sénégal • 🇬🇭 Ghana • 🇧🇯 Bénin • 🇹🇬 Togo •
🇧🇫 Burkina Faso • 🇲🇱 Mali • 🇳🇪 Niger • 🇳🇬 Nigeria
""")

st.divider()
st.subheader("📞 Nous contacter")
c1, c2 = st.columns(2)
with c1:
    st.link_button("📱 WhatsApp — (347) 632-6546",
                   "https://wa.me/13476326546", use_container_width=True)
with c2:
    st.link_button("✉️ Email", "mailto:contact@lompocars.com",
                   use_container_width=True)