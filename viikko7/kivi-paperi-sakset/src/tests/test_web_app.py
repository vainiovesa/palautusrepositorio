"""Unit tests for Flask web application"""
import pytest
from web_app import app, init_game, WebKPSPelaajaVsPelaaja, WebKPSTekoaly
from tuomari import Tuomari
from tekoaly import Tekoaly, TekoalyParannettu


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client


@pytest.fixture
def session_client():
    """Create test client with session support"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['game_type'] = 'kaksinpeli'
            sess['tuomari'] = {
                'ekan_pisteet': 0,
                'tokan_pisteet': 0,
                'tasapelit': 0
            }
            sess['historia'] = []
        yield client


class TestRoutes:
    def test_index_route(self, client):
        """Test index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Tervetuloa pelaamaan' in response.data

    def test_valitse_kaksinpeli(self, client):
        """Test selecting two-player mode"""
        response = client.get('/valitse/kaksinpeli', follow_redirects=False)
        assert response.status_code == 302
        assert '/pelaa' in response.location

    def test_valitse_yksinpeli(self, client):
        """Test selecting single-player mode"""
        response = client.get('/valitse/yksinpeli', follow_redirects=False)
        assert response.status_code == 302
        assert '/pelaa' in response.location

    def test_valitse_haastava_yksinpeli(self, client):
        """Test selecting advanced AI mode"""
        response = client.get('/valitse/haastava_yksinpeli', follow_redirects=False)
        assert response.status_code == 302
        assert '/pelaa' in response.location

    def test_valitse_invalid_game_type(self, client):
        """Test invalid game type redirects to index"""
        response = client.get('/valitse/invalid', follow_redirects=False)
        assert response.status_code == 302
        assert response.location == '/'

    def test_pelaa_without_session_redirects(self, client):
        """Test playing without session redirects to index"""
        response = client.get('/pelaa', follow_redirects=False)
        assert response.status_code == 302
        assert response.location == '/'

    def test_pelaa_with_session(self, session_client):
        """Test playing with valid session"""
        response = session_client.get('/pelaa')
        assert response.status_code == 200
        assert b'Tilanne' in response.data

    def test_lopeta_clears_session(self, session_client):
        """Test ending game clears session"""
        response = session_client.get('/lopeta', follow_redirects=False)
        assert response.status_code == 302
        assert response.location == '/'

    def test_kaksinpeli_post(self, session_client):
        """Test posting moves in two-player mode"""
        response = session_client.post('/pelaa', data={
            'pelaaja1_siirto': 'k',
            'pelaaja2_siirto': 's'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_kaksinpeli_full_game_flow(self, client):
        """Test complete two-player game flow"""
        # Select game mode
        response = client.get('/valitse/kaksinpeli', follow_redirects=True)
        assert response.status_code == 200
        
        # Play a round
        response = client.post('/pelaa', data={
            'pelaaja1_siirto': 'k',
            'pelaaja2_siirto': 's'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_yksinpeli_post(self, client):
        """Test posting move in single-player mode"""
        # Initialize single-player game
        client.get('/valitse/yksinpeli')
        
        response = client.post('/pelaa', data={
            'pelaaja1_siirto': 'k'
        }, follow_redirects=True)
        assert response.status_code == 200


class TestInitGame:
    def test_init_kaksinpeli(self, client):
        """Test initializing two-player game"""
        client.get('/valitse/kaksinpeli')
        with client.session_transaction() as sess:
            assert sess['game_type'] == 'kaksinpeli'
            assert sess['tuomari']['ekan_pisteet'] == 0
            assert sess['tuomari']['tokan_pisteet'] == 0
            assert sess['tuomari']['tasapelit'] == 0
            assert sess['historia'] == []

    def test_init_yksinpeli(self, client):
        """Test initializing single-player game"""
        client.get('/valitse/yksinpeli')
        with client.session_transaction() as sess:
            assert sess['game_type'] == 'yksinpeli'
            assert 'tekoaly_siirto' in sess

    def test_init_haastava_yksinpeli(self, client):
        """Test initializing advanced AI game"""
        client.get('/valitse/haastava_yksinpeli')
        with client.session_transaction() as sess:
            assert sess['game_type'] == 'haastava_yksinpeli'
            assert 'tekoaly_muisti' in sess


class TestWebKPSPelaajaVsPelaaja:
    def test_luonti(self):
        """Test creating web two-player game"""
        tuomari = Tuomari()
        peli = WebKPSPelaajaVsPelaaja(tuomari)
        assert peli.tuomari == tuomari

    def test_onko_ok_siirto(self):
        """Test valid move checking"""
        tuomari = Tuomari()
        peli = WebKPSPelaajaVsPelaaja(tuomari)
        
        assert peli._onko_ok_siirto("k") == True
        assert peli._onko_ok_siirto("p") == True
        assert peli._onko_ok_siirto("s") == True
        assert peli._onko_ok_siirto("x") == False

    def test_pelaa_kierros_valid(self):
        """Test playing a valid round"""
        tuomari = Tuomari()
        peli = WebKPSPelaajaVsPelaaja(tuomari)
        
        result = peli.pelaa_kierros("k", "s")
        assert result == True
        assert tuomari.ekan_pisteet == 1

    def test_pelaa_kierros_invalid(self):
        """Test playing with invalid moves"""
        tuomari = Tuomari()
        peli = WebKPSPelaajaVsPelaaja(tuomari)
        
        result = peli.pelaa_kierros("x", "s")
        assert result == False
        assert tuomari.ekan_pisteet == 0


class TestWebKPSTekoaly:
    def test_luonti(self):
        """Test creating web AI game"""
        tuomari = Tuomari()
        tekoaly = Tekoaly()
        peli = WebKPSTekoaly(tuomari, tekoaly)
        
        assert peli.tuomari == tuomari
        assert peli.tekoaly == tekoaly

    def test_pelaa_kierros_valid(self):
        """Test playing a valid round against AI"""
        tuomari = Tuomari()
        tekoaly = Tekoaly()
        peli = WebKPSTekoaly(tuomari, tekoaly)
        
        tietokoneen_siirto = peli.pelaa_kierros("k")
        assert tietokoneen_siirto in ["k", "p", "s"]

    def test_pelaa_kierros_invalid(self):
        """Test playing with invalid move"""
        tuomari = Tuomari()
        tekoaly = Tekoaly()
        peli = WebKPSTekoaly(tuomari, tekoaly)
        
        tietokoneen_siirto = peli.pelaa_kierros("x")
        assert tietokoneen_siirto is None
        assert tuomari.ekan_pisteet == 0

    def test_tekoaly_oppii_parannettu(self):
        """Test that advanced AI learns from moves"""
        tuomari = Tuomari()
        tekoaly = TekoalyParannettu(10)
        peli = WebKPSTekoaly(tuomari, tekoaly)
        
        # Play several rounds
        for _ in range(5):
            peli.pelaa_kierros("k")
        
        # Memory should contain moves
        assert tekoaly._vapaa_muisti_indeksi > 0


class TestGameLogic:
    def test_kaksinpeli_player1_wins(self, client):
        """Test player 1 winning in two-player mode"""
        client.get('/valitse/kaksinpeli')
        client.post('/pelaa', data={
            'pelaaja1_siirto': 'k',
            'pelaaja2_siirto': 's'
        })
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['ekan_pisteet'] == 1
            assert sess['tuomari']['tokan_pisteet'] == 0

    def test_kaksinpeli_player2_wins(self, client):
        """Test player 2 winning in two-player mode"""
        client.get('/valitse/kaksinpeli')
        client.post('/pelaa', data={
            'pelaaja1_siirto': 's',
            'pelaaja2_siirto': 'k'
        })
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['ekan_pisteet'] == 0
            assert sess['tuomari']['tokan_pisteet'] == 1

    def test_kaksinpeli_tie(self, client):
        """Test tie in two-player mode"""
        client.get('/valitse/kaksinpeli')
        client.post('/pelaa', data={
            'pelaaja1_siirto': 'k',
            'pelaaja2_siirto': 'k'
        })
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['tasapelit'] == 1

    def test_historia_tallentuu(self, client):
        """Test that game history is saved"""
        client.get('/valitse/kaksinpeli')
        client.post('/pelaa', data={
            'pelaaja1_siirto': 'k',
            'pelaaja2_siirto': 's'
        })
        
        with client.session_transaction() as sess:
            assert len(sess['historia']) == 1
            assert sess['historia'][0]['pelaaja1'] == 'k'
            assert sess['historia'][0]['pelaaja2'] == 's'
