# dataconnections/postgres.py

import psycopg2
import subprocess
import os
from utils.env import secret, paths, os_path
import inspect

class pgc:

    POSTGRES_HOST       = secret('POSTGRES_HOST')
    POSTGRES_DB         = secret('POSTGRES_DB')
    POSTGRES_USER       = secret('POSTGRES_USER')
    POSTGRES_PASSWORD   = secret('POSTGRES_PASSWORD')

    def get_conn(self):
        try:
            conn = psycopg2.connect(host=self.POSTGRES_HOST, database=self.POSTGRES_DB,
                                    user=self.POSTGRES_USER, password=self.POSTGRES_PASSWORD)
            return conn
        except psycopg2.OperationalError as e:
            print(f"Fehler beim Herstellen der Datenbankverbindung: {e}")
            raise e

    def execute(self, statement, data=None):
        conn = None
        cur = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if data:
                cur.execute(statement, data)
            else:
                cur.execute(statement)
            conn.commit()
        except Exception as e:
            print(f"Fehler bei der Ausführung von Statement: {statement[:100]}...")
            if conn:
                conn.rollback()
            raise e
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
    def query(self, statement, data=None):
        conn = None
        cur = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if data:
                cur.execute(statement, data)
            else:
                cur.execute(statement)
            desc = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [desc, rows]
        except Exception as e:
            print(f"Fehler bei der Ausführung von Query: {statement[:100]}...")
            if conn:
                conn.rollback()
            raise e
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def sql_from_file(self, folder, filename):
        postgres_base_path = paths.get("postgres")
        if not postgres_base_path:
            raise EnvironmentError("PostgreSQL base path ('paths.get(\"postgres\")') is not configured.")

        full_path = os_path(os.path.join(postgres_base_path, "sql", folder, filename))

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"SQL file not found: {full_path}")

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
                statement = " ".join(lines)
                statement = " ".join(statement.split())
            return statement
        except Exception as e:
            print(f"Fehler beim Lesen der SQL-Datei {full_path}: {e}")
            raise

    def execute_with_return(self, statement, data=None):
        conn = None
        cur = None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            if data:
                cur.execute(statement, data)
            else:
                cur.execute(statement)                
            result = cur.fetchone()
            conn.commit()
            return result
        except Exception as e:
            print(f"Fehler bei der Ausführung von execute_with_return: {statement[:100]}...")
            if conn:
                conn.rollback()
            raise e
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def reset(self):
        print(f"--- Starte Datenbank-Reset ---")
        print(f"Host: {self.POSTGRES_HOST}")
        print(f"DB: {self.POSTGRES_DB}")
        print(f"User: {self.POSTGRES_USER}")

        try:
            reset_files_path = os.path.join(paths.get("postgres"), "sql", "reset")
            if not os.path.isdir(reset_files_path):
                 raise FileNotFoundError(f"Reset SQL directory not found: {reset_files_path}")

            sorted_files = sorted([f for f in os.listdir(reset_files_path) if f.lower().endswith('.sql')])
            
            if not sorted_files:
                print("WARNUNG: Keine SQL-Dateien im 'reset'-Verzeichnis gefunden. Überspringe Löschphase.")
            else:
                for file in sorted_files:
                    print(f"Führe aus (Reset): {file}")
                    sql_statement = self.sql_from_file('reset', file)
                    self.execute(sql_statement)

            print("Reset-Phase abgeschlossen. Starte Initialisierung...")
            self.initialize()

        except FileNotFoundError as e:
            print(f"Fehler: SQL-Datei oder Verzeichnis nicht gefunden. {e}")
            raise e
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist während des Resets aufgetreten: {e}")
            raise e
        print(f"--- Datenbank-Reset und Initialisierung abgeschlossen ---")

    def initialize(self):
        print(f"--- Starte Datenbank-Initialisierung ---")
        try:
            init_files_path = os.path.join(paths.get("postgres"), "sql", "init")
            if not os.path.isdir(init_files_path):
                 print(f"WARNUNG: Init SQL directory not found: {init_files_path}. Überspringe Init-Phase.")
            else:
                sorted_files = sorted([f for f in os.listdir(init_files_path) if f.lower().endswith('.sql')])
                
                if not sorted_files:
                    print("WARNUNG: Keine SQL-Dateien im 'init'-Verzeichnis gefunden. Überspringe Init-Phase.")
                else:
                    for file in sorted_files:
                        print(f"Führe aus (Init): {file}")
                        sql_statement = self.sql_from_file('init', file)
                        self.execute(sql_statement)

            list_tt_tables_sql = self.sql_from_file('defaults', 'list_tt_tables.sql')
            list_tt_tables_sql = list_tt_tables_sql.replace('__INSERT__OWNER__HERE__', self.POSTGRES_DB)
            
            tt_tabs_result = self.query(list_tt_tables_sql)
            tt_tables = tt_tabs_result[1] 
            
            print(f"Gefundene 'tt_'-Tabellen zur Erstellung von Views: {len(tt_tables)}")

            for tt_tab_row in tt_tables:
                table_name = tt_tab_row[0] 
                print(f"Erstelle View für Tabelle: {table_name}")
                self.tv_create(table_name)

        except FileNotFoundError as e:
            print(f"Fehler: SQL-Datei oder Verzeichnis für die Initialisierung nicht gefunden. {e}")
            if "list_tt_tables.sql" in str(e):
                print("WARNUNG: Konnte 'list_tt_tables.sql' nicht finden. Views werden nicht erstellt.")
            else:
                raise e
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist während der Initialisierung aufgetreten: {e}")
            raise e
        print(f"--- Datenbank-Initialisierung abgeschlossen ---")

    def as_list_of_json(self, result):
        list_of_dicts = []
        if not isinstance(result, list) or len(result) != 2:
            print("Warnung: Ungültiges Ergebnisformat für as_list_of_json. Erwartet [desc, data].")
            return []
            
        desc, data = result
        
        if not desc or not data:
            return []

        num_columns = len(desc)
        for row in data:
            if len(row) != num_columns:
                print(f"Warnung: Zeile hat {len(row)} Elemente, erwartet wurden {num_columns}. Überspringe Zeile: {row}")
                continue
                
            row_dict = dict(zip(desc, row))
            list_of_dicts.append(row_dict)
        
        return list_of_dicts
        
    def tt_info(self, table):
        if not table.startswith('tt_'):
            print(f"WARNUNG: tt_info wird für keine 'tt_'-Tabelle aufgerufen: {table}")
            return []

        statement = self.sql_from_file('defaults', 'tt_table_info.sql')
        statement = statement.replace('__TABLE__NAME__HERE__', table)
        
        query_result = self.query(statement)
        return self.as_list_of_json(query_result)
    
    def tt_insert(self, table, data):
        if not table.startswith('tt_'):
            raise ValueError("tt_insert kann nur für 'tt_'-Tabellen aufgerufen werden.")

        if not data:
            raise ValueError("Keine Daten zum Einfügen angegeben.")

        num_data_values = len(data)
        value_placeholders = ','.join(['%s'] * num_data_values)
        
        sql_statement = f"INSERT INTO {table} VALUES ({value_placeholders}, now(), True)"
        
        self.execute(sql_statement, data)
        print(f"Daten erfolgreich in '{table}' eingefügt.")

    def tv_create(self, table):
        if not table.startswith('tt_'):
            raise ValueError(f"Die angegebene Tabelle '{table}' ist keine 'tt_'-Tabelle und kann keine View erstellen.")
        
        statement_template = self.sql_from_file('defaults', 'vt_create.sql')
        
        try:
            column_info = self.tt_info(table)
            if not column_info:
                 print(f"WARNUNG: Keine Spalteninformationen für Tabelle '{table}' gefunden. Kann View nicht erstellen.")
                 return
        except Exception as e:
            print(f"Fehler beim Abrufen von Spalteninformationen für Tabelle '{table}': {e}")
            raise

        all_columns = ""
        for col_data in column_info:
            cn = col_data.get('column_name')
            if cn and cn not in ['since_', 'active_']:
                all_columns += f'"{cn}",'
        all_columns = all_columns.rstrip(',')

        pk_columns = ""
        for col_data in column_info:
            cn = col_data.get('column_name')
            if cn and col_data.get('primary_key'):
                pk_columns += f'"{cn}",'
        pk_columns = pk_columns.rstrip(',')
        
        view_name = 'vt_' + table[3:] 

        final_statement = statement_template.replace('__TABLE__NAME__HERE__', f'"{table}"')
        final_statement = final_statement.replace('__VIEW__NAME__HERE__', f'"{view_name}"')
        final_statement = final_statement.replace('__ALL__COLUMNS__HERE__', all_columns)
        final_statement = final_statement.replace('__PK__COLUMNS__HERE__', pk_columns)
        
        try:
            self.execute(final_statement)
            print(f"View '{view_name}' für Tabelle '{table}' erfolgreich erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen der View '{view_name}' für Tabelle '{table}': {e}")
            raise

    def backup_db(self, backup_file):
        try:
            pg_dump_path = r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe"
            
            if not os.path.exists(pg_dump_path):
                raise FileNotFoundError(f"pg_dump.exe nicht gefunden unter: {pg_dump_path}. Bitte Pfad überprüfen oder PostgreSQL Tools installieren und zum PATH hinzufügen.")

            backup_dir = os.path.dirname(backup_file)
            if backup_dir and not os.path.exists(backup_dir):
                os.makedirs(backup_dir, exist_ok=True)

            cmd = [
                pg_dump_path,
                '-h', self.POSTGRES_HOST,
                '-U', self.POSTGRES_USER,
                '-d', self.POSTGRES_DB,
                '-Fc',
                '-f', backup_file
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = self.POSTGRES_PASSWORD

            print(f"Führe Befehl aus: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                print(f"Backup erfolgreich erstellt in: {backup_file}")
            else:
                error_message = result.stderr.strip()
                if not error_message:
                    error_message = "Unbekannter Fehler."
                print(f"Fehler beim Erstellen des Backups (Return Code {result.returncode}):\n{error_message}")
                raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)

        except FileNotFoundError as e:
            print(f"Fehler beim Backup: {e}")
            raise
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist während des Backups aufgetreten: {e}")
            raise

    def restore_db(self, backup_file):
        try:
            pg_restore_path = r"C:\Program Files\PostgreSQL\16\bin\pg_restore.exe"
            
            if not os.path.exists(pg_restore_path):
                raise FileNotFoundError(f"pg_restore.exe nicht gefunden unter: {pg_restore_path}. Bitte Pfad überprüfen oder PostgreSQL Tools installieren und zum PATH hinzufügen.")

            if not os.path.exists(backup_file):
                raise FileNotFoundError(f"Backup-Datei nicht gefunden: {backup_file}")

            cmd = [
                pg_restore_path,
                '-h', self.POSTGRES_HOST,
                '-U', self.POSTGRES_USER,
                '-d', self.POSTGRES_DB,
                '--clean',
                '-Fc',
                backup_file
            ]

            env = dict(os.environ)
            env['PGPASSWORD'] = self.POSTGRES_PASSWORD

            print(f"Führe Befehl aus: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                print(f"Datenbank erfolgreich aus {backup_file} wiederhergestellt.")
            else:
                error_message = result.stderr.strip()
                if not error_message:
                    error_message = "Unbekannter Fehler."
                print(f"Fehler beim Wiederherstellen der Datenbank (Return Code {result.returncode}):\n{error_message}")
                raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)

        except FileNotFoundError as e:
            print(f"Fehler bei der Wiederherstellung: {e}")
            raise
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist während der Wiederherstellung aufgetreten: {e}")
            raise

db = pgc()