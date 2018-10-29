from settings import ENV

def resolver_func(attribute_name):
    template = ENV.get_template('resolver.txt')
    return template.render(attribute_name=attribute_name)
