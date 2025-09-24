from datetime import datetime

from utils.env import paths

def qwlog(message):
    try:
        qwlog_write(message)
    except:
        try:
            import os
            if not os.path.exists(paths.get('logs')):
                os.makedirs(paths.get('logs'))
            qwlog_write(message)
        except:
            raise ValueError('Error when writing to logs.')
            
def qwlog_write(message):
    file1 = open(paths.get('logs') + '/qwlog.txt', 'a')
    file1.write(str(datetime.now()) + " " + message + '\n')
    file1.close()