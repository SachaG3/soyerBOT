import pymysql
from repository import utilisateurRepository
from db_config import db_config
class profil:
    def profiles(self, author, id, ctx, z):
        try:
            user = utilisateurRepository.get_user_by_idUtilisateur(id)
            current_score = user['score']
            if z == 1:
                return f"Ton score est : {current_score}"
            else:
                    return "Score mis à jour avec succès."
        except Exception as e:
            print(e)
            return "Une erreur est survenue lors de l'accès à la base de données."