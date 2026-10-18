import yaml
import psycopg2

class DbConn:
    def __init__(self):
        cfg = yaml.safe_load(open('config.yaml'))
        self.prefix = cfg.get('dbtableprefix', '')
        self.conn = psycopg2.connect(
            dbname   = cfg['dbname'],
            user     = cfg['user'],
            password = cfg['password'],
            host     = cfg.get('host', 'localhost'),
            port     = cfg.get('port', 5432)
        )

    def __del__(self):
        if getattr(self, 'conn', None):
            self.conn.close()
