use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
 select store_id from store where store.store_id in (select store_id from sale);


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
 select store_id from store where store.store_id not in (select store_id from sale);

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select name,avg(total/quantity) from sale natural join product where quantity is not null group by name;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select name from product natural join sale group by name having count(distinct(store_id))=1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select name from store natural join sale group by name having count(distinct(product_id))=1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
 select * from sale where total=(select MAX(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
 select date from sale group by date order by sum(total) desc, date limit 1;
