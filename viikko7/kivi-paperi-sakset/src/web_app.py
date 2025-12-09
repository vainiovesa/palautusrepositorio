from flask import Flask, render_template, request, session, redirect, url_for
from kps import Pelit, KPSPelaajaVsPelaaja, KPSHuonompiTekoaly, KPSParempiTekoaly
from tuomari import Tuomari
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


class WebKPSPelaajaVsPelaaja:
    """Web-adapted two-player game"""
    def __init__(self, tuomari):
        self.tuomari = tuomari
    
    def _onko_ok_siirto(self, siirto):
        return siirto in ("k", "p", "s")
    
    def pelaa_kierros(self, pelaaja1_siirto, pelaaja2_siirto):
        if self._onko_ok_siirto(pelaaja1_siirto) and self._onko_ok_siirto(pelaaja2_siirto):
            self.tuomari.kirjaa_siirto(pelaaja1_siirto, pelaaja2_siirto)
            return True
        return False


class WebKPSTekoaly:
    """Web-adapted single-player game against AI"""
    def __init__(self, tuomari, tekoaly):
        self.tuomari = tuomari
        self.tekoaly = tekoaly
    
    def _onko_ok_siirto(self, siirto):
        return siirto in ("k", "p", "s")
    
    def pelaa_kierros(self, pelaaja_siirto):
        if self._onko_ok_siirto(pelaaja_siirto):
            tietokoneen_siirto = self.tekoaly.anna_siirto()
            self.tuomari.kirjaa_siirto(pelaaja_siirto, tietokoneen_siirto)
            self.tekoaly.aseta_siirto(pelaaja_siirto)
            return tietokoneen_siirto
        return None


def init_game(game_type):
    """Initialize a new game session"""
    session['game_type'] = game_type
    session['tuomari'] = {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0
    }
    session['historia'] = []
    session['peli_paattynyt'] = False
    session['voittaja'] = None
    
    if game_type in ['yksinpeli', 'haastava_yksinpeli']:
        session['tekoaly_muisti'] = []
        session['tekoaly_siirto'] = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/valitse/<game_type>')
def valitse_peli(game_type):
    if game_type not in ['kaksinpeli', 'yksinpeli', 'haastava_yksinpeli']:
        return redirect(url_for('index'))
    
    init_game(game_type)
    return redirect(url_for('pelaa'))


@app.route('/pelaa', methods=['GET', 'POST'])
def pelaa():
    if 'game_type' not in session:
        return redirect(url_for('index'))
    
    game_type = session['game_type']
    
    if request.method == 'POST':
        pelaaja1_siirto = request.form.get('pelaaja1_siirto')
        
        # Recreate tuomari from session
        tuomari = Tuomari()
        tuomari.ekan_pisteet = session['tuomari']['ekan_pisteet']
        tuomari.tokan_pisteet = session['tuomari']['tokan_pisteet']
        tuomari.tasapelit = session['tuomari']['tasapelit']
        
        if game_type == 'kaksinpeli':
            pelaaja2_siirto = request.form.get('pelaaja2_siirto')
            peli = WebKPSPelaajaVsPelaaja(tuomari)
            
            if peli.pelaa_kierros(pelaaja1_siirto, pelaaja2_siirto):
                session['historia'].append({
                    'pelaaja1': pelaaja1_siirto,
                    'pelaaja2': pelaaja2_siirto
                })
        
        elif game_type == 'yksinpeli':
            from tekoaly import Tekoaly
            tekoaly = Tekoaly()
            tekoaly._siirto = session.get('tekoaly_siirto', 0)
            
            peli = WebKPSTekoaly(tuomari, tekoaly)
            tietokoneen_siirto = peli.pelaa_kierros(pelaaja1_siirto)
            
            if tietokoneen_siirto:
                session['historia'].append({
                    'pelaaja1': pelaaja1_siirto,
                    'pelaaja2': tietokoneen_siirto
                })
                session['tekoaly_siirto'] = tekoaly._siirto
        
        elif game_type == 'haastava_yksinpeli':
            from tekoaly import TekoalyParannettu
            tekoaly = TekoalyParannettu(10)
            tekoaly._muisti = session.get('tekoaly_muisti', [None] * 10)
            tekoaly._vapaa_muisti_indeksi = len([x for x in tekoaly._muisti if x is not None])
            
            peli = WebKPSTekoaly(tuomari, tekoaly)
            tietokoneen_siirto = peli.pelaa_kierros(pelaaja1_siirto)
            
            if tietokoneen_siirto:
                session['historia'].append({
                    'pelaaja1': pelaaja1_siirto,
                    'pelaaja2': tietokoneen_siirto
                })
                session['tekoaly_muisti'] = tekoaly._muisti
        
        # Update session with tuomari state
        session['tuomari'] = {
            'ekan_pisteet': tuomari.ekan_pisteet,
            'tokan_pisteet': tuomari.tokan_pisteet,
            'tasapelit': tuomari.tasapelit
        }
        
        # Check if game is over
        session['peli_paattynyt'] = tuomari.peli_paattynyt()
        session['voittaja'] = tuomari.voittaja()
        session.modified = True
    
    return render_template('pelaa.html', 
                         game_type=game_type,
                         tuomari=session['tuomari'],
                         historia=session.get('historia', []),
                         peli_paattynyt=session.get('peli_paattynyt', False),
                         voittaja=session.get('voittaja'))


@app.route('/lopeta')
def lopeta():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
