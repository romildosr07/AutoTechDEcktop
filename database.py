import sqlite3


def open_connection(database_name):
    conn = sqlite3.connect(database_name)
    return conn


def close_connection(conn):
    conn.close()


class Database:
    def __init__(self, database_name):
        self.conn = open_connection(database_name)
        self.cursor = self.conn.cursor()

    # Tabela de Peças
    def create_part_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS part(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quantity INTEGER,
            name TEXT NOT NULL,
            value REAL
        );               
        """)

    # Tabelas de Serviço
    def create_service_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS service(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL
        );               
        """)

    # Tabela ordem de serviço
    def create_service_order_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_order(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            plate TEXT NOT NULL,
            kms TEXT
        );          
        """)

    # Tabela ordem de serviço pecas
    def create_service_order_part_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_order_part(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_order_id INTEGER,
            part_id INTEGER,
            FOREIGN KEY (service_order_id) REFERENCES service_order(id)
            FOREIGN KEY (part_id) REFERENCES part(id)
        );          
        """)

    # Tabela ordem de serviço pecas
    def create_service_order_service_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_order_service(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_order_id  INTEGER,
            service_id  INTEGER,
            FOREIGN KEY (service_order_id) REFERENCES service_order(id)
            FOREIGN KEY (service_id) REFERENCES service(id)
        );          
        """)


class PartControl:
    def __init__(self, database):
        self.conn = open_connection(database)
        self.cursor = self.conn.cursor()

    def create_part(self, quantity, name, value):
        self.cursor.execute("INSERT INTO part(quantity, name, value) VALUES(?, ?, ?)", (quantity, name, value))
        self.conn.commit()

    def read_all_part(self):
        self.cursor.execute("SELECT * FROM  part")
        return self.cursor.fetchall()

    def read_part_by_id(self, part_id):
        self.cursor.execute("SELECT * FROM part WHERE id=?", (part_id,))
        return self.cursor.fetchone()

    def update_part(self, part_id, name=None, value=None):
        update_query = "UPDATE part SET"
        update_data = []

        if name:
            update_query += " name=?,"
            update_data.append(name)

        if value:
            update_query += " value=?,"
            update_data.append(value)


        # Remova a vírgula extra no final da consulta UPDATE
        update_query = update_query.rstrip(',')

        # Adicione a cláusula WHERE para a condição específica do carro
        update_query += " WHERE id=?"

        # Adicione o ID do carro à lista de dados
        update_data.append(part_id)

        self.cursor.execute(update_query, tuple(update_data))
        self.conn.commit()

    def delete_part(self, part_id):
        self.cursor.execute("DELETE FROM part WHERE id=?", (part_id,))
        self.conn.commit()

    def truncate_part(self):
        try:
            self.cursor.execute(f'DELETE FROM  part;')

            self.conn.commit()
            print(f'Tabela part truncada com sucesso.')
        except sqlite3.Error as e:
            print(f"Erro ao truncar a tabela part: {e}")

        finally:
            if self.conn:
                self.conn.close()


class ServiceControl:
    def __init__(self, database):
        self.conn = open_connection(database)
        self.cursor = self.conn.cursor()

    def create_service(self, name, value):
        self.cursor.execute("INSERT INTO service(name, value) VALUES(?, ?)", (name, value))
        self.conn.commit()

    def read_all_service(self):
        self.cursor.execute("SELECT * FROM service")
        return self.cursor.fetchall()

    def read_service_by_id(self, service_id):
        self.cursor.execute("SELECT * FROM service WHERE id=?", (service_id,))
        return self.cursor.fetchone()

    def update_service(self, service_id, name=None, value=None):
        update_query = "UPDATE service SET"
        update_data = []

        if name:
            update_query += " name=?,"
            update_data.append(name)

        if value:
            update_query += " value=?,"
            update_data.append(value)


        # Remova a vírgula extra no final da consulta UPDATE
        update_query = update_query.rstrip(',')

        # Adicione a cláusula WHERE para a condição específica do carro
        update_query += " WHERE id=?"

        # Adicione o ID do carro à lista de dados
        update_data.append(service_id)

        self.cursor.execute(update_query, tuple(update_data))
        self.conn.commit()

    def delete_service(self, service_id):
        self.cursor.execute("DELETE FROM service WHERE id=?", (service_id,))
        self.conn.commit()

    def truncate_service(self):
        try:
            self.cursor.execute(f'DELETE FROM  service;')

            self.conn.commit()
            print(f'Tabela service truncada com sucesso.')
        except sqlite3.Error as e:
            print(f"Erro ao truncar a tabela service: {e}")

        finally:
            if self.conn:
                self.conn.close()


class ServiceOrderControl:
    def __init__(self, database_name):
        self.conn = open_connection(database_name)
        self.cursor = self.conn.cursor()

    def create_service_order(self, name, plate, kms):
        self.cursor.execute("INSERT INTO service_order (name, plate, kms) VALUES(?,?,?)", (name, plate, kms))
        self.conn.commit()

    def read_all_service_order(self):
        self.cursor.execute("SELECT * FROM  service_order")
        return self.cursor.fetchall()

    def read_service_order_by_id(self, service_order_id):
        self.cursor.execute("SELECT * FROM service_order WHERE id=?", (service_order_id,))
        return self.cursor.fetchone()

    def update_service_order(self, service_order_id, car_id=None):
        update_query = "UPDATE service_order SET"
        update_data = []

        if car_id:
            update_query += " name=?,"
            update_data.append(car_id)

        # Remova a vírgula extra no final da consulta UPDATE
        update_query = update_query.rstrip(',')

        # Adicione a cláusula WHERE para a condição específica do carro
        update_query += " WHERE id=?"

        # Adicione o ID do carro à lista de dados
        update_data.append(service_order_id)

        self.cursor.execute(update_query, tuple(update_data))
        self.conn.commit()

    def delete_service_order(self, service_order_id):
        self.cursor.execute("DELETE FROM service_order WHERE id=?", (service_order_id,))
        self.conn.commit()

    def truncate_service_order(self):
        try:
            self.cursor.execute(f'DELETE FROM  service_order;')

            self.conn.commit()
            print(f'Tabela service_order truncada com sucesso.')
        except sqlite3.Error as e:
            print(f"Erro ao truncar a tabela service_order: {e}")

        finally:
            if self.conn:
                self.conn.close()


class ServiceOrderPartControl:
    def __init__(self, database_name):
        self.conn = open_connection(database_name)
        self.cursor = self.conn.cursor()

    def create_service_order_part(self, service_order_id, part_id):
        self.cursor.execute(
            "INSERT INTO service_order_part (service_order_id, part_id) VALUES(?)", (service_order_id, part_id))
        self.conn.commit()

    def read_all_service_order_part(self):
        self.cursor.execute("SELECT * FROM  service_order_part")
        return self.cursor.fetchall()

    def read_service_order_part_by_id(self, service_order_part_id):
        self.cursor.execute("SELECT * FROM service_order_part WHERE id=?", (service_order_part_id,))
        return self.cursor.fetchone()

    def update_service_order_part(self, service_order_part_id, service_order_id=None, part_id=None):
        update_query = "UPDATE service_order_part SET"
        update_data = []

        if service_order_id:
            update_query += " service_order_id=?,"
            update_data.append(service_order_id)

        if part_id:
            update_query += " part_id=?,"
            update_data.append(part_id)

        # Remova a vírgula extra no final da consulta UPDATE
        update_query = update_query.rstrip(',')

        # Adicione a cláusula WHERE para a condição específica do carro
        update_query += " WHERE id=?"

        # Adicione o ID do carro à lista de dados
        update_data.append(service_order_part_id)

        self.cursor.execute(update_query, tuple(update_data))
        self.conn.commit()

    def delete_service_order(self, service_order_part_id):
        self.cursor.execute("DELETE FROM service_order_part WHERE id=?", (service_order_part_id,))
        self.conn.commit()


class ServiceOrderServiceControl:
    def __init__(self, database_name):
        self.conn = open_connection(database_name)
        self.cursor = self.conn.cursor()

    def create_service_order_service(self, service_order_id, service_id):
        self.cursor.execute(
            "INSERT INTO service_order_service (service_order_id, service_id) VALUES(?)", (service_order_id, service_id))
        self.conn.commit()

    def read_all_service_order_service(self):
        self.cursor.execute("SELECT * FROM  service_order_service")
        return self.cursor.fetchall()

    def read_service_order_service_by_id(self, service_order_service_id):
        self.cursor.execute("SELECT * FROM service_order_service WHERE id=?", (service_order_service_id,))
        return self.cursor.fetchone()

    def update_service_order_service(self, service_order_service_id, service_order_id=None, service_id=None):
        update_query = "UPDATE service_order_service SET"
        update_data = []

        if service_order_id:
            update_query += " service_order_id=?,"
            update_data.append(service_order_id)

        if service_id:
            update_query += " service_id=?,"
            update_data.append(service_id)

        # Remova a vírgula extra no final da consulta UPDATE
        update_query = update_query.rstrip(',')

        # Adicione a cláusula WHERE para a condição específica do carro
        update_query += " WHERE id=?"

        # Adicione o ID do carro à lista de dados
        update_data.append(service_order_service_id)

        self.cursor.execute(update_query, tuple(update_data))
        self.conn.commit()

    def delete_service_order_service(self, service_order_service_id):
        self.cursor.execute("DELETE FROM service_order_service WHERE id=?", (service_order_service_id,))
        self.conn.commit()

