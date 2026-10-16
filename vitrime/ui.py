"""Composants d'interface partagés (HTML, formats, liens)."""
from __future__ import annotations

import html
import json
from datetime import datetime
from urllib.parse import quote

import streamlit as st

import config as cfg
from cloudinary_helper import optimized
from styles import build_css

esc = html.escape

PLACEHOLDER = (
    "data:image/svg+xml;utf8,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E"
    "%3Crect width='400' height='300' fill='%23E3E8EF'/%3E"
    "%3Ctext x='200' y='160' font-family='sans-serif' font-size='20' "
    "text-anchor='middle' fill='%235A6B80'%3EPhoto bient%C3%B4t disponible%3C/text%3E%3C/svg%3E"
)


# ------------------------------------------------------------------ helpers
def fmt_int(n) -> str:
    """12345 -> '12 345' (espace fine insécable, usage français)."""
    try:
        return f"{int(round(float(n))):,}".replace(",", "\u202f")
    except (TypeError, ValueError):
        return "—"


def wa_link(message: str | None = None) -> str:
    url = f"https://wa.me/{cfg.WHATSAPP_NUM}"
    return f"{url}?text={quote(message)}" if message else url


def clean_phone(raw: str) -> str:
    return "".join(ch for ch in (raw or "") if ch.isdigit())


def parse_photos(car: dict) -> list[str]:
    photos = car.get("photos")
    if isinstance(photos, str):
        try:
            photos = json.loads(photos)
        except ValueError:
            photos = []
    photos = [p for p in (photos or []) if isinstance(p, str) and p]
    main = car.get("photo_principale")
    if main and main not in photos:
        photos.insert(0, main)
    return photos


def _compact(s: str) -> str:
    """Supprime indentations et sauts de ligne : un seul bloc HTML pour Markdown."""
    return "".join(line.strip() for line in s.splitlines())


def md(s: str) -> None:
    st.markdown(f'<div class="vt">{_compact(s)}</div>', unsafe_allow_html=True)


def inject_css(admin: bool = False) -> None:
    st.markdown(f"<style>{build_css(admin)}</style>", unsafe_allow_html=True)


# ------------------------------------------------------------------ blocs
def nav_and_hero() -> None:
    wa = wa_link()
    md(f"""
    <div id="top" class="anchor"></div>
    <nav class="nav"><div class="nav-in">
      <a class="brand" href="#top" target="_self">{esc(cfg.NOM_BOUTIQUE)}<span>{esc(cfg.SOUS_TITRE)}</span></a>
      <div class="nav-links">
        <a href="#catalogue" target="_self">Catalogue</a>
        <a href="#process" target="_self">Comment ça marche</a>
        <a href="#contact" target="_self">Contact</a>
      </div>
      <a class="btn btn-sign btn-sm" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div></nav>
    <header class="hero fb"><div class="hero-in">
      <h1>Roulez américain. Livré chez vous.</h1>
      <p class="lead">Nous gérons l'achat, l'inspection, le transport et la livraison de votre voiture, des États-Unis à l'Afrique de l'Ouest.</p>
      <div class="hero-cta">
        <a class="btn btn-sign" href="#catalogue" target="_self">Voir le catalogue</a>
        <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">Écrire sur WhatsApp</a>
      </div>
      <div class="route" aria-hidden="true">
        <div class="route-mid">{esc(cfg.DELAI)}</div>
        <div class="route-line"><span class="route-ship"></span></div>
        <div class="route-ends"><span>États-Unis</span><span>Afrique de l'Ouest</span></div>
      </div>
    </div></header>
    """)


def section_header(anchor: str, title: str, sub: str = "") -> None:
    sub_html = f'<p class="sub">{esc(sub)}</p>' if sub else ""
    md(f'<section class="sec"><div id="{anchor}" class="anchor"></div><h2>{esc(title)}</h2>{sub_html}</section>')


