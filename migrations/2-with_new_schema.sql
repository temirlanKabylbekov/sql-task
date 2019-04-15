-- Schema changing:
--    adding not null constraints for exchange_rates table columns
--      (the reason is with at least one null value, none of the rows of these tables will have a meaning)
--    preliminary addition in exchange_rates table unique rows from one currency to the same currency with a date in the distant past and rate = 1

drop table if exists exchange_rates;
create table exchange_rates(
    ts timestamp without time zone not null,
    from_currency varchar(3) not null,
    to_currency varchar(3) not null,
    rate numeric not null
);
truncate table exchange_rates;


drop table if exists transactions;
create table transactions (
    ts timestamp without time zone,
    user_id int,
    currency varchar(3),
    amount numeric
);
truncate table transactions;
