drop table if exists exchange_rates;
create table exchange_rates(
    ts timestamp without time zone,
    from_currency varchar(3),
    to_currency varchar(3),
    rate numeric
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
