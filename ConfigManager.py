import os, ConfigParser

class ConfigManager:
    def __init__(self, application):
        self.cfg = ConfigParser.RawConfigParser()
        self.conf_dir = os.path.join(os.getenv('XDG_CONFIG_HOME',
            os.path.join(os.getenv('HOME'), '.config')), application)
        self.conf_file = os.path.join(self.conf_dir, 'config')
        if os.path.exists(self.conf_file):
            self.cfg.read(conf_file)
        else:
            self.create_conf()

    def create_conf():
        if not os.path.exists(self.conf_dir):
            os.mkdir(self.conf_dir)

    def read_conf():
        pass

