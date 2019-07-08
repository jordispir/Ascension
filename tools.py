import os 

def obtenPath(directorio):
    pathFicheroScript = os.path.realpath(__file__)
    directorioTrabajo = os.path.dirname(pathFicheroScript)
    pathRecurso = os.path.join(directorioTrabajo, directorio)
    
    return pathRecurso

def obtenPathDeRecurso(directorio, elemento):
    path = obtenPath(directorio)
    
    return os.path.join(path, elemento)
