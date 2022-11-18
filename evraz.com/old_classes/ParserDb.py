import datetime


from classes.BaseDb import BaseDb


class ParserDb(BaseDb):
    def add_order(self, url: str, order_type: str, order_id: str,
                  order_data: str, order_detail: str, customer: str,
                  was_send: int = 0) -> bool:
        query = "INSERT INTO " \
                "orders(url, order_type, order_id, order_data, order_detail, " \
                "customer, was_send) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = [(url, order_type, order_id, order_data, order_detail, customer, was_send)]
        return self.write_data_to_db(query, values)

    def create_table_orders(self):
        cursor = self.create_connection().cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT DEFAULT "", 
                order_type TEXT DEFAULT "", 
                order_id TEXT DEFAULT "", 
                order_data TEXT DEFAULT "", 
                order_detail TEXT DEFAULT "", 
                customer TEXT DEFAULT "", 
                was_send BOOLEAN DEFAULT 0
            )
        """)

    def formatted_order(self, order_row: list) -> dict:
        return {
            "created_at": self.get_created_at_date(order_row[0]),
            "url": order_row[1],
            "order_type": order_row[2],
            "order_id": order_row[3],
            "order_data": order_row[4],
            "order_detail": order_row[5],
            "customer": order_row[6],
            "was_send": order_row[7]
        }

    def get_all_orders(self) -> dict:
        query = "SELECT * FROM orders"
        rows = self.get_all_from_db(query)
        return {row[3]: self.formatted_order(row) for row in rows}

    def get_all_order_ids(self) -> list:
        query = "SELECT order_id FROM orders"
        rows = self.get_all_from_db(query)
        return [row[0] for row in rows]

    def get_order_by_order_id(self, order_id: str) -> dict:
        query = f"SELECT * FROM orders WHERE order_id={order_id}"
        rows = self.get_all_from_db(query)
        orders = [self.formatted_order(row) for row in rows]
        if orders:
            return orders.pop()
        else:
            return {}

    def get_unsent_orders(self) -> list:
        query = "SELECT * FROM orders WHERE was_send = 0"
        rows = self.get_all_from_db(query)
        return [self.formatted_order(row) for row in rows]

    def update_send_on_success(self, order_id: str) -> bool:
        query = "UPDATE orders SET was_send=1, order_data=NULL, order_detail=NULL, " \
                "customer=NULL WHERE order_id=?"
        return self.write_data_to_db(query, [(order_id,)])

    @staticmethod
    def get_created_at_date(created_at: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        return datetime.datetime.strptime(created_at, date_format)
