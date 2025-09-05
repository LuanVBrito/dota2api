import requests
import os
import dotenv
import pymysql
import pymysql.cursors

dotenv.load_dotenv()

def get_opendota(endpoint: str, params: dict = None):
    base_url = "https://api.opendota.com/api"
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []


connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    cursorclass=pymysql.cursors.DictCursor,
)

with connection.cursor() as cursor:

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                localized_name VARCHAR(100)
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hero_stats (
                   id INT PRIMARY KEY,
                   primary_attr VARCHAR(100),
                   attack_type VARCHAR(100),
                   pro_win INT,
                   pro_ban INT,
                   pro_pick INT,
                   FOREIGN KEY (id) REFERENCES heroes(id)
            )    
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hero_roles (
                   hero_id INT,
                   role VARCHAR(100),
                   PRIMARY KEY (hero_id, role),
                   FOREIGN KEY (hero_id) REFERENCES heroes(id)
            )
    """)
    
    heroes = get_opendota("heroes")
    heroStats = get_opendota("heroStats")

    for hero in heroes:
        cursor.execute("""
        INSERT INTO heroes (id, name, localized_name)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name=VALUES(name),
            localized_name=VALUES(localized_name)
    """, (hero["id"], hero["name"], hero["localized_name"]))
        
    for stats in heroStats:
        cursor.execute("""
            INSERT INTO hero_stats (id, primary_attr, attack_type, pro_win, pro_ban, pro_pick)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                primary_attr=VALUES(primary_attr),
                attack_type=VALUES(attack_type),
                pro_win=VALUES(pro_win),
                pro_ban=VALUES(pro_ban),
                pro_pick=VALUES(pro_pick)
        """, (stats["id"], stats["primary_attr"], stats["attack_type"], stats["pro_win"], stats["pro_ban"], stats["pro_pick"]))

        for role in stats["roles"]:
            cursor.execute("""
                INSERT INTO hero_roles (hero_id, role)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    role=VALUES(role)
        """, (stats["id"], role))

    connection.commit()

print("Dados inseridos")