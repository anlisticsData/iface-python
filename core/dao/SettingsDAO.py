from core.ConexaoMySQL import MySQLConnection


class SettingsDAO:
    @staticmethod
    def create(setting_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = """
                  INSERT INTO settings (type, description, paramets, json)
                  VALUES (%s, %s, %s, %s) \
                  """
            cursor.execute(sql, (
                setting_data.get('type'),
                setting_data.get('description'),
                setting_data.get('paramets'),
                setting_data.get('json'),
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def read(setting_id):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM settings WHERE id = %s", (setting_id,))
            return cursor.fetchone()
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def by_description(description):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM settings WHERE type = %s", (description,))
            return cursor.fetchone()
        except:
            return None
        finally:
            MySQLConnection.close(conn)



    @staticmethod
    def is_block(description):
        conn = MySQLConnection.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM settings WHERE type = %s", (description,))
            row =  cursor.fetchone()
            is_block_data = int(row['json'])
            if is_block_data==0:
                return True
            else:
                return False

        except:
            return 0
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def block(description):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = f"UPDATE settings SET json='1' WHERE type=%s"
            cursor.execute(sql, [description,],)
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            pass

        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def unblock(description):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = f"UPDATE settings SET json='0' WHERE type=%s"
            cursor.execute(sql, [description, ], )
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            pass

        finally:
            MySQLConnection.close(conn)




    @staticmethod
    def update(setting_id, updated_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            fields = ', '.join(f"{key} = %s" for key in updated_data.keys())
            values = list(updated_data.values()) + [setting_id]
            sql = f"UPDATE settings SET {fields} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def delete(setting_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM settings WHERE id = %s", (setting_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)






