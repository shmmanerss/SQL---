from dbtable import DbTable

class DrugTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + 'drugs'
    def columns(self):
        return {
            'id':                    ['serial', 'PRIMARY KEY'],
            'name':                  ['varchar(255)', 'NOT NULL'],
            'dosage':                ['varchar(50)',  'NOT NULL'],
            'volume_amount':         ['varchar(50)',  'NOT NULL'],
            'manufacturer':          ['varchar(255)', 'NOT NULL'],
            'prescription_required': ['boolean',      'NOT NULL'],
            'price':                 ['numeric(10,2)', 'NOT NULL'],
            'drug_category_id':      ['integer',       'NOT NULL', 'REFERENCES ' + self.dbconn.prefix + 'drug_categories(id) ON DELETE CASCADE']
        }
    def primary_key(self):
        return ['name', 'dosage']
    def column_names(self):
        return ['id', 'name', 'dosage', 'volume_amount', 'manufacturer', 'prescription_required', 'price', 'drug_category_id']
    def column_names_without_id(self):
        return ['name', 'dosage', 'volume_amount', 'manufacturer', 'prescription_required', 'price', 'drug_category_id']
    def find_by_position(self, num):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY name, dosage LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (num-1,))
        return cur.fetchone()
    def all_by_category(self, cat_id):
        sql = f"SELECT * FROM {self.table_name()} WHERE drug_category_id=%s ORDER BY name, dosage"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cat_id,))
        return cur.fetchall()
