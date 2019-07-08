<<<<<<< HEAD
import os 
=======
import os
>>>>>>> 7a412e8adb0c370d9ea97c45a434cc17ee088c0e

def obtenPath(directorio):
    pathFicheroScript = os.path.realpath(__file__)
    directorioTrabajo = os.path.dirname(pathFicheroScript)
    pathRecurso = os.path.join(directorioTrabajo, directorio)
<<<<<<< HEAD
    
    return pathRecurso

def obtenPathDeRecurso(directorio, elemento):
    path = obtenPath(directorio)
    
=======

    return pathRecurso


def obtenPathDeRecurso(directorio, elemento):
    path = obtenPath(directorio)

>>>>>>> 7a412e8adb0c370d9ea97c45a434cc17ee088c0e
    return os.path.join(path, elemento)
