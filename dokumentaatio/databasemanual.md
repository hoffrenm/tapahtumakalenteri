# Tietokanta 24.8.2019

![tietokantakaavio](https://github.com/hoffrenm/tapahtumakalenteri/blob/master/dokumentaatio/db.png)

## Tietokannan luonti SQL-lauseilla
MySQL-syntaksi

```sql
CREATE TABLE `account`
(
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(144) NOT NULL,
  `username` varchar(144) NOT NULL,
  `password` hash NOT NULL
);

CREATE TABLE `event`
(
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(144) NOT NULL,
  `description` varchar(1023),
  `location` varchar(144) NOT NULL,
  `date_time` date NOT NULL,
  `attendee_max` int DEFAULT 0
);

CREATE TABLE `comment`
(
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `content` varchar(144) NOT NULL,
  `event_id` int NOT NULL,
  `account_id` int NOT NULL
);

CREATE TABLE `roles_users`
(
  `account_id` int NOT NULL,
  `role_id` int NOT NULL
);

CREATE TABLE `role`
(
  `id` int UNIQUE PRIMARY KEY,
  `name` varchar(64) NOT NULL,
  `description` varchar(255) NOT NULL
);

CREATE TABLE `participation`
(
  `account_id` int NOT NULL,
  `event_id` int NOT NULL
);

ALTER TABLE `comment` ADD FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);

ALTER TABLE `comment` ADD FOREIGN KEY (`account_id`) REFERENCES `account` (`id`);

ALTER TABLE `roles_users` ADD FOREIGN KEY (`account_id`) REFERENCES `account` (`id`);

ALTER TABLE `roles_users` ADD FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);

ALTER TABLE `participation` ADD FOREIGN KEY (`account_id`) REFERENCES `account` (`id`);

ALTER TABLE `participation` ADD FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);
```
