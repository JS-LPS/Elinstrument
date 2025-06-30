
from USS_DBS import USS_DBS
import time

Balance = USS_DBS('ASRL5::INSTR')
    #   DEVICE_ADDR , DEVICE_TIMEOUT , DEVICE_BAUDRATE
    #   Permet d'ouvrir la communication avec l'instrument et initialise les paramètres d'acquisition
    #   Seule l'adresse de l'instrument est obligatoire sous la forme 'ASRL21::INSTR' (COM21)
    
Balance.SetAcquisition(1,100,5,"C:\\Users\\frest\\Downloads\\_Measures")
    #   SAMPLES/MEASURE , PERIOD[ms] , DURATION[s] , OUTPUT_FOLDER
    #   Attention : il est nécessaire de mettre des doubles antislashs entre chaque sous-dossier

print('Single measure = ',Balance.GetMeasure())
    #   Permet de récupérer une mesure unique

Balance.StartMeasurement(isBlocking=True) 
    #   Permet de récupérer une série de mesure selon les paramètres renseignés via .SetAcquisition
    #   True : cette fonction est bloquante bloque et attend jusqu'à la fin de la durée des mesures
    #   False : cette fonction est passante et les mesures sont effectuées en parallèle au programme principal

# ---

    # Exemple pour une durée égale à 0 (infinie), les mesures doivent être arrêtées par l'utilisateur :

Balance.SetAcquisition(1,100,0,"C:\\Users\\frest\\Downloads\\_Measures")
Balance.StartMeasurement(False)

time.sleep(10)

Balance.StopMeasurement()
    #   Permet de stopper l'acquisition en cours

print('Single measure #2 = ',Balance.GetMeasure())

Balance.close()
    #   Permet de fermer la communication avec l'instrument
