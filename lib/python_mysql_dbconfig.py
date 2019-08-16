from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    """ read database config
    :param filename: config file name
    :param section: config section
    return: db dictionary config
    """

    parser = ConfigParser()
    
    # read config file
    parser.read('./config.ini')

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db
