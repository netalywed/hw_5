select name, year from albom
where year = 2018;

select name from song
where duration >= 3.5;

select name from collection 
where year >= 2018 and year <= 2020;

select name from singer 
where name not like '%% %%';

select name from song 
where name like '%%My%%';

SELECT name, duration from song  
WHERE duration = (SELECT MAX(duration) FROM song);