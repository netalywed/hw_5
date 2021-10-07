


insert into genre (name)
values 
('rnb'),
('pop'),
('black metal'),
('symphonic metal'),
('blues'),
('rock');

insert into singergenre(singer_id, genre_id)
values 
(1, 6),
(2, 1),
(3, 2),
(4, 3),
(5, 4),
(6, 5),
(7, 6),
(8, 6),
(9, 1);

# singer, genre, link
INSERT INTO singer (name) 
VALUES 
('Lennon')
('Beyonce'),
('Lady Gaga'),
('Burzum'),
('Nightwish'),
('Janis Joplin'),
('Pink Floyd'),
('Joni Mitchell'),
('Shakira');


#albom, link singer
insert into albom(name, year)
values 
('Please Please Me', 1963),
('Everything is love', 2018),
('Cromatica', 2020),
('Burzum', 1992),
('Wishmaster', 2000),
('Cheap Thrills', 1968),
('The Wall', 1979),
('Blue', 1971),
('Laundry Service', 2002);

insert into singeralbom(singer_id, albom_id)
values 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9);

#song
insert into song(name, duration, albom_id)
values 
('Misery', 1.50, 1),
('I saw her standing there', 2.54, 1),
('Summer', 4.45, 2),
('Apeshit', 4.25, 2),
('Stupid love', 3.13, 3),
('Rain on me', 3.02, 3),
('911', 2.52, 3),
('Feeble Screams from Forests Unknown', 7.28, 4),
('Black Spell of Destruction', 5.39, 4),
('War', 2.50, 4),
('Sleeping sun', 4.05, 5),
('Wishmaster', 4.24, 5),
('Combination of the Two', 5.47, 6),
('I Need a Man to Love', 4.54, 6),
('Goodbye Blue Sky', 4.29, 7),
('Empty Spaces', 2.07, 7),
('Dont Leave Me Now', 4.16, 7),
('All I Want', 3.32, 8),
('Little Green', 3.25, 8),
('Blue', 3.00, 8),
('Objection (Tango)', 3.44, 9),
('Underneath Your Clothes', 3.45, 9),
('Piece of My Heart', 4.15, 6);

#collection, link song
insert into collection(name, year)
values 
('Rock songs', 2020),
('Pop songs', 2021),
('Female vocal', 2015),
('Female vocal', 2020),
('Old hits', 2002),
('Metal', 2014),
('Ballads', 2011),
('Greatest hits', 2021);

insert into collectionsong(collection_id, song_id)
values 
(1, 1),
(1, 2),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(3, 11),
(3, 12),
(3, 13),
(3, 14),
(3, 18),
(3, 19),
(3, 20),
(3, 21),
(3, 22),
(4, 11),
(4, 12),
(4, 13),
(4, 14),
(4, 18),
(4, 19),
(4, 20),
(4, 21),
(4, 22),
(4, 3),
(4, 4),
(4, 5),
(4, 6),
(4, 7),
(5, 1),
(5, 2),
(5, 13),
(5, 14),
(5, 15),
(5, 16),
(5, 17),
(5, 18),
(5, 19),
(5, 20),
(6, 8),
(6, 9),
(6, 10),
(6, 11),
(6, 12),
(7, 11),
(7, 18),
(7, 20),
(7, 22),
(8, 2),
(8, 6),
(8, 7),
(8, 21),
(8, 22),
(3, 23),
(4, 23),
(5, 23);
