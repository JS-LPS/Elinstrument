from ElInstrument import ElInstrument
import re, time, statistics
from datetime import timedelta, datetime
from threading import Thread
from timeit import default_timer as timer

#__________________________________________________________________________________

class USS_DBS(ElInstrument) : 

    def __init__(self, address = '', timeout = 200, baudrate = 9600):
        #   Permet d'ouvrir la communication avec l'instrument, seule l'adresse est obligatoire sous la forme 'ASRL21::INSTR' (COM21)
        #   Initialise les paramètres d'acquisition par défaut
        ElInstrument.__init__(self, address, timeout, baudrate)
        self.Folder = ""
        self.Samples = 1
        self.Period = 200
        self.Duration = 0
        self.AcqRunning = False
        self.AcqStopped = False
        #    Démarre la tâche de mesure parallèlement au programme principal
        self.thread = Thread(target = self.Measurement, daemon=True)
        self.thread.start()
        #   Réalise une première lecture de l'instrument pour le réveiller
        self.read()
        

    def SetAcquisition(self, samples, period, duration, folder) :
         #  Permet de définir dans l'ordre : le nombre d'échantillions par mesure, la période [ms] entre deux mesures,
         #  La durée [s] totale des mesures (0 = infini, les mesures doivent être stoppées par l'utilisateur)
         #  et le dossier dans lequel sera créé le fichier de mesure
         self.Samples = samples
         self.Period = period
         self.Duration = duration
         self.Folder = folder

    def GetMeasure(self):
         #  Acquiert SAMPLES échantillons, en fait la moyenne pour retourner une mesure
         #  Chaque lecture récupère la chaîne "[signe][data_0][data_1][data_2][data_3][data_4][data_5][data_6][data_7][unité]"
         Datas=[]
         for i in range(self.Samples):
            Data = (re.sub(r"[ g]", '', self.read()))
            #   Retire tous les caractères non numériques
            Datas.append(float(Data))
            #   Transforme la chaîne numérique en nombre et l'insère dans un tableau
            #   Puis retourne la moyenne du tableau
         return statistics.mean(Datas)
    
    def Measurement(self):
        #   Cette fonction est appelée dans une tâche différente du programme principal et boucle tant que le programme principal
        #   est éxécuté (deamon => est détruit quand l'instance du programme principal devient inactive)
        #   'AcqRunning' est un booléen indiquant si l'utilisateur souhaite une acquisition ou non
        #   'AcqStopped' est un booléen permettant l'arrêt de la boucle d'acquisition des mesures
        while(True) :
            if (self.AcqRunning):
                self.AcqStopped = False
                if not self.Folder :
                    #   Vérifie si l'utilisateur a renseigné un dossier dans lequel sauvegarder les mesures,
                    #   si non, stoppe la boucle d'acquisition des mesures 
                    print('OutPut Folder is empty')
                    self.AcqRunning = False
                else :
                    #   Si oui, créé un fichier dont le nom est AAAA-MM-JJ_HH-MM-SS.csv dans le dossier spécifié puis écrit l'en-tête dans le fichier
                    now = datetime.now()
                    FileName = now.strftime("\\%Y-%m-%d_%Hh%Mm%Ss.csv")
                    f = open(self.Folder+FileName, 'w')
                    f.write("ElapsedTime[s],Mass[g]\n")
                    start = timer()
                    #   'start' représente le temps de départ de l'acquisition
                    while (True):
                        Data = self.GetMeasure()
                        #   Récupère une mesure de SAMPLES échantillons
                        elapsedTime = timer()-start
                        #   Récupère le temps écoulé depuis 'start'
                        DataAsString = str(timedelta(seconds=elapsedTime).total_seconds())+','+str(Data)+'\r'
                        print(DataAsString)
                        #   Formatte la chaîne "Temps_écoulé,Mesure\n" et l'affiche dans la console
                        f.write(DataAsString)
                        #   Ajoute la chaîne de mesure dans le fichier
                        if ((self.Duration != 0) and (elapsedTime >= self.Duration)) :
                            #   Si la durée des mesures est dépassée, stoppe l'acquisition et ferme le fichier
                            print("Stopped by Duration")
                            f.close()
                            self.AcqRunning = False
                            break
                        if (self.AcqStopped) :
                            #   Si l'utilisateur demande l'arrêt des mesures, stoppe l'acquisition et ferme le fichier
                            print("Stopped by User")
                            f.close()
                            self.AcqRunning = False
                            break
                        time.sleep(self.Period/1000.0)
                        #   Attends la période configurée avant la prochaine mesure
            else :  time.sleep(0.100)
                    #   Si aucune acquisition est en cours, effectue une attente de 100ms
                    #   Cela évite à la boucle de tourner à une cadence trop élevée et donc de consommer des ressources inutilement
         
    def StartMeasurement(self, isBlocking = False):
            self.AcqStopped = False
            self.AcqRunning = True
            if (isBlocking) : time.sleep(self.Duration+1.0)
        #   L'attente permet à la boucle d'acquisition de faire une dernière mesure puis de s'arrêter 
         
              
    def StopMeasurement(self):
         self.AcqStopped = True
         time.sleep(1.0)
         #   L'attente permet à la boucle d'acquisition de faire une dernière mesure puis de s'arrêter

#__________________________________________________________________________________

# Exemple #

"""

from USS_DBS import USS_DBS
import time

Balance = USS_DBS('ASRL21::INSTR')
    #   DEVICE_ADDR , DEVICE_TIMEOUT , DEVICE_BAUDRATE
    #   Permet d'ouvrir la communication avec l'instrument et initialise les paramètres d'acquisition
    #   Seule l'adresse de l'instrument est obligatoire sous la forme 'ASRL21::INSTR' (COM21)
    
Balance.SetAcquisition(1,100,5,"D:\\Users\\Michel\\Downloads")
    #   SAMPLES/MEASURE , PERIOD[ms] , DURATION[s] , OUTPUT_FOLDER
    #   Attention : il est nécessaire de mettre des doubles antislashs entre chaque sous-dossier

print(Balance.GetMeasure())
    #   Permet de récupérer une mesure unique

Balance.StartMeasurement(isBlocking=True) 
    #   Permet de récupérer une série de mesure selon les paramètres renseignés via .SetAcquisition
    #   True : cette fonction est bloquante bloque et attend jusqu'à la fin de la durée des mesures
    #   False : cette fonction est passante et les mesures sont effectuées en parallèle au programme principal

# ---

    # Exemple pour une durée égale à 0 (infinie), les mesures doivent être arrêtées par l'utilisateur :

Balance.SetAcquisition(1,100,0,"D:\\Users\\Michel\\Downloads")
Balance.StartMeasurement(False)

time.sleep(10)

Balance.StopMeasurement()
    #   Permet de stopper l'acquisition en cours

Balance.close()
    #   Permet de fermer la communication avec l'instrument


"""