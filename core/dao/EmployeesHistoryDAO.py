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
                    process, upload,created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,now())
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
    def has_time(employees_code_id,time):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees_history WHERE employees_iface_id = %s and process=%s", (employees_code_id,time,))
            return cursor.fetchall()

        except Exception as e:
            print(e)
        finally:
            MySQLConnection.close(conn)



    @staticmethod
    def uploadNuvem(employees_code_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = f"update employees_history set upload='S' where employees_code_id=%s"
            cursor.execute(sql, [employees_code_id,])
            conn.commit()
            return cursor.rowcount > 0
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




    @staticmethod
    def get_pending_movements():
        results = []
        conn = MySQLConnection.connect()
        if not conn:
            return results

        try:
            cursor = conn.cursor(dictionary=True)
            sql = """
                  SELECT eh.employees_code_id, \
                         e.fullname, \
                         e.company_join, \
                         e.employees_code,
                         eh.readding, \
                         eh.process, \
                         eh.remote_uud
                  FROM employees e
                           JOIN employees_history eh ON e.id = eh.employees_iface_id
                  WHERE e.autorized = 1 \
                    AND eh.upload = 'N' \
                    AND e.deleted_at IS NULL LIMIT 0, 8 \
                  """
            cursor.execute(sql)
            for row in cursor.fetchall():
                results.append({
                    'employees_code_id': str(row.get('employees_code_id')),
                    'fullname': row.get('fullname') or '',
                    'company_join': row.get('company_join') or '',
                    'employees_code': row.get('employees_code'),
                    'readding': row.get('readding').strftime('%Y-%m-%d %H:%M:%S') if row.get('readding') else None,
                    'process': row.get('process').strftime('%Y-%m-%d %H:%M:%S') if row.get('process') else None,
                    'remote_uuid': row.get('remote_uud'),
                })
        except Exception as ex:
            # Você pode melhorar isso salvando os logs conforme fazia na versão C#
            print(f"Error: {ex}")
        finally:
            MySQLConnection.close(conn)

        return results
