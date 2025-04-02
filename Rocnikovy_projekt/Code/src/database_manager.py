from psycopg2 import connect
from psycopg2 import sql, DatabaseError, IntegrityError
from .enums import FileType

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
        try:
            return connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
        except DatabaseError as e:
            raise RuntimeError(f"Database connection failed: {e}")

    def _create_tables(self):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS file_types (
                            f_type_id SERIAL PRIMARY KEY,
                            f_type VARCHAR(100) NOT NULL UNIQUE
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
                            metric_type VARCHAR(255) NOT NULL UNIQUE,
                            is_column_based BOOLEAN NOT NULL DEFAULT FALSE
                        );
                    """)

                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS calculated_metrics (
                            id SERIAL PRIMARY KEY,
                            file_id INTEGER NOT NULL REFERENCES files(file_id),
                            metric_id INTEGER NOT NULL REFERENCES metrics(metric_id),
                            value INTEGER NOT NULL,
                            column_name VARCHAR(255) NULL
                        );
                    """)

            conn.commit()
        except DatabaseError as e:
            print(f"Error creating tables: {e}")

    def _insert_file_types(self):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    for file_type in FileType:
                        cursor.execute("""
                            INSERT INTO file_types (f_type) 
                            VALUES (%s) 
                            ON CONFLICT (f_type) DO NOTHING;
                        """, (file_type.value,))

            conn.commit()
        except DatabaseError as e:
            print(f"Error inserting file types: {e}")

    def _insert_metric_types(self):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    for metric in self.metrics:
                        cursor.execute("""
                            INSERT INTO metrics (metric_type, is_column_based) 
                            VALUES (%s, %s) 
                            ON CONFLICT (metric_type) DO UPDATE 
                            SET is_column_based = EXCLUDED.is_column_based;
                        """, (metric.name, metric.is_column_based))

            conn.commit()
        except DatabaseError as e:
            print(f"Error inserting metric types: {e}")

    def save(self, file_name, file_type, metric_type, timestamp, metric_value):
        try:
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

        except ValueError as e1:
            print(f"Validation Error: {e1}")
        except IntegrityError as e2:
            print(f"Database Integrity Error: {e2}")
        except DatabaseError as e3:
            print(f"Database Error: {e3}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_value(self, file_name, metric_type, file_format, time_stamp, column=None):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    if column:
                        cursor.execute("""
                                            SELECT cm.value
                                            FROM calculated_metrics cm
                                            JOIN files f ON cm.file_id = f.file_id
                                            JOIN metrics m ON cm.metric_id = m.metric_id
                                            JOIN file_types ft ON f.f_type_id = ft.f_type_id
                                            WHERE f.f_name = %s AND m.metric_type = %s AND ft.f_type = %s 
                                            AND cm.column = %s AND time = TO_TIMESTAMP(%s, 'YYYYMMDDHH24MISS');
                                            """, (file_name, metric_type, file_format, column, time_stamp))
                    else:
                        cursor.execute("""
                                            SELECT cm.value
                                            FROM calculated_metrics cm
                                            JOIN files f ON cm.file_id = f.file_id
                                            JOIN metrics m ON cm.metric_id = m.metric_id
                                            JOIN file_types ft ON f.f_type_id = ft.f_type_id
                                            WHERE f.f_name = %s AND m.metric_type = %s AND ft.f_type = %s 
                                            AND cm.column IS NULL AND time = TO_TIMESTAMP(%s, 'YYYYMMDDHH24MISS');
                                            """, (file_name, metric_type, file_format, time_stamp))

                    result = cursor.fetchall()
                    return result

        except ValueError as ve:
            print(f"Validation Error: {ve}")
            return None
        except DatabaseError as de:
            print(f"Database Error: {de}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None

    def get_file_types(self):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                                        SELECT ft.f_type
                                        FROM file_types ft
                                        """)

                    result = cursor.fetchall()
                    return result
        except DatabaseError as de:
            print(f"Database Error: {de}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None
