SQL -запрос представляет собой то-то

снять видео как у меня все это работает, вдруг у них не поднимется

приложить оутпут Explain
tests stress (кэш не работает, тк на новой базе прогоняем тесты)


не рассматриваем тот случай, когда совершена транзакция в валюте А
и в exchange rates нет прямого A -> GBP
есть A -> B, B -> GBP

добавить в таблицу GBP -> GBP = 1
ускорить

стресс-тест
    мерим первый запуск на новой бд
    на одной бд померить бы еще
    



SELECT Tr.user_id,
       SUM(COALESCE(Ex.rate, 1) * Tr.amount)
FROM
  (SELECT Tr.ts AS tr_ts,
          Tr.currency AS currency,
          CASE
              WHEN Tr.currency = 'GBP' THEN NULL
              ELSE max(Ex.ts)
          END AS ex_ts
   FROM exchange_rates AS Ex,
        transactions AS Tr
   WHERE (Ex.from_currency = Tr.currency
          AND Ex.ts <= Tr.ts) OR Tr.currency = 'GBP'
   GROUP BY Tr.ts,
            Tr.currency) AS A
LEFT JOIN exchange_rates AS Ex ON (Ex.ts = A.ex_ts
                                   AND Ex.to_currency = 'GBP'
                                   AND Ex.from_currency = A.currency)
INNER JOIN transactions AS Tr ON (Tr.ts = A.tr_ts
                                  AND Tr.currency = A.currency)
GROUP BY Tr.user_id;

