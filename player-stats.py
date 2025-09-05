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
        CREATE TABLE IF NOT EXISTS player_stats(
            id INT,
            hero_id INT,
            games INT,
            win INT,
            with_games INT,
            PRIMARY KEY (id, hero_id),
            FOREIGN KEY (id) REFERENCES player(id)
        )
    """)

    account_id = 52328004
    heroes = get_opendota("players/52328004/heroes")

    for hero in heroes:
        for games in hero:
            hero_id = hero.get("hero_id")
            games = hero.get("games")
            win = hero.get("win")
            with_games = hero.get("with_games")

            cursor.execute("""
                INSERT INTO player_stats (id, hero_id, games, win, with_games)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    hero_id=VALUES(hero_id),
                    games=VALUES(games),
                    win=VALUES( win),
                    with_games=VALUES(with_games)
        """, (account_id, hero_id, games, win, with_games))
        
    connection.commit()

print("Dados inseridos")