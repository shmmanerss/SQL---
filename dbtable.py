from dbconn import DbConn
import psycopg2

class DbTable:
    def __init__(self):
        self.dbconn = DbConn()
    def table_name(self):
        raise NotImplementedError
    def columns(self):
        raise NotImplementedError
    def primary_key(self):
        raise NotImplementedError
    def column_names(self):
        return list(self.columns().keys())
    def column_names_without_id(self):
        return [c for c in self.column_names() if c != 'id']
    def create_table(self):
        cols = [f"{name} {' '.join(attrs)}" for name, attrs in self.columns().items()]
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name()} (" + ", ".join(cols) + ");"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
    def insert_one(self, vals):
        cols = self.column_names_without_id()
        placeholders = ["%s"] * len(cols)
        sql = f"INSERT INTO {self.table_name()}(" + ", ".join(cols) + ") VALUES(" + ", ".join(placeholders) + ")"
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, vals)
            self.dbconn.conn.commit()
        except psycopg2.IntegrityError as e:
            self.dbconn.conn.rollback()
            print("Ошибка целостности:", e)
    def all(self):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY " + ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    def delete_one(self, key_vals):
        cond = [f"{k}=%s" for k in key_vals]
        sql = f"DELETE FROM {self.table_name()} WHERE " + " AND ".join(cond)
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, list(key_vals.values()))
            self.dbconn.conn.commit()
        except psycopg2.IntegrityError as e:
            self.dbconn.conn.rollback()
            print("Ошибка удаления:", e)
    def update_one(self, key_vals, new_vals):
        sc = [f"{k}=%s" for k in new_vals]
        cond = [f"{k}=%s" for k in key_vals]
        sql = f"UPDATE {self.table_name()} SET " + ", ".join(sc) + " WHERE " + " AND ".join(cond)
        cur = self.dbconn.conn.cursor()
        try:
            cur.execute(sql, list(new_vals.values()) + list(key_vals.values()))
            self.dbconn.conn.commit()
        except psycopg2.IntegrityError as e:
            self.dbconn.conn.rollback()
            print("Ошибка обновления:", e)
