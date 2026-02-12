try:
    from besdapp.model import CustomUser
    print("LECTURE REUSSIE : Python voit la classe CustomUser !")
except Exception as e:
    print(f"ERREUR DE LECTURE : {e}")