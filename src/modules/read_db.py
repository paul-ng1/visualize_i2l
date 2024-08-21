from sshtunnel import SSHTunnelForwarder
import psycopg2
from psycopg2 import sql


class DatabaseConnection:
    def __init__(self, ssh_host, ssh_port, ssh_user, ssh_private_key, db_host, db_port, db_name, db_user, db_password) -> None:
        self.tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_private_key=ssh_private_key,
            remote_bind_address=(db_host, db_port)
        )
        self.tunnel.start()
        self.connection = psycopg2.connect(
            host='localhost',
            port=self.tunnel.local_bind_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.tunnel.stop()


def get_capture_history(db_connection, limit: int = 10):
    db_connection.cursor.execute(f"SELECT * FROM capture_history order BY created_at DESC limit {limit};")
    result = db_connection.cursor.fetchall()
    
    return result
    

def get_generate_history(db_connection, section_source):
    section_url = section_source.replace('https://', '%')
    db_connection.cursor.execute(f"select * from generate_history where image_source like '{section_url}';")
    result = db_connection.cursor.fetchone()

    return result