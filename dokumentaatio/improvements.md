# Työn puutteet ja kehitysideat

- Sovelluksessa on tällä hetkellä vain 2 roolia: admin ja enduser (Nyt kaikki ylläpito vaatii admin-roolin).
 Ideana oli lisätä kolmas rooli, esim. "järjestäjä", jolla olisi pääkäyttäjää rajatummat oikeudet vain omien tapahtumien 
 luontiin ja hallintaan
  - Flask-securityn ansiosta uusien roolien luominen ja autorisointi on kuitenkin suoraviivaista
  - Lisäksi tapahtuman tulisi tallettaa tieto sen luoneesta käyttäjästä, jotta käyttäjäkohtainen 
  tapahtumanhallinta olisi mahdollista
  
- Sovelluksessa ei pysty tällä hetkellä hakemaan tapahtumia esimerkiksi tapahtuman nimestä tai muutenkaan rajaamaan tuloksia.
