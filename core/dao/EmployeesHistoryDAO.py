from core.ConexaoMySQL import MySQLConnection


class EmployeesHistoryDAO:
    @staticmethod
    def create(history_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO employees_history (
                    employees_iface_id, employees_remote_code,
                    remote_event_code, remote_uud, fullname,
                    company_join, readding, recordType,
                    process, upload
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                history_data.get('employees_iface_id'),
                history_data.get('employees_remote_code'),
                history_data.get('remote_event_code'),
                history_data.get('remote_uud'),
                history_data.get('fullname'),
                history_data.get('company_join'),
                history_data.get('readding'),
                history_data.get('recordType'),
                history_data.get('process'),
                history_data.get('upload')
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def read(history_id):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees_history WHERE employees_code_id = %s", (history_id,))
            return cursor.fetchone()
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def update(history_id, updated_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            fields = ', '.join(f"{key} = %s" for key in updated_data.keys())
            values = list(updated_data.values()) + [history_id]
            sql = f"UPDATE employees_history SET {fields} WHERE employees_code_id = %s"
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def delete(history_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees_history WHERE employees_code_id = %s", (history_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)
