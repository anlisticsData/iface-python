from core.ConexaoMySQL import MySQLConnection


class EmployeeDAO:
    @staticmethod
    def create(employee_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO employees (
                    autorized, employees_code, fullname, rg, cpf,
                    controller_code, company_join, remote_event_code,
                    remote_uuid, data_bloqueio_liberacao, deleted_at, iface,photo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            """
            cursor.execute(sql, (
                employee_data.get('autorized'),
                employee_data.get('employees_code'),
                employee_data.get('fullname'),
                employee_data.get('rg'),
                employee_data.get('cpf'),
                employee_data.get('controller_code'),
                employee_data.get('company_join'),
                employee_data.get('remote_event_code'),
                employee_data.get('remote_uuid'),
                employee_data.get('data_bloqueio_liberacao'),
                employee_data.get('deleted_at'),
                employee_data.get('iface'),
                employee_data.get('photo')
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            MySQLConnection.close(conn)


    @staticmethod
    def read(employee_id):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE id = %s and deleted_at is null ", (employee_id,))
            return cursor.fetchone()
        finally:
            MySQLConnection.close(conn)



    @staticmethod
    def device_not_faces():
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE iface = 'N' and deleted_at is null and  photo is not null")
            return cursor.fetchall()
        finally:
            MySQLConnection.close(conn)







    @staticmethod
    def remote_employee_code(employee_id):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE employees_code = %s and deleted_at is null", (employee_id,))
            return cursor.fetchone()
        finally:
            MySQLConnection.close(conn)




    @staticmethod
    def update(employee_id, updated_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            fields = ', '.join(f"`{key}` = %s" for key in updated_data.keys())
            values = list(updated_data.values()) + [employee_id]
            sql = f"UPDATE employees SET {fields} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(e)
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def delete(employee_id, updated_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            fields = ', '.join(f"`{key}` = %s" for key in updated_data.keys())
            values = list(updated_data.values()) + [employee_id]
            sql = f"UPDATE employees SET {fields} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(e)
        finally:
            MySQLConnection.close(conn)




    @staticmethod
    def delete_in_device(employee_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE  employees set deleted_at=now() WHERE id = %s", (employee_id,))
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(e)
            return  None
        finally:
            MySQLConnection.close(conn)




    @staticmethod
    def disabled(employee_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE employees SET autorized=0 WHERE id = %s", (employee_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)


    @staticmethod
    def enabled(employee_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE employees SET autorized=1,iface='S' WHERE id = %s", (employee_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)



