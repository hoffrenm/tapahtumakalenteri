# Asennusohje

Sovelluksen käyttöönottoon tarvitaan seuraavat komentorivityökalut
- python3
- sqlite3
- heroku
- git

Komentorivityökalujen saattaminen käyttökuntoon on suoritusympäristökohtaista ja se jätetään asentajan vastuulle.

Ohjeen koodiblokit kuvastavat käskyjen ajoa terminaalissa projektin juurihakemistossa.

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

sqlite> INSERT INTO account (name, username, password, role) VALUES ('admin', 'admin', 'password', 'ADMIN');
```

Sovellus on nyt käyttövalmis. Sovelluksen kautta luodut tunnukset ovat automaattisesti 'ENDUSER' roolissa.

## Sovelluksen asennus Herokuun

Tarvitset lisäksi
- [Herokun](https://www.heroku.com) tunnukset

1. Luo sovellukselle Heroku-projekti

```
$ heroku create <pre><i>nimi</i></pre>
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

<pre><i>tietokannan-nimi-12345</i></pre>::DATABASE=>INSERT INTO account (name, username, password, role) VALUES ('admin', 'admin', 'password', 'ADMIN');
```

Sovellus on nyt käyttövalmis. Sovelluksen kautta tehtävät tunnukset ovat automaattiseti 'ENDUSER' roolissa.
