# Kivi-Paperi-Sakset Web-sovellus

Web-pohjainen versio klassisesta kivi-paperi-sakset -pelistä, joka on toteutettu Flaskilla.

## Ominaisuudet

- **Kaksinpeli**: Pelaa kaverisi kanssa samalta tietokoneelta
- **Tekoäly (helppo)**: Pelaa yksinkertaista tekoälyä vastaan
- **Tekoäly (haastava)**: Pelaa parannettua tekoälyä vastaan, joka oppii pelistäsi

## Asennus

Projekti käyttää Poetrya riippuvuuksien hallintaan.

```bash
# Asenna riippuvuudet
poetry install
```

## Käyttö

### Web-sovellus (suositeltu)

Käynnistä Flask-palvelin:

```bash
cd src
poetry run python web_app.py
```

Avaa selaimessa: http://127.0.0.1:5000

### Komentorivi

Voit myös pelata komentorivillä:

```bash
cd src
poetry run python index.py
```

## Teknologiat

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS (responsiivinen suunnittelu)
- **Riippuvuuksien hallinta**: Poetry
- **Ohjelmointikieli**: Python 3.12

## Projektista

Projekti käyttää olemassa olevaa logiikkaa (`kps.py`, `tuomari.py`, `tekoaly.py`) ja toteuttaa vain web-kerroksen päälle. Alkuperäinen komentorivisovellus toimii edelleen normaalisti.

### Tiedostorakenne

```
kivi-paperi-sakset/
├── pyproject.toml          # Poetry-konfiguraatio
├── src/
│   ├── index.py            # Komentorivisovellus
│   ├── web_app.py          # Flask-sovellus
│   ├── kps.py              # Pelilogiikka
│   ├── tuomari.py          # Pistelaskenta
│   ├── tekoaly.py          # Tekoäly-toteutukset
│   ├── templates/          # HTML-templateit
│   │   ├── base.html
│   │   ├── index.html
│   │   └── pelaa.html
│   └── static/             # CSS-tyylit
│       └── style.css
```

## Pelaaminen

1. Valitse pelimuoto etusivulta
2. Tee siirtosi klikkaamalla kiveä, paperia tai saksia
3. Kaksinpelissä toinen pelaaja valitsee myös siirtonsa
4. Pisteet päivittyvät automaattisesti
5. Pelihistoria näyttää viimeisimmät 10 kierrosta
6. Voit lopettaa pelin milloin tahansa "Lopeta peli" -napista

## Kehitys

Flask-sovellus on kehitystilassa (debug mode), joka mahdollistaa:
- Automaattisen uudelleenkäynnistyksen koodin muuttuessa
- Yksityiskohtaiset virheilmoitukset
- Debugger-työkalut

Tuotantokäyttöön sovellus tulisi ajaa WSGI-palvelimella (esim. Gunicorn, uWSGI).
