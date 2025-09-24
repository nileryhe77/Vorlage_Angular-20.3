import os
import platform

def os_path(path):
    # Hier wird die Plattform überprüft und der Pfad entsprechend formatiert
    if 'linux' in platform.platform().lower():
        return path.replace("\\", "/")
    if 'windows' in platform.platform().lower():
        return path
    return path  # Wenn es ein anderes OS gibt, einfach den Pfad zurückgeben

# Verbessertes paths-Dictionary
paths = {
    "base" : os_path(os.getcwd() + '\\'),
    "postgres" : os_path(os.getcwd().split('/python')[0].split('\\python')[0] + '\\postgres\\'),
    "logs" : os_path(os.getcwd() + '\\logs\\')  # Füge den Logs-Pfad hinzu
}

def secret(name):
    secret = 'not found'
    if name in list(os.environ):
        secret = os.environ[name]
    else:
        path = paths.get('base')
        file = '.env'
        if file in os.listdir(path):
            f = open(path + file, "r")
            lines = f.readlines()
            for line in lines:
                if line.split('=')[0] == name:
                    secret = line.split('=')[1].replace('\n','')
            f.close()
    if secret == 'not found':
        raise ValueError('Secret ' + name + ' could not be found.')
    return secret
