insert into vista_test_task_phone_book.users (id, username, email, password, birth_date, created_at)
values (1, 'petya', 'petya@a.b', md5('password'), '2000-01-01', '2022-04-13 09:48:04'),
       (2, 'вася', 'vasya@ya.com', md5('password'), '2000-01-01', '2022-04-13 09:48:04'),
       (3, 'иван петров', 'email', md5('password'), '2021-03-15', '2022-04-13 09:48:04');

insert into vista_test_task_phone_book.contacts (id, name, phone_number, birth_date, owner_id)
values (1, 'Иванов Иван', '891150040011', '1975-05-13', 1),
       (2, 'Александров Вячеслав', '898166655544', '2004-04-04', 1),
       (3, 'Васин Василий', '+79213345324', '2000-06-04', 1),
       (4, 'Горина Анастасия', '+73456755334', '1995-08-05', 1),
       (5, 'Ёжиков\nЁжик', '-123', '1912-05-15', 1),
       (6, 'Doe John', '+132145689', '1900-01-01', 1),
       (7, '# fda898', '5;l1;&	%*951', '0500-01-01', 1),
       (8, 'Имяреков Имярек', '+3512312355', '1917-05-15', 2);
