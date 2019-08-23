# Asennusohje

Sovelluksen käyttöönottoon tarvitaan seuraavat komentorivityökalut
- python3
- sqlite3
- heroku
- git

Komentorivityökalujen saattaminen käyttökuntoon on suoritusympäristökohtaista ja se jätetään asentajan vastuulle.

Ohjeen koodiblokit kuvastavat käskyjen suoritusta terminaalissa projektin juurihakemistossa.

## Projektin lataaminen paikalliselle koneelle

Lataa sovellus githubista

```
$ git clone git@github.com:hoffrenm/tapahtumakalenteri.git
```

**Tai**

Lataa ja pura projekti [zip-tiedostona](https://github.com/hoffrenm/tapahtumakalenteri/archive/master.zip)

## Sovelluksen paikallinen asennus 

1. Asenna sovelluksen käyttöön virtuaaliympäristö

```
$ python3 -m venv venv
```

2. Saata virtuaaliympäristö aktiiviseksi

```
$ source venv/bin/activate
```

3. Asenna projektin riippuvuudet

```
(venv) $ pip install -r requirements.txt
```

4. Käynnistä sovellus

```
(venv) $ python run.py
```

Sovellus käynnistyy oletusarvoisesti osoitteeseen http://localhost:5000/

5. Luo pääkäyttäjän tunnus

```
$ sqlite3 application/events.db

sqlite> INSERT INTO account (name, username, password) VALUES ('admin', 'admin', 'password');
sqlite> INSERT INTO role (name, description) VALUES ('admin', 'Full permission');
sqlite> INSERT INTO roles_users (account_id, role_id) VALUES (1, 1);
```

Sovellus on nyt käyttövalmis. Sovelluksen kautta luodut tunnukset ovat automaattisesti 'ENDUSER' roolissa.

## Sovelluksen asennus Herokuun

Tarvitset lisäksi
- [Herokun](https://www.heroku.com) tunnukset

1. Luo sovellukselle Heroku-projekti

```
$ heroku create projektin-nimi
```

2. Liitä paikallinen repositorio Heroku-sovellukseen

```
$ git remote add heroku
$ git add .
$ git commit -m "commit for heroku"
```

3. Lähetä sovellus Herokuun

```
$ git push heroku master
```

4. Tarvittavat Heroku-konfiguraatiot

```
$ heroku config:set HEROKU=1
$ heroku addons:add heroku-postgresql:hobby-dev
```

5. Luo pääkäyttäjän tunnus

```
$ heroku pg:psql

tietokannan-nimi-12345::DATABASE=> INSERT INTO account (name, username, password) VALUES ('admin', 'admin', 'password');
tietokannan-nimi-12345::DATABASE=> INSERT INTO role (name, description) VALUES ('admin', 'Full permission');
tietokannan-nimi-12345::DATABASE=> INSERT INTO roles_users (account_id, role_id) VALUES (1, 1);
```

Sovellus on nyt käyttövalmis. Sovelluksen kautta luotavat tunnukset ovat automaattisesti 'ENDUSER' roolissa.
