from configparser import ConfigParser


def load(file, section):
    """
    file: path or relative file path (to the package).
    """
    file = str(file)
    parser = ConfigParser()
    parser.read(file)
    key_values = {}
    if not parser.has_section(section):
        raise ValueError(f'The section {section} does not exists in the {file} file.')
    
    for k, v in parser.items(section):
        key_values[k] = v
    return key_values
