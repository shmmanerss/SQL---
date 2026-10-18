import os, sys
if os.name == 'nt':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

from tables.category_table import CategoryTable
from tables.drug_table import DrugTable

class MainApp:
    def __init__(self):
        cat = CategoryTable()
        drug = DrugTable()
        cur = cat.dbconn.conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {drug.table_name()} CASCADE;")
        cur.execute(f"DROP TABLE IF EXISTS {cat.table_name()} CASCADE;")
        cat.dbconn.conn.commit()
        cat.create_table()
        drug.create_table()
        self.cat_table = cat
        self.drug_table = drug
        self.seed_data()

    def seed_data(self):
        if os.path.exists('seed_data.sql'):
            sql = open('seed_data.sql','r',encoding='utf-8').read()
            cur = self.cat_table.dbconn.conn.cursor()
            for stmt in sql.split(';'):
                stmt = stmt.strip()
                if stmt: 
                    try: cur.execute(stmt)
                    except: pass
            self.cat_table.dbconn.conn.commit()

    def run(self):
        while True:
            print("\nГлавное меню:")
            print("1. Категории")
            print("2. Выход")
            choice = input("Выбор: ").strip()
            if choice == '1': self.menu_categories()
            elif choice == '2': break

    def menu_categories(self):
        while True:
            cats = self.cat_table.all()
            print("\nКатегории:")
            for i,c in enumerate(cats,1):
                print(f"{i}. {c[1]}")
            print("a. Добавить  d. Удалить  e. Редактировать  v. Показать  b. Назад")
            choice = input("Выбор: ").strip().lower()
            if choice == 'v':
                num = input("№ категории: ").strip()
                if not num.isdigit():
                    print("Неверный ввод. Введите число.")
                    continue
                num=int(num); cats=self.cat_table.all()
                if 1<=num<=len(cats): self.menu_drugs(cats[num-1])
            elif choice=='a':
                name=input("Название: ").strip()
                if name: self.cat_table.insert_one([name])
            elif choice=='d':
                num = input("№ для удаления: ").strip()
                if not num.isdigit(): print("Неверный ввод"); continue
                num=int(num); cats=self.cat_table.all()
                if 1<=num<=len(cats): self.cat_table.delete_one({'name':cats[num-1][1]})
            elif choice=='e':
                num = input("№ ред.: ").strip()
                if not num.isdigit(): print("Неверный ввод"); continue
                num=int(num); cats=self.cat_table.all()
                if 1<=num<=len(cats):
                    newn=input("Новое название: ").strip()
                    if newn: self.cat_table.update_one({'name':cats[num-1][1]},{'name':newn})
            elif choice=='b': break

    def menu_drugs(self,category):
        cid,cname=category
        while True:
            drugs=self.drug_table.all_by_category(cid)
            print(f"\nЛекарства в категории {cname}:")
            for i,d in enumerate(drugs,1): print(f"{i}. {d[1]} {d[2]} | {d[5]} | {d[6]}₽")
            print("a. Добавить  d. Удалить  e. Редактировать  b. Назад")
            choice = input("Выбор: ").strip().lower()
            if choice=='a':
                name=input("Название: ").strip()
                dosage=input("Дозировка: ").strip()
                volume=input("Объём: ").strip()
                man=input("Производитель: ").strip()
                # prescription True/False
                while True:
                    pr=input("По рецепту? (True/False): ").strip().lower()
                    if pr in ['true','false']: pr_val = pr=='true'; break
                    print("Введите True или False")
                # price
                while True:
                    price_input=input("Цена: ").strip()
                    try: price_val=float(price_input); break
                    except: print("Введите число (e.g., 150.50)")
                self.drug_table.insert_one([name,dosage,volume,man,pr_val,price_val,cid])
            elif choice=='d':
                num=input("№ для удаления: ").strip()
                if not num.isdigit(): print("Неверный ввод"); continue
                num=int(num); drs=self.drug_table.all_by_category(cid)
                if 1<=num<=len(drs): rec=drs[num-1]; self.drug_table.delete_one({'name':rec[1],'dosage':rec[2],'drug_category_id':rec[7]})
            elif choice=='e':
                num=input("№ ред.: ").strip()
                if not num.isdigit(): print("Неверный ввод"); continue
                num=int(num); drs=self.drug_table.all_by_category(cid)
                if 1<=num<=len(drs):
                    rec=drs[num-1]
                    name=input(f"Название ({rec[1]}): ").strip() or rec[1]
                    dosage=input(f"Дозировка ({rec[2]}): ").strip() or rec[2]
                    volume=input(f"Объём ({rec[3]}): ").strip() or rec[3]
                    man=input(f"Производитель ({rec[4]}): ").strip() or rec[4]
                    while True:
                        pr=input(f"По рецепту ({rec[5]}) [True/False]: ").strip().lower()
                        if pr in ['true','false']: pr_val=pr=='true'; break
                        print("Введите True или False")
                    while True:
                        pi=input(f"Цена ({rec[6]}): ").strip()
                        try: price_val=float(pi); break
                        except: print("Введите число")
                    self.drug_table.update_one({'name':rec[1],'dosage':rec[2],'drug_category_id':rec[7]},
                                               {'name':name,'dosage':dosage,'volume_amount':volume,'manufacturer':man,'prescription_required':pr_val,'price':price_val})
            elif choice=='b': break

if __name__=='__main__':
    MainApp().run()
