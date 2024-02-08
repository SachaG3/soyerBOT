import requests
import pymysql
from db_config import db_config


def fetch_api_data():
    """Fonction pour récupérer les données de l'API."""
    url = "https://valorant-api.com/v1/weapons/skins"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("Erreur lors de la récupération des données de l'API")
        return None


def save_data_to_db(data):
    """Fonction pour sauvegarder les données dans la base de données."""
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        for item in data:
            # Vous devrez peut-être adapter cette commande SQL en fonction de la structure de votre base de données
            sql = "INSERT INTO weapons_skins (uuid, displayName, themeUuid, contentTierUuid, displayIcon, wallpaper, assetPath) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
            item['uuid'], item['displayName'], item['themeUuid'], item['contentTierUuid'], item['displayIcon'],
            item['wallpaper'], item['assetPath']))

            # Pour les chromas
            for chroma in item['chromas']:
                # Insérer les données des chromas - Adaptez cette commande SQL également
                sql_chroma = "INSERT INTO chromas (uuid, displayName, displayIcon, fullRender, swatch, streamedVideo, assetPath, weaponSkinUuid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_chroma, (
                chroma['uuid'], chroma['displayName'], chroma['displayIcon'], chroma['fullRender'], chroma['swatch'],
                chroma['streamedVideo'], chroma['assetPath'], item['uuid']))

            # Pour les niveaux
            for level in item['levels']:
                # Insérer les données des niveaux
                sql_level = "INSERT INTO levels (uuid, displayName, levelItem, displayIcon, streamedVideo, assetPath, weaponSkinUuid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_level, (
                level['uuid'], level['displayName'], level['levelItem'], level['displayIcon'], level['streamedVideo'],
                level['assetPath'], item['uuid']))
        connection.commit()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        connection.rollback()
    finally:
        connection.close()


# Programme principal
if __name__ == "__main__":
    data = fetch_api_data()
    if data is not None:
        save_data_to_db(data)
