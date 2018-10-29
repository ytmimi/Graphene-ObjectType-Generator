from settings import ENV

def add_imports(*imports):
    template = ENV.get_template('imports.txt')
    return template.render(imports=imports).strip()
