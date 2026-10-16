"""Configuration unique de la boutique (une seule source de vérité)."""

NOM_BOUTIQUE = "Lompocars"
SOUS_TITRE = "Export"
WHATSAPP_NUM = "13476326546"          # format international, sans + ni espaces
WHATSAPP_AFFICHE = "(347) 632-6546"
EMAIL_CONTACT = "contact@lompocars.com"  # à changer plus tard
DEVISE_2 = "FCFA"
DELAI = "4 à 8 semaines"
PAGE_SIZE = 9  # véhicules affichés par "page" dans le catalogue

ZONES = [
    "Côte d'Ivoire", "Sénégal", "Ghana", "Bénin", "Togo",
    "Burkina Faso", "Mali", "Niger", "Nigeria",
]

ETAPES = [
    ("Choix", "Vous choisissez votre voiture dans notre catalogue ou sur demande."),
    ("Achat aux USA", "Nous achetons et inspectons le véhicule aux États-Unis."),
    ("Transport", "Mise en container et expédition maritime vers le port de destination."),
    ("Livraison", "Dédouanement et remise des clés dans votre pays."),
]

ARGUMENTS = [
    ("Véhicules inspectés", "Chaque voiture est vérifiée avant l'expédition."),
    ("Photos réelles", "Ce que vous voyez est ce que vous recevez."),
    ("Échange direct", "Vous parlez à notre équipe sur WhatsApp, sans intermédiaire."),
    ("Réseau logistique éprouvé", "Un circuit USA → Afrique que nous maîtrisons."),
    ("Délais annoncés", f"{DELAI} selon la destination."),
    ("Prix clairs", "Pas de frais cachés."),
    ("Accompagnement personnalisé", "Un interlocuteur du début à la fin."),
    ("Suivi du container", "Vous suivez votre véhicule jusqu'à l'arrivée."),
]
