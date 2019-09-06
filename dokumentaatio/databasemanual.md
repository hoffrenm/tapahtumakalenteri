# Tietokanta 6.9.2019

Tietokanta koostuu neljästä entiteettejä kuvaavista tauluista (Event, Account, Comment, Role) sekä kahdesta liitostaulusta (Roles_users, Participation).

Tietokanta sisältää 2 monesta moneen suhdetta:
- Tapahtuman (Event) ja käyttäjän (Account) välinen suhde kuvaa käyttäjän osallistumista tapahtumaan; käyttäjä voi liittyä moneen tapahtumaan ja yksittäiseen tapahtumaan voi osallistua useita eri käyttäjiä. Osallistumista kuvaavat avainparit tallennetaan liitostauluun (Participation).
- Käyttäjällä (Account) voi olla useita rooleja (Role) ja sama rooli voi kuulua usealle käyttäjälle. Roolit tallennetaan käyttäjän ja roolin väliseen liitostauluun (Roles-users).


![tietokantakaavio](https://github.com/hoffrenm/tapahtumakalenteri/blob/master/dokumentaatio/db.png)


## Tietokannan luonti SQL-lauseilla

```sql
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	description VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE event (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	location VARCHAR(144) NOT NULL, 
	date_time DATETIME NOT NULL, 
	attendee_max INTEGER, 
	attendee_min INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE roles_users (
	account_id INTEGER, 
	role_id INTEGER, 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(role_id) REFERENCES role (id)
);

CREATE TABLE participation (
	event_id INTEGER, 
	account_id INTEGER, 
	FOREIGN KEY(event_id) REFERENCES event (id) ON DELETE CASCADE, 
	FOREIGN KEY(account_id) REFERENCES account (id) ON DELETE CASCADE
);

CREATE TABLE comment (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	content VARCHAR(144) NOT NULL, 
	event_id INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(event_id) REFERENCES event (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
```
