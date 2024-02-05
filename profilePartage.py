import pymysql
from db_config import db_config
class profil:
    def profiles(self, author, id, ctx,z):
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                cursor.execute("SELECT score FROM utilisateurs WHERE idUtilisateur = %s", (id,))
                result = cursor.fetchone()

                if result is None:
                    return "Il te faut un profil. Utilise ^^NP pour en créer un."
                else:
                    current_score = result['score']

                    if z == 1:
                        return f"Ton score est : {current_score}"
                    else:
                        # Sinon, mettre à jour le score de l'utilisateur
                        new_score = current_score + z
                        cursor.execute("UPDATE utilisateurs SET score = %s WHERE idUtilisateur = %s",
                                       (new_score, id))
                        connection.commit()
                        return "Score mis à jour avec succès."
        except pymysql.MySQLError as e:
            print(e)
            return "Une erreur est survenue lors de l'accès à la base de données."
        finally:
            if connection:
                connection.close()

    def modif(self, author, id, ctx):
        with open('profile.txt', 'a') as f:
            f.write('\n\n')
            f.write(str(id))
            f.write("\n", )
            f.write(str(author))
            f.write('\n0')