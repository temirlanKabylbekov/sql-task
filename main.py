from decimal import Decimal


def get_result(conn, to_currency):
    with conn.cursor() as cursor:
        query = f'''
        SELECT Tr.user_id as user_id,
               ROUND(SUM(CASE WHEN Tr.currency = '{to_currency}' THEN 1 ELSE COALESCE(Ex.rate, 0) END * COALESCE(Tr.amount, 0)), 3) as total_spent_gbp
        FROM
        (SELECT Tr.ts AS tr_ts,
                Tr.currency AS currency,
                CASE
                    WHEN Tr.currency = '{to_currency}' THEN NULL
                    ELSE max(Ex.ts)
                END AS ex_ts
        FROM exchange_rates AS Ex,
             transactions AS Tr
        WHERE (Ex.from_currency = Tr.currency
               AND Ex.rate IS NOT NULL
               AND Ex.ts <= Tr.ts)
               OR Tr.currency = '{to_currency}'
        GROUP BY Tr.ts,
                 Tr.currency) AS A
        LEFT JOIN exchange_rates AS Ex ON (Ex.ts = A.ex_ts
                                           AND Ex.to_currency = '{to_currency}'
                                           AND Ex.from_currency = A.currency)
        INNER JOIN transactions AS Tr ON (Tr.ts = A.tr_ts
                                          AND Tr.currency = A.currency)
        GROUP BY Tr.user_id
        ORDER BY Tr.user_id;
        '''
        cursor.execute(query)
        return cursor.fetchall()


def get_result_for_new_schema(conn, to_currency):
    with conn.cursor() as cursor:
        query = f'''
        SELECT Tr.user_id AS user_id,
               ROUND(SUM(Ex.rate * COALESCE(Tr.amount, 0)), 3) AS total_spent_gbp
        FROM transactions AS Tr,
             exchange_rates AS Ex,
            (SELECT Tr.ts AS tr_ts,
                    Tr.currency AS currency,
                    max(Ex.ts) AS ex_ts
            FROM exchange_rates AS Ex,
                 transactions AS Tr
            WHERE Ex.from_currency = Tr.currency
                  AND Ex.ts <= Tr.ts
            GROUP BY Tr.ts,
                     Tr.currency) AS A
        WHERE Ex.ts = A.ex_ts
              AND Ex.from_currency = A.currency
              AND Ex.to_currency = '{to_currency}'
              AND Tr.ts = A.tr_ts
              AND Tr.currency = A.currency
        GROUP BY Tr.user_id
        ORDER BY Tr.user_id;
        '''
        cursor.execute(query)
        return cursor.fetchall()


def round_number_to_decimal(value, precision):
    return Decimal(str(round(value, precision)))
