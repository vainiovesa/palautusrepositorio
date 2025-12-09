"""Unit tests for Tuomari class"""
import pytest
from tuomari import Tuomari


class TestTuomari:
    def setup_method(self):
        """Setup test fixtures"""
        self.tuomari = Tuomari()

    def test_tuomari_alkutila(self):
        """Test initial state of Tuomari"""
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_tasapeli_kivi_kivi(self):
        """Test tie with rock vs rock"""
        self.tuomari.kirjaa_siirto("k", "k")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0

    def test_tasapeli_paperi_paperi(self):
        """Test tie with paper vs paper"""
        self.tuomari.kirjaa_siirto("p", "p")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0

    def test_tasapeli_sakset_sakset(self):
        """Test tie with scissors vs scissors"""
        self.tuomari.kirjaa_siirto("s", "s")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0

    def test_eka_voittaa_kivi_sakset(self):
        """Test first player wins with rock vs scissors"""
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_sakset_paperi(self):
        """Test first player wins with scissors vs paper"""
        self.tuomari.kirjaa_siirto("s", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_paperi_kivi(self):
        """Test first player wins with paper vs rock"""
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_sakset_kivi(self):
        """Test second player wins with scissors vs rock"""
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_paperi_sakset(self):
        """Test second player wins with paper vs scissors"""
        self.tuomari.kirjaa_siirto("p", "s")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_kivi_paperi(self):
        """Test second player wins with rock vs paper"""
        self.tuomari.kirjaa_siirto("k", "p")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_usean_kierroksen_tulokset(self):
        """Test multiple rounds"""
        # Round 1: Player 1 wins
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

        # Round 2: Player 2 wins
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

        # Round 3: Tie
        self.tuomari.kirjaa_siirto("p", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 1

        # Round 4: Player 1 wins
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 2
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 1

    def test_str_representation(self):
        """Test string representation of Tuomari"""
        self.tuomari.kirjaa_siirto("k", "s")
        self.tuomari.kirjaa_siirto("p", "p")
        
        expected = "Pelitilanne: 1 - 0\nTasapelit: 1"
        assert str(self.tuomari) == expected

    def test_str_representation_alkutila(self):
        """Test string representation at initial state"""
        expected = "Pelitilanne: 0 - 0\nTasapelit: 0"
        assert str(self.tuomari) == expected
