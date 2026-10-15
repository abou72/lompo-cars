import psycopg2

url = "postgresql://neondb_owner:npg_IyOYgbWP6x8G@ep-silent-cake-b4xudta2.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"

print("Connexion à Neon...")
try:
    conn = psycopg2.connect(url, connect_timeout=10)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cars;")
    print("✅ Connecté ! Nombre de voitures :", cur.fetchone()[0])
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Erreur :", repr(e))