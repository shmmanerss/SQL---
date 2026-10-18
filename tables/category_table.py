from dbtable import DbTable

class CategoryTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + 'drug_categories'
    def columns(self):
        return {
            'id':   ['serial', 'PRIMARY KEY'],
            'name': ['varchar(255)', 'NOT NULL', 'UNIQUE']
        }
    def primary_key(self):
        return ['name']
    def column_names(self):
        return ['id', 'name']
    def column_names_without_id(self):
        return ['name']
    def find_by_position(self, num):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY name LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (num-1,))
        return cur.fetchone()
