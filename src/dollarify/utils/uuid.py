from uuid import uuid4


def generate(dashes = False):
    uuid_str = str(uuid4())
    if not dashes:
        uuid_str.replace('-', '')
    return uuid_str


def uuid_include_dashes(uuid_str):
    uuid_str = uuid_str.replace('-', '')
    uuid_dashes = uuid_str[:8] + '-' + uuid_str[8:12] + '-' + uuid_str[12:16] + '-' + uuid_str[16: 20] + '-'+ uuid_str[20:]
    return ''.join(uuid_dashes)