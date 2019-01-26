from unidecode import unidecode


def slugify(name):
    name_url = unidecode(name).lower().replace(' ', '-')
    return name_url
