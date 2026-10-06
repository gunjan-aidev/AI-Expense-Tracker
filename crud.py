from database import get_connection


def create_expense(title, amount, category, expense_date):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO expenses
                    (title, amount, category, expense_date)
                VALUES
                    (%s, %s, %s, %s)
                RETURNING id, title, amount, category, expense_date;
            """

            cursor.execute(
                query,
                (title, amount, category, expense_date),
            )

            return cursor.fetchone()


def get_expenses(category=None, month_start=None, month_end=None):
    query = """
        SELECT id, title, amount, category, expense_date
        FROM expenses
    """

    conditions = []
    parameters = []

    if category:
        conditions.append("category = %s")
        parameters.append(category)

    if month_start and month_end:
        conditions.append("expense_date >= %s")
        conditions.append("expense_date < %s")
        parameters.extend([month_start, month_end])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        ORDER BY expense_date DESC, id DESC;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()


def get_expense_by_id(expense_id):
    query = """
        SELECT id, title, amount, category, expense_date
        FROM expenses
        WHERE id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (expense_id,))
            return cursor.fetchone()


def delete_expense(expense_id):
    query = """
        DELETE FROM expenses
        WHERE id = %s
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (expense_id,))
            return cursor.fetchone()


def get_expense_summary(month_start=None, month_end=None):
    conditions = []
    parameters = []

    if month_start and month_end:
        conditions.append("expense_date >= %s")
        conditions.append("expense_date < %s")
        parameters.extend([month_start, month_end])

    where_clause = ""

    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                f"""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(amount), 0)
                FROM expenses
                {where_clause};
                """,
                parameters,
            )

            total_row = cursor.fetchone()

            cursor.execute(
                f"""
                SELECT
                    category,
                    COUNT(*),
                    COALESCE(SUM(amount), 0)
                FROM expenses
                {where_clause}
                GROUP BY category
                ORDER BY SUM(amount) DESC;
                """,
                parameters,
            )

            category_rows = cursor.fetchall()

            return total_row, category_rows