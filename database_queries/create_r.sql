create table singer(
	id serial primary key,
	name varchar(70) not null
);

create table albom(
	id serial primary key,
	name varchar(100) not null,
	year integer check(year > 1500 and year < 3000)
);

create table song(
	id serial primary key,
	name varchar(100) not null,
	duration numeric,
	albom_id integer references albom(id)
);

create table if not exists genre(
	id serial primary key,
	name varchar(80) not null
);
create table if not exists singergenre(
	singer_id integer references singer(id),
	genre_id integer references genre(id),
	constraint pk_singergenre primary key (singer_id, genre_id)
);
create table if not exists collection(
	id serial primary key,
	name varchar(100),
	year integer check(year > 1500 and year < 3000)
);

create table if not exists collectionsong(
	collection_id integer references collection(id),
	song_id integer references song(id),
	constraint pk_collectionsong primary key (collection_id, song_id)
);

create table if not exists singeralbom(
	singer_id integer references singer(id),
	albom_id integer references albom(id),
	constraint pk_singeralbom primary key (singer_id, albom_id)
);


