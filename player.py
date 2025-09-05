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
        CREATE TABLE IF NOT EXISTS player (
                id INT PRIMARY KEY,
                rank_tier INT,
                steam_id VARCHAR(100),
                last_login VARCHAR(100),
                win VARCHAR(100),
                lose VARCHAR(100)
            )
    """)

    players = get_opendota("players/52328004")
    wl = get_opendota("players/52328004/wl")

    profile = players.get("profile", {})
    rank_tier = players.get("rank_tier")
    steam_id = profile.get("steamid")
    last_login = profile.get("last_login")
    account_id = profile.get("account_id")
    win = wl.get("win")
    lose = wl.get("lose")


    for player in players:
        cursor.execute("""
            INSERT INTO player (id, rank_tier, steam_id, last_login, win, lose)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                rank_tier=VALUES(rank_tier),
                steam_id=VALUES(steam_id),
                last_login=VALUES(last_login),
                win=VALUES(win),
                lose=VALUES(lose)
    """, (account_id, rank_tier, steam_id, last_login, win, lose))
        
    connection.commit()
print("Dados inseridos")