from datetime import datetime

from core.ConexaoMySQL import MySQLConnection


class EventsDAO:
    @staticmethod
    def create(event_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO events (event, created_at, event_log)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                event_data.get('event'),
                event_data.get('created_at', datetime.now()),
                event_data.get('event_log')
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def read(event_id):
        conn = MySQLConnection.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM events WHERE id = %s"
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def update(event_id, update_data):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = """
                UPDATE events
                SET event = %s, event_log = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                update_data.get('event'),
                update_data.get('event_log'),
                event_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def delete(event_id):
        conn = MySQLConnection.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM events WHERE id = %s"
            cursor.execute(sql, (event_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            MySQLConnection.close(conn)

    @staticmethod
    def list_all():
        conn = MySQLConnection.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM events ORDER BY created_at DESC"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            MySQLConnection.close(conn)
