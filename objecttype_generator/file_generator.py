def add_imports(*args):
    '''args: properly formated import strings'''
    #consider checking import strings for proper formating
    return '\n'.join(args)

def to_py_file(full_file_name, objecttype, mode='w', include_imports=True, import_list=[]):
    '''
    writes the contents of objectType to a file
    full_file_name: path to save the .py file
    objecttype: list of strings defining objecttype definitions
    mode: how to write to a file. valid options are 'a' or 'w'
    imports: a boolean specifying weather to include imports in the file
    import_list: list of additional imports. By default, graphene will always be imported,
        and need not be included in import_list.
    '''
    #check mode
    if mode != 'w' and mode != 'a':
        raise ValueError('Mode must be set to either a or w.')
    # check imports for graphene
    if include_imports and 'import graphene' not in import_list:
        import_list = ['import graphene'] + import_list
    #check that a .py file was given.
    if full_file_name[-3:] != '.py':
        raise ValueError('Please supply the path to a .py file.')

    with open(full_file_name, mode) as f:
        if mode == 'w' and include_imports:
            f.write(add_imports(*import_list))
            f.write('\n\n')
        for object in objecttype:
            f.write(object)
            f.write('\n\n')
