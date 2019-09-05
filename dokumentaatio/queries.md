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

# CRUD

Listaus, lisäys, muokkaus ja poistotoiminnallisuudet löytyvät Event ja Comment-entiteeteistä 
ja niistä kaikkia voidaan käyttää sovelluksen kautta. 

- Tapahtuma (Event)
  - Lisäys, muokkaus ja poisto vaativat admin-roolin
- Kommentti (Comment)
  - Kirjautunut käyttäjä voi jättää kommentteja
  - Muokkaus ja poisto on mahdollista joko admin-roolilla, tai vain sen käyttäjän toimesta, joka kommentin on kirjoittanut.
  
