def imports(*args):
    '''args: properly formated import strings'''
    return '\n'.join(args)

def to_py_file(full_file_name, mode, objectType):
    '''
    writes the contents of objectType to a file
    '''
    with open(full_file_name, mode) as f:
        if mode == 'w':
            f.write(add_imports('import graphene'))
            f.write('\n\n')
        f.write(objectType)
        f.write('\n\n')
    return f
