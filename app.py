#Importálom a platform modult, a rendszer adatok lekérése miatt
import platform
# Importálom a subprocess modult, a binary file lefuttatása miatt
import subprocess
# Importálom a Flask modult
from flask import Flask, url_for, render_template, request
# Importálom a secure_filename modult
from werkzeug.utils import secure_filename
# Importálom a copy modult, a file adatok átmásolásához
import copy
# Importálom a datetime modult, a fileok mentésének a megkülömböztetéséhez
from datetime import datetime


# Lekérem a rendszer architecture-et, ezt kisbetűssé alaktítom
systemArchitecture = platform.system().lower()

#Lekérem a rendszer típust, és átalaktom a megfelelő formátumba
machineArchitecture = platform.machine() == "AMD64" and "amd64" or "386"

#Definiálom a binary file nevét későbbi használatra
binaryFilename = "lexunit-exercise-"+systemArchitecture+"-"+machineArchitecture



# Létrehozom a Flask servert
app = Flask(__name__)

# Megadom neki a szerver root mappáját, POST, GET methodokat is fogadjon
@app.route("/", methods=['POST','GET'])
def index():
    if request.method == "POST":
        # POSTolás esetén csekkolom, hogy jó file extensiont kapotte a server
        file = request.files['content']

        if not "." in file.filename or not "json" in file.filename.split(".")[1].lower():
            return render_template('base.html', textResult="Hibás file név")

        # Csekkolom, hogy kapotte tresholdot a szerver
        treshold = request.form['treshold']
        if treshold == "" or treshold == None:
            return render_template('base.html', textResult="Hibás különbözet érték")

        #Leformázom a tresholdot
        treshold = str(float(treshold))

        #Elmentem a filet
        date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        saveFile = open("uploads/"+secure_filename(file.filename)+date, "a")
        fileData = file.read()
        saveFile.write(copy.copy(fileData).decode("utf-8"))
        saveFile.close()

        #Lekérem a file tartalmát, azt átformázom a megfelelő formátumra
        fileConcent = fileData.replace(b'\n', b'').replace(b'\t', b'').decode("utf-8").replace(' ', '').replace("'", '"')
        
        #Lefuttatom subprocessben a binary filet, megvárom még az lefut
        popen = subprocess.Popen("./binaries/"+binaryFilename+" '"+fileConcent+"' "+treshold, stdout=subprocess.PIPE, shell=True)
        popen.wait()
        

        #Eredmény lekérésre, formázása
        output = popen.stdout.read().decode("utf-8").split("\n")
        return render_template('base.html', result=output)
    else:
        return render_template('base.html') 


# Elindítom a Flask servert
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")