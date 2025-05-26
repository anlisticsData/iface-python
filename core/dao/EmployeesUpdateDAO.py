from core.ConexaoMySQL import MySQLConnection


class EmployeesUpdateDAO:
    @staticmethod
    def create(update_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO employees_update (
                    operacao, codigo_funcionario, data_bloqueio_liberacao,
                    hash_64_dig_1, hash_64_dig_2, numero_cracha,
                    codigo_bloqueio, codigoObra, employees_code, deleted_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                update_data.get('operacao'),
                update_data.get('codigo_funcionario'),
                update_data.get('data_bloqueio_liberacao'),
                update_data.get('hash_64_dig_1'),
                update_data.get('hash_64_dig_2'),
                update_data.get('numero_cracha'),
                update_data.get('codigo_bloqueio'),
                update_data.get('codigoObra'),
                update_data.get('employees_code'),
                update_data.get('deleted_at')
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def read(update_id):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees_update WHERE id = %s", (update_id,))
            return cursor.fetchone()
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def update(update_id, updated_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            fields = ', '.join(f"{key} = %s" for key in updated_data.keys())
            values = list(updated_data.values()) + [update_id]
            sql = f"UPDATE employees_update SET {fields} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def delete(update_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees_update WHERE id = %s", (update_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)
