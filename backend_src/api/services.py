import psycopg2
import logging


class DbService:
    _instance = None

    def __new__(cls, db_url: str) -> "DbService":
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                conn_params = cls.parse_db_url(db_url)
                cls._instance.conn = psycopg2.connect(**conn_params)
                cls._instance.conn.autocommit = True  # Set autocommit to True
            except psycopg2.Error as e:
                logging.error("Unable to connect to the database: %s", e)
                raise e
        return cls._instance

    @staticmethod
    def parse_db_url(db_url: str):
        import re

        # Parse the db_url using a regular expression
        # Assumes format: postgresql://user:password@host:port/dbname
        pattern = re.compile(
            r"postgresql://(?P<user>\w+):(?P<password>\w+)@(?P<host>\S+):(?P<port>\d+)/(?P<dbname>\w+)")
        match = pattern.match(db_url)
        if not match:
            raise ValueError("Invalid db_url format")

        # Extract the connection parameters from the matched groups
        conn_params = match.groupdict()
        conn_params["password"] = conn_params["password"].replace(
            "%", "%25").replace("+", "%2B").replace(" ", "+")
        return conn_params

    def execute(self, query, params=None):
        return_results = []
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

            for row in data:
                result = {}
                for i in range(len(columns)):
                    result[columns[i]] = row[i]
                return_results.append(result)
        return return_results


class PriceService:
    def __init__(self, db_service):
        self.db_service = db_service

    def get_prices(self, date_from, date_to, origin, destination):
        # SQL query to fetch prices data based on input parameters
        prices_query = """
        SELECT to_char(d.day, 'YYYY-MM-DD') AS day, ROUND(p.price) AS average_price
        FROM (
            SELECT generate_series(%s, %s, '1 day') AS day
        ) d
        LEFT JOIN (
            SELECT day, ROUND(AVG(price)) AS price
            FROM prices p3
            WHERE (orig_code = %s
                OR orig_code IN (
                    SELECT DISTINCT p1.code
                    FROM ports p1
                    INNER JOIN regions r1 ON p1.parent_slug = r1.parent_slug
                    WHERE r1.parent_slug = %s
                        OR r1.slug = %s
                ))
                AND (dest_code = %s
                    OR dest_code IN (
                        SELECT DISTINCT p2.code
                        FROM ports p2
                        INNER JOIN regions r2 ON p2.parent_slug = r2.parent_slug
                        WHERE r2.parent_slug = %s
                            OR r2.slug = %s
                    ))
                AND p3.day BETWEEN %s AND %s
            GROUP BY day -- include "day" in the GROUP BY clause
            HAVING COUNT(*) >= 3
        ) p ON d.day = p.day
        ORDER BY d.day;
        """
        prices = self.db_service.execute(prices_query, (
            date_from,
            date_to,
            origin,
            origin,
            origin,
            destination,
            destination,
            destination,
            date_from,
            date_to
        ))
        return prices


class ApiService:
    def __init__(self, db_url):
        self.db_service = DbService(db_url)
        self.price_service = PriceService(self.db_service)

    def get_prices(self, date_from, date_to, origin, destination):
        prices = self.price_service.get_prices(
            date_from, date_to, origin, destination)
        return prices
