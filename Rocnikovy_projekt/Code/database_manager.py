from psycopg2 import connect
from enums import FileType

class DBManager:
    def __init__(self, host, database, user, password, metrics):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.metrics = metrics
        self._create_tables()
        self._insert_file_types()
        self._insert_metric_types()


    def _connect(self):
        return connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def _create_tables(self):
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS file_types (
                                        f_type_id SERIAL PRIMARY KEY,
                                        f_type VARCHAR(100) NOT NULL
                                    );
                                    """)

                    cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS files (
                                        file_id SERIAL PRIMARY KEY,
                                        f_name VARCHAR(255) NOT NULL,
                                        time TIMESTAMP NOT NULL,
                                        f_type_id INTEGER NOT NULL REFERENCES file_types(f_type_id)
                                    );
                                    """)

                    cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS metrics (
                                        metric_id SERIAL PRIMARY KEY,
                                        metric_type VARCHAR(255) NOT NULL
                                    );
                                    """)

                    cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS calculated_metrics (
                                            id SERIAL PRIMARY KEY,
                                            file_id INTEGER NOT NULL REFERENCES files(file_id),
                                            metric_id INTEGER NOT NULL REFERENCES metrics(metric_id),
                                            value INTEGER NOT NULL
                                    );
                                    """)

            conn.commit()


    def _insert_file_types(self):
        with self._connect() as conn:
            with conn.cursor() as cursor:

                file_types = []
                for file_type in FileType:
                    file_types.append(file_type.value)

                for file_type in file_types:
                    cursor.execute("""
                                                SELECT 1 FROM file_types WHERE f_type = %s;
                                            """, (file_type,))
                    if cursor.fetchone() is None:
                        cursor.execute(
                            """
                                    INSERT INTO file_types (f_type) VALUES (%s)
                            """, (file_type,))

        conn.commit()

    def _insert_metric_types(self):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                for metric in self.metrics:
                    cursor.execute("""
                                    SELECT 1 FROM metrics WHERE metric_type = %s;
                                """, (metric.name,))
                    if cursor.fetchone() is None:
                        cursor.execute(
                            """
                                    INSERT INTO metrics (metric_type) VALUES (%s)
                            """, (metric.name,))

        conn.commit()

    def save(self, file_name, file_type, metric_type, timestamp, metric_value):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT f_type_id FROM file_types WHERE f_type = %s
                """, (file_type,))

                file_type_row = cursor.fetchone()

                if file_type_row is None:
                    raise ValueError("Wrong file type!")
                else:
                    f_type_id = file_type_row[0]

                cursor.execute("""
                                    SELECT file_id FROM files WHERE f_name = %s AND time = TO_TIMESTAMP(%s, 'YYYYMMDDHH24MISS') 
                                    AND f_type_id = %s
                                """, (file_name, timestamp, f_type_id,))

                file_row = cursor.fetchone()

                if file_row is None:
                    cursor.execute("""
                                        INSERT INTO files (f_name, f_type_id, time) VALUES (%s, %s, TO_TIMESTAMP(%s, 'YYYYMMDDHH24MISS')) RETURNING file_id;
                                    """, (file_name, f_type_id, timestamp,))
                    file_row = cursor.fetchone()



                file_id = file_row[0]

                cursor.execute("""
                    SELECT metric_id FROM metrics WHERE metric_type = %s
                """, (metric_type,))

                metric_row = cursor.fetchone()
                if metric_row is None:
                    raise ValueError("Wrong metric type!")
                else:
                    metric_id = metric_row[0]

                cursor.execute("""
                    INSERT INTO calculated_metrics (file_id, metric_id, value)
                    VALUES (%s, %s, %s);
                """, (int(file_id), int(metric_id), int(metric_value)))

        conn.commit()

    def get_value(self, file_name, metric_type, file_format, time_stamp):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                            SELECT cm.value
                            FROM calculated_metrics cm
                            JOIN files f ON cm.file_id = f.file_id
                            JOIN metrics m ON cm.metric_id = m.metric_id
                            JOIN file_types ft ON f.f_type_id = ft.f_type_id
                            WHERE f.f_name = %s AND m.metric_type = %s AND ft.f_type = %s AND time = TO_TIMESTAMP(%s, 'YYYYMMDDHH24MISS');
                        """, (file_name, metric_type, file_format, time_stamp))

                result = cursor.fetchall()
                return result
