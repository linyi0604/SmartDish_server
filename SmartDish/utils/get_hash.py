from hashlib import sha1

def get_hash(str ,salt = None):
    '''取字符串散列值'''
    str = 'zxc' + str + 'qwe'
    if salt is not None:
        str += salt
    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()