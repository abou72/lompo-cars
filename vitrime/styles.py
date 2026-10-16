"""Thème visuel Lompocars : marine océan + jaune signalisation.

Les sélecteurs commençant par `.vt ` sont préfixés par `.stApp` à l'injection
pour l'emporter sur les styles par défaut de Streamlit.
"""

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&display=swap');
:root{--ink:#0E1B2C;--ink-2:#12294A;--steel:#5A6B80;--steel-lt:#B9C5D4;--mist:#E3E8EF;--bg:#F4F6F9;--sign:#FFC400;--sign-ink:#1B1500;--wa:#128C54;--wa-dk:#0E7544;--sold:#B42318;}

/* ---- Cadre Streamlit ---- */
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],section.main{scroll-behavior:smooth;}
[data-testid="stAppViewContainer"]{overflow-x:hidden;}
.stApp{background:var(--bg);color:var(--ink);}
.stApp,.stApp p,.stApp label,.stApp input,.stApp textarea,.stApp button,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp li,.stApp a,.stApp [data-baseweb="select"] *{font-family:'Bricolage Grotesque',system-ui,-apple-system,'Segoe UI',sans-serif;}
header[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"],#MainMenu,footer{display:none !important;}
.block-container{max-width:1180px;padding:0 1.25rem 0 !important;}
.stApp [data-testid="stVerticalBlock"]{gap:.9rem;}

/* ---- Widgets ---- */
.stApp [data-testid="stWidgetLabel"] p,.stApp label p{font-weight:600;color:var(--ink);font-size:.92rem;}
.stApp [data-baseweb="input"],.stApp [data-baseweb="base-input"],.stApp [data-baseweb="textarea"],.stApp [data-baseweb="select"] > div{border-radius:10px !important;border-color:var(--mist) !important;background:#fff !important;}
.stApp [data-baseweb="input"]:focus-within,.stApp [data-baseweb="textarea"]:focus-within,.stApp [data-baseweb="select"] > div:focus-within{border-color:var(--ink) !important;}
.stApp [data-testid="stForm"]{background:#fff;border:1px solid var(--mist);border-radius:16px;padding:1.4rem;}
.stApp .stButton > button,.stApp [data-testid="stFormSubmitButton"] > button{min-height:46px;border-radius:10px;font-weight:700;border:1px solid var(--ink);background:#fff;color:var(--ink);}
.stApp .stButton > button:hover,.stApp [data-testid="stFormSubmitButton"] > button:hover{border-color:var(--ink);background:var(--mist);color:var(--ink);}
.stApp button[kind^="primary"]{background:var(--sign);border-color:var(--sign);color:var(--sign-ink);}
.stApp button[kind^="primary"] p{color:var(--sign-ink);}
.stApp button[kind^="primary"]:hover{background:#FFD23F;border-color:#FFD23F;color:var(--sign-ink);}
.stApp button:focus-visible,.stApp a:focus-visible,.stApp summary:focus-visible{outline:3px solid var(--ink);outline-offset:2px;}

/* ---- Boutons maison ---- */
.vt .btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:46px;padding:0 1.3rem;border-radius:10px;font-weight:700;font-size:1rem;text-decoration:none !important;border:1px solid transparent;transition:background .15s,border-color .15s;}
.vt .btn-block{display:flex;width:100%;}
.vt .btn-sm{min-height:38px;padding:0 1rem;font-size:.92rem;}
.vt .btn-sign{background:var(--sign);color:var(--sign-ink) !important;}
.vt .btn-sign:hover{background:#FFD23F;}
.vt .btn-wa{background:var(--wa);color:#fff !important;}
.vt .btn-wa:hover{background:var(--wa-dk);}
.vt .btn-ghost{background:transparent;color:#fff !important;border-color:rgba(255,255,255,.4);}
.vt .btn-ghost:hover{border-color:#fff;}
.vt .btn-line{background:#fff;color:var(--ink) !important;border-color:var(--ink);}
.vt .btn-line:hover{background:var(--mist);}
.vt .nav a:focus-visible,.vt .hero a:focus-visible,.vt .foot a:focus-visible{outline-color:var(--sign);}

/* ---- Navigation fixe ---- */
.fb{width:100vw;margin-left:calc(50% - 50vw);}
.vt .nav{position:fixed;top:0;left:0;right:0;z-index:999;background:rgba(14,27,44,.9);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);}
.vt .nav-in{max-width:1180px;margin:0 auto;height:64px;padding:0 1.25rem;display:flex;align-items:center;gap:2rem;}
.vt .brand{color:#fff !important;font-weight:800;font-size:1.35rem;letter-spacing:-.02em;text-decoration:none !important;margin-right:auto;}
.vt .brand span{font-weight:400;color:var(--steel-lt);margin-left:.35rem;}
.vt .nav-links{display:flex;gap:1.6rem;}
.vt .nav-links a{color:var(--steel-lt) !important;font-weight:500;text-decoration:none !important;font-size:.95rem;}
.vt .nav-links a:hover{color:#fff !important;}

/* ---- Hero ---- */
.vt .hero{background-color:var(--ink);background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.035) 0 2px,transparent 2px 34px),linear-gradient(160deg,#0E1B2C 0%,#12294A 100%);color:#fff;padding:8.5rem 0 4.5rem;}
.vt .hero-in{max-width:1180px;margin:0 auto;padding:0 1.25rem;}
.vt .hero h1{font-size:clamp(2.7rem,7.2vw,5.6rem);line-height:.98;letter-spacing:-.035em;font-weight:800;margin:0;padding:0;max-width:11em;color:#fff;}
.vt .hero .lead{font-size:clamp(1.05rem,2vw,1.3rem);color:var(--steel-lt);max-width:35em;margin:1.5rem 0 2rem;line-height:1.5;}
.vt .hero-cta{display:flex;flex-wrap:wrap;gap:.75rem;}
.vt .route{position:relative;margin-top:4rem;max-width:760px;}
.vt .route-line{position:relative;height:2px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 8px,transparent 8px 16px);}
.vt .route-line::after{content:"";position:absolute;left:0;top:0;height:2px;width:100%;background:var(--sign);transform:scaleX(0);transform-origin:left;animation:lc-draw 3.4s cubic-bezier(.65,0,.35,1) .5s forwards;}
.vt .route-ship{position:absolute;top:-6px;left:0;width:14px;height:14px;border-radius:50%;background:var(--sign);box-shadow:0 0 0 6px rgba(255,196,0,.22);animation:lc-sail 3.4s cubic-bezier(.65,0,.35,1) .5s forwards;}
.vt .route-mid{position:absolute;left:50%;top:-2rem;transform:translateX(-50%);color:var(--steel-lt);font-size:.88rem;white-space:nowrap;}
.vt .route-ends{display:flex;justify-content:space-between;margin-top:.9rem;font-weight:600;font-size:.95rem;}
@keyframes lc-draw{to{transform:scaleX(1);}}
@keyframes lc-sail{to{left:calc(100% - 14px);}}
@media (prefers-reduced-motion:reduce){.vt .route-line::after{animation:none;transform:scaleX(1);}.vt .route-ship{animation:none;left:calc(100% - 14px);}html,body,[data-testid="stMain"],section.main{scroll-behavior:auto;}}

/* ---- Sections ---- */
.vt .anchor{scroll-margin-top:84px;}
.vt .sec{padding:4.5rem 0 .5rem;}
.vt .sec h2{font-size:clamp(1.9rem,4vw,2.9rem);line-height:1.05;letter-spacing:-.025em;font-weight:800;margin:0 0 .6rem;padding:0;color:var(--ink);}
.vt .sec .sub{color:var(--steel);font-size:1.05rem;max-width:40em;margin:0;line-height:1.5;}
.vt .count{color:var(--steel);font-weight:500;font-size:.95rem;margin:.4rem 0 0;}

/* ---- Catalogue ---- */
.vt .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:1.25rem;align-items:start;margin:.5rem 0;}
.vt .car{background:#fff;border:1px solid var(--mist);border-radius:16px;overflow:hidden;}
.vt .car-media{position:relative;aspect-ratio:4/3;background:var(--mist);}
.vt .car-media img{width:100%;height:100%;object-fit:cover;display:block;}
.vt .car-media .tag{position:absolute;left:.75rem;top:.75rem;font-size:.8rem;font-weight:700;padding:.28rem .7rem;border-radius:999px;background:#fff;color:var(--ink);}
.vt .car-media .tag-new{background:var(--sign);color:var(--sign-ink);}
.vt .car.is-sold .car-media img{filter:grayscale(1) brightness(.55);}
.vt .car-media .sold{position:absolute;inset:0;display:grid;place-items:center;color:#fff;font-weight:800;font-size:1.7rem;letter-spacing:.02em;}
.vt .car-body{padding:1rem 1.1rem 1.2rem;}
.vt .car-body h3{font-size:1.25rem;font-weight:700;letter-spacing:-.01em;margin:0;padding:0;line-height:1.2;color:var(--ink);}
.vt .specs{list-style:none;display:flex;flex-wrap:wrap;margin:.45rem 0 0;padding:0;color:var(--steel);font-size:.93rem;}
.vt .specs li{margin:0;padding:0;}
.vt .specs li+li::before{content:"";display:inline-block;width:1px;height:.9em;background:var(--steel-lt);margin:0 .65rem;vertical-align:-1px;}
.vt .price{margin:.9rem 0 .9rem;display:flex;flex-direction:column;gap:.1rem;}
.vt .price strong{font-size:1.65rem;font-weight:800;letter-spacing:-.02em;line-height:1.1;}
.vt .price span{color:var(--steel);font-size:.92rem;}
.vt .more{margin:0 0 1rem;border-top:1px solid var(--mist);}
.vt .more summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:.93rem;padding:.7rem 0 .2rem;}
.vt .more summary::-webkit-details-marker{display:none;}
.vt .more summary::after{content:"+";font-size:1.3rem;font-weight:500;line-height:1;}
.vt .more[open] summary::after{content:"\2212";}
.vt .more-in p{margin:.5rem 0 .8rem;color:#2A3A4F;font-size:.95rem;line-height:1.55;}
.vt .thumbs{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem;}
.vt .thumbs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;display:block;}
.vt .empty{background:#fff;border:1px dashed var(--steel-lt);border-radius:16px;padding:2rem;text-align:center;color:var(--steel);}
.vt .empty strong{display:block;color:var(--ink);font-size:1.15rem;margin-bottom:.3rem;}

/* ---- Étapes (vraie séquence) ---- */
.vt .steps{list-style:none;margin:2.5rem 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;}
.vt .steps li{position:relative;margin:0;padding:0;}
.vt .steps li::before{content:"";position:absolute;top:19px;left:50px;right:-1.5rem;height:2px;background:var(--mist);}
.vt .steps li:last-child::before{display:none;}
.vt .dot{position:relative;z-index:1;display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--ink);color:#fff;font-weight:700;}
.vt .steps li:last-child .dot{background:var(--sign);color:var(--sign-ink);}
.vt .steps h3{font-size:1.2rem;font-weight:700;margin:1rem 0 .3rem;padding:0;}
.vt .steps p{margin:0;color:var(--steel);line-height:1.5;font-size:.97rem;}

/* ---- Arguments / zones ---- */
.vt .why{display:grid;grid-template-columns:repeat(2,1fr);gap:0 3rem;margin-top:2rem;}
.vt .why > div{border-top:1px solid var(--mist);padding:1.1rem 0 1.2rem;}
.vt .why h3{font-size:1.1rem;font-weight:700;margin:0 0 .25rem;padding:0;}
.vt .why p{margin:0;color:var(--steel);line-height:1.5;}
.vt .chips{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1.5rem;}
.vt .chip{padding:.5rem 1rem;border:1px solid var(--mist);border-radius:999px;background:#fff;font-weight:600;font-size:.95rem;}

/* ---- Contact ---- */
.vt .contact-side p{color:var(--steel);line-height:1.55;margin:0 0 1.2rem;}
.vt .contact-side .btn{margin:0 .5rem .6rem 0;}

/* ---- Pied de page ---- */
.vt .foot{background:var(--ink);color:var(--steel-lt);margin-top:5rem;padding:3rem 0 2rem;}
.vt .foot-in{max-width:1180px;margin:0 auto;padding:0 1.25rem;display:flex;flex-wrap:wrap;gap:2rem 4rem;justify-content:space-between;}
.vt .foot p{margin:.35rem 0 0;font-size:.95rem;}
.vt .foot a{color:var(--steel-lt) !important;text-decoration:none !important;}
.vt .foot a:hover{color:#fff !important;}
.vt .foot .copy{max-width:1180px;margin:2.5rem auto 0;padding:1.2rem 1.25rem 0;border-top:1px solid rgba(255,255,255,.12);font-size:.85rem;}

/* ---- Mobile ---- */
@media (max-width:820px){
.vt .nav-links{display:none;}
.vt .nav-in{gap:1rem;}
.vt .hero{padding:6.5rem 0 3rem;}
.vt .route{margin-top:3rem;}
.vt .steps{grid-template-columns:1fr;gap:1.6rem;}
.vt .steps li{padding-left:58px;}
.vt .steps li .dot{position:absolute;left:0;top:0;}
.vt .steps li::before{top:44px;bottom:-1.6rem;left:19px;right:auto;width:2px;height:auto;}
.vt .steps h3{margin-top:0;}
.vt .why{grid-template-columns:1fr;}
.vt .sec{padding-top:3.2rem;}
}
"""

ADMIN_EXTRA = ".block-container{padding-top:2rem !important;padding-bottom:3rem !important;}"


def build_css(admin: bool = False) -> str:
    css = CSS.replace(".vt ", ".stApp .vt ")
    if admin:
        css += ADMIN_EXTRA
    return css
