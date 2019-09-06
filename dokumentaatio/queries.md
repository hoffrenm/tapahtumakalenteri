# SQL-yhteenvetokyselyt

### Tapahtumien listaus
Käyttäjä haluaa nähdä yhdellä vilkaisulla tarjolla olevat tapahtumat ja samalla saada tietoonsa niiden perustiedot, osallistuja- ja kommenttimäärät.

```sql
SELECT Event.id, Event.name, Event.location, COUNT(DISTINCT Comment.id), COUNT(DISTINCT Participation.account_id)
    FROM Event
    LEFT JOIN Comment ON Comment.event_id = Event.id
    LEFT JOIN Participation ON Participation.event_id = Event.id
    GROUP BY Event.id
    ORDER BY Event.date_time ASC
```

Kysely hakee tietokannasta kaikkien tapahtumien id:t, nimet ja sijainnit, yhdistää hakuun kommentti- ja osallistujataulut, 
laskee niiden summan ja ryhmittelee ne yksittäisen tapahtuman mukaan sekä järjestää tulokset tapahtuman ajankohdan mukaisesti 
nousevaan järjestykseen.

Tulos

![SQL1](https://github.com/hoffrenm/tapahtumakalenteri/blob/master/dokumentaatio/3-1.png)

### Tapahtumien listaus, joihin käyttäjä on ilmoittautunut
Kuten edellä, mutta nyt käyttäjä haluaa nähdä vain ne tapahtumat joihin on itse ilmoittanut osallistuvansa.

```sql
SELECT Event.id, Event.name, Event.location, COUNT(DISTINCT Comment.id), COUNT(DISTINCT Participation.account_id)
    FROM Event
    LEFT JOIN Comment ON Comment.event_id = Event.id
    LEFT JOIN Participation ON Participation.event_id = Event.id
    WHERE Participation.event_id IN
    (
        SELECT Event.id
            FROM Event
            LEFT JOIN Participation ON Participation.event_id = Event.id
            WHERE Participation.account_id = :account_id
    )
    GROUP BY Event.id
    ORDER BY Event.date_time ASC").params(account_id=account_id)
```

Identtinen kysely ylläolevan kanssa mutta kyselyssä suoritetaan alikysely niille tapahtumille joihin käyttäjä on ilmoittautunut ja hakutuloksista rajataan niiden perusteella muut tapahtumat pois.


### Käyttäjien listaus
Pääkäyttäjä haluaa yhteenvedon sovelluksen käyttäjistä sekä tietoja toiminnasta kuten käyttäjäkohtaisen ilmoittautumisten ja kommenttien määrät.

```sql
SELECT Account.name, COUNT(DISTINCT Comment.id), COUNT(DISTINCT Participation.event_id)
    FROM Account
    LEFT JOIN Comment ON Comment.account_id = Account.id
    LEFT JOIN Participation ON Participation.account_id = Account.id
    GROUP BY Account.name
```

Kysely hakee tietokannasta käyttäjien nimet, laskee käyttäjän ilmoittaumiset tapahtumiin sekä kommenttien määrät ja ryhmittelee ne yksittäisen käyttäjän mukaan.

Tulos

![SQL3](https://github.com/hoffrenm/tapahtumakalenteri/blob/master/dokumentaatio/3-2.png)

### Sovelluksessa olevat roolit ja niihin liittyvien käyttäjien määrä
Pääkäyttäjä haluaa tietää kuinka monta käyttäjää sovelluksen eri rooleilla on.

```sql
SELECT Role.name, COUNT(Roles_users.account_id)
    FROM Role
    LEFT JOIN Roles_users ON Roles_users.role_id = Role.id
    GROUP BY Role.name
```

Yhteenvetokysely hakee sovelluksen rooleihin liittyvät tunnukset liitostaulusta ja laskee eri rooleille summan siihen kuuluvista käyttäjistä.

![SQL4](https://github.com/hoffrenm/tapahtumakalenteri/blob/master/dokumentaatio/3-3.png)


# CRUD - Listaus, lisäys, muokkaus ja poisto

Listaus, lisäys, muokkaus ja poistotoiminnallisuudet löytyvät kokonaisuudessaan Event ja Comment-entiteeteistä 
ja niistä kaikkia voidaan käyttää sovelluksen kautta. 

Niihin liittyvät autorisoinnin puolesta seuraavat rajoitteet:
- Tapahtuma (Event)
  - Lisäys, muokkaus ja poisto vaativat admin-roolin
- Kommentti (Comment)
  - Kirjautunut käyttäjä voi jättää kommentteja
  - Muokkaus ja poisto on mahdollista joko admin-roolilla, tai vain sen käyttäjän toimesta, joka kommentin on kirjoittanut.
  
