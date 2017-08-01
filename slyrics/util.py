import pkg_resources

def get_data_filename(filename):
    return pkg_resources.resource_filename(__name__, filename)

def die(msg=None, code=0):
    if msg:
        print(msg)
    exit(code)
