import pymysql
from db_config import db_config

weapon_types = [
    "Classic", "Shorty", "Frenzy", "Ghost", "Sheriff",
    "Stinger", "Spectre", "Bucky", "Judge",
    "Bulldog", "Guardian", "Phantom", "Vandal",
    "Marshal", "Operator",
    "Ares", "Odin",
    "Melee","Knife"
]

def update_weapon_type():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT uuid, displayName FROM weapons_skins")
        weapons_skins = cursor.fetchall()
        print(weapons_skins)

        for weapon_skin in weapons_skins:
            uuid = weapon_skin['uuid']
            displayName = weapon_skin['displayName']
            updated = False
            for weapon_type in weapon_types:
                if weapon_type in displayName:
                    update_query = "UPDATE weapons_skins SET weaponType = %s WHERE uuid = %s"
                    cursor.execute(update_query, (weapon_type, uuid))
                    print(f"Updated {displayName} with {weapon_type}")
                    updated = True
                    break

        connection.commit()
        print("Mise à jour terminée.")
    except Exception as e:
        print(f"Erreur : {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    update_weapon_type()
