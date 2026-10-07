
import psycopg


class AfsphereDB():
    def __init__(self):
        self.conn = psycopg.connect("host=127.0.0.1 port=5432 dbname=afsphere user=pizzamozzarella password=gotica")

    def Execute(self, query, values):
        with self.conn.cursor() as cur:
            cur.execute(query, values)

            self.conn.commit()
            if cur.description:
                return cur.fetchall()
            return None

    def OneExecute(self, query, values):
        with self.conn.cursor() as cur:
            cur.execute(query, values)

            self.conn.commit()
            if cur.rowcount == 0:
                return None
            return cur.fetchone()[0]

    def Exists(self, query, values):
        with self.conn.cursor() as cur:
            cur.execute("SELECT EXISTS(" + query + ");", values)

            return cur.fetchone()[0]

    def close(self):
        self.conn.close()