def car_card(car: dict) -> str:
    titre = f"{car['marque']} {car['modele']}"
    vendu = car.get("statut") == "Vendu"
    photos = parse_photos(car)
    img = optimized(photos[0], 800) if photos else PLACEHOLDER
    etat = car.get("etat") or ""
    tag_cls = "tag tag-new" if etat == "Neuf" else "tag"
    tag = f'<span class="{tag_cls}">{esc(etat)}</span>' if etat else ""
    sold = '<span class="sold">Vendu</span>' if vendu else ""

    specs = []
    if car.get("annee"):
        specs.append(f"<li>{int(car['annee'])}</li>")
    if car.get("kilometrage") is not None:
        specs.append(f"<li>{fmt_int(car['kilometrage'])} km</li>")

    usd = f"{fmt_int(car.get('prix_usd'))}\u00a0$"
    fcfa = f"≈ {fmt_int(car.get('prix_fcfa'))} {cfg.DEVISE_2}"

    desc = esc(car.get("description") or "").replace("\r", "").replace("\n", "<br>")
    desc_html = f"<p>{desc}</p>" if desc else ""
    extra = photos[1:7]
    thumbs = ""
    if extra:
        links = "".join(
            f'<a href="{esc(p)}" target="_blank" rel="noopener"><img src="{esc(optimized(p, 300))}" alt="{esc(titre)}" loading="lazy"></a>'
            for p in extra
        )
        thumbs = f'<div class="thumbs">{links}</div>'
    more = (
        f'<details class="more"><summary>Voir les détails</summary><div class="more-in">{desc_html}{thumbs}</div></details>'
        if (desc_html or thumbs) else ""
    )

    if vendu:
        cta = '<span class="btn btn-line btn-block" aria-disabled="true">Véhicule vendu</span>'
    else:
        msg = (f"Bonjour {cfg.NOM_BOUTIQUE}, je suis intéressé par la {titre} "
               f"{car.get('annee') or ''} (réf. #{car.get('id')})")
        cta = f'<a class="btn btn-wa btn-block" href="{wa_link(msg)}" target="_blank" rel="noopener">Demander sur WhatsApp</a>'

    return (
        f'<article class="car{" is-sold" if vendu else ""}">'
        f'<div class="car-media"><img src="{esc(img)}" alt="{esc(titre)}" loading="lazy">{tag}{sold}</div>'
        f'<div class="car-body"><h3>{esc(titre)}</h3><ul class="specs">{"".join(specs)}</ul>'
        f'<div class="price"><strong>{usd}</strong><span>{esc(fcfa)}</span></div>'
        f'{more}{cta}</div></article>'
    )


def render_grid(cars: list[dict]) -> None:
    md(f'<div class="grid">{"".join(car_card(c) for c in cars)}</div>')


def process_and_why() -> None:
    steps = "".join(
        f'<li><span class="dot">{i}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>'
        for i, (t, d) in enumerate(cfg.ETAPES, 1)
    )
    why = "".join(f"<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>" for t, d in cfg.ARGUMENTS)
    zones = "".join(f'<span class="chip">{esc(z)}</span>' for z in cfg.ZONES)
    md(f"""
    <section class="sec"><div id="process" class="anchor"></div>
      <h2>De l'Amérique à chez vous, en 4 étapes</h2>
      <p class="sub">Délai habituel : {esc(cfg.DELAI)} selon la destination.</p>
      <ol class="steps">{steps}</ol>
    </section>
    <section class="sec"><h2>Pourquoi nous faire confiance</h2><div class="why">{why}</div></section>
    <section class="sec"><h2>Zones desservies</h2><div class="chips">{zones}</div></section>
    """)


def contact_side() -> None:
    wa = wa_link()
    md(f"""
    <section class="sec contact-side"><div id="contact" class="anchor"></div>
      <h2>Parlons de votre voiture</h2>
      <p class="sub" style="margin-bottom:1.5rem">Vous ne trouvez pas votre modèle ? Dites-nous ce que vous cherchez, nous le trouvons sur demande.</p>
      <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">WhatsApp {esc(cfg.WHATSAPP_AFFICHE)}</a>
      <a class="btn btn-line" href="mailto:{esc(cfg.EMAIL_CONTACT)}">{esc(cfg.EMAIL_CONTACT)}</a>
    </section>
    """)


def footer() -> None:
    md(f"""
    <div class="foot fb"><div class="foot-in">
      <div><a class="brand" href="#top" target="_self">{esc(cfg.NOM_BOUTIQUE)}<span>{esc(cfg.SOUS_TITRE)}</span></a>
        <p>Voitures des États-Unis livrées en Afrique de l'Ouest.</p></div>
      <div><p>WhatsApp : <a href="{wa_link()}" target="_blank" rel="noopener">{esc(cfg.WHATSAPP_AFFICHE)}</a></p>
        <p>E-mail : <a href="mailto:{esc(cfg.EMAIL_CONTACT)}">{esc(cfg.EMAIL_CONTACT)}</a></p></div>
      <div><p><a href="Admin" target="_self">Espace admin</a></p></div>
    </div>
    <div class="copy">© {datetime.now().year} {esc(cfg.NOM_BOUTIQUE)} {esc(cfg.SOUS_TITRE)}</div></div>
    """)
