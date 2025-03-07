# importer les variables d'environement

# déclarer la db en fonction de ENVIRONMENT et DATABASE_URL

# initialiser la base de données (créer les tableaux)

# déclarer les schémas Pydantic

# déclarer l'app
# ajouter les middlewares
# ajouter un vérificateur de session

# ajouter les routes de l'API

# run l'app en fonction de ENVIRONMENT

from logic.OAuth2 import OA2

t = OA2().get_user_data_from_code("d9mPp5VmBYeVhT68eQQ7EjXfSoPm1V")
print(t)