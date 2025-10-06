# 🧠 Dota2API

A **Python** project that connects to the **[OpenDota API](https://docs.opendota.com/)** and stores detailed **hero** and **player** data in a **MySQL** database.  
The goal is to build a local dataset with up-to-date stats for future analytics or dashboards.

---

## 📋 Features

- Automatically creates MySQL tables:
  - `heroes`, `hero_stats`, `hero_roles`
  - `player`, `player_stats`
- Fetches data from the OpenDota API:
  - Hero statistics (winrate, pro picks, bans, etc.)
  - Player information (rank, wins, losses, last login)
  - Player-specific hero performance (games with, against, and total)
- Inserts data into MySQL with **duplicate key handling** (`ON DUPLICATE KEY UPDATE`)

---

## ⚙️ Technologies Used

- **Python 3.x**
- **MySQL**
- **OpenDota API**
- Libraries:
  - `requests`
  - `pymysql`
  - `python-dotenv`
  - `os`

