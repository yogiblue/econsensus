VERSION = (0, 4, 5)

def get_version():
    return '.'.join([str(subversion) for subversion in VERSION])
