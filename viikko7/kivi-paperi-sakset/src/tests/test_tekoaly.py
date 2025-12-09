"""Unit tests for Tekoaly classes"""
import pytest
from tekoaly import Tekoaly, TekoalyParannettu


class TestTekoaly:
    def setup_method(self):
        """Setup test fixtures"""
        self.tekoaly = Tekoaly()

    def test_tekoaly_alkutila(self):
        """Test initial state of Tekoaly"""
        assert self.tekoaly._siirto == 0

    def test_tekoaly_anna_siirto_sykli(self):
        """Test that Tekoaly cycles through moves"""
        # First move should be paper (p) since counter starts at 0 and increments to 1
        siirto1 = self.tekoaly.anna_siirto()
        assert siirto1 == "p"
        
        # Second move should be scissors (s)
        siirto2 = self.tekoaly.anna_siirto()
        assert siirto2 == "s"
        
        # Third move should be rock (k)
        siirto3 = self.tekoaly.anna_siirto()
        assert siirto3 == "k"
        
        # Fourth move should cycle back to paper (p)
        siirto4 = self.tekoaly.anna_siirto()
        assert siirto4 == "p"

    def test_tekoaly_aseta_siirto_ei_muuta_tilaa(self):
        """Test that aseta_siirto doesn't change state"""
        initial_siirto = self.tekoaly._siirto
        self.tekoaly.aseta_siirto("k")
        assert self.tekoaly._siirto == initial_siirto
        
        self.tekoaly.aseta_siirto("p")
        assert self.tekoaly._siirto == initial_siirto

    def test_tekoaly_pitka_pelisarja(self):
        """Test a long series of moves"""
        odotetut_siirrot = ["p", "s", "k", "p", "s", "k", "p", "s", "k"]
        
        for odotettu in odotetut_siirrot:
            siirto = self.tekoaly.anna_siirto()
            assert siirto == odotettu


class TestTekoalyParannettu:
    def setup_method(self):
        """Setup test fixtures"""
        self.muistin_koko = 10
        self.tekoaly = TekoalyParannettu(self.muistin_koko)

    def test_tekoaly_parannettu_alkutila(self):
        """Test initial state of TekoalyParannettu"""
        assert len(self.tekoaly._muisti) == self.muistin_koko
        assert self.tekoaly._vapaa_muisti_indeksi == 0
        assert all(item is None for item in self.tekoaly._muisti)

    def test_anna_siirto_alkutilassa(self):
        """Test move at initial state (should return 'k')"""
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_aseta_siirto_tallentaa_muistiin(self):
        """Test that aseta_siirto saves moves to memory"""
        self.tekoaly.aseta_siirto("k")
        assert self.tekoaly._muisti[0] == "k"
        assert self.tekoaly._vapaa_muisti_indeksi == 1
        
        self.tekoaly.aseta_siirto("p")
        assert self.tekoaly._muisti[1] == "p"
        assert self.tekoaly._vapaa_muisti_indeksi == 2

    def test_anna_siirto_yhden_siirron_jalkeen(self):
        """Test move after one stored move"""
        self.tekoaly.aseta_siirto("k")
        siirto = self.tekoaly.anna_siirto()
        # With only one move in memory, should return 'k'
        assert siirto == "k"

    def test_muisti_tayttyy_ja_pyyhkiytyy(self):
        """Test that memory fills up and oldest items are removed"""
        # Fill memory completely
        siirrot = ["k", "p", "s", "k", "p", "s", "k", "p", "s", "k"]
        for siirto in siirrot:
            self.tekoaly.aseta_siirto(siirto)
        
        assert self.tekoaly._vapaa_muisti_indeksi == self.muistin_koko
        assert self.tekoaly._muisti[0] == "k"
        assert self.tekoaly._muisti[-1] == "k"
        
        # Add one more - should remove first item
        self.tekoaly.aseta_siirto("p")
        assert self.tekoaly._vapaa_muisti_indeksi == self.muistin_koko
        assert self.tekoaly._muisti[0] == "p"  # First item shifted
        assert self.tekoaly._muisti[-1] == "p"  # New item at end

    def test_tekoaly_oppii_kuvioita(self):
        """Test that AI learns patterns"""
        # Create a pattern: after 'k', player always plays 'p'
        pelisarja = [
            ("k", "p"),  # Player plays k, then p
            ("k", "p"),  # Pattern repeats
            ("k", "p"),  # Pattern repeats again
        ]
        
        for pelaaja_siirto, _ in pelisarja:
            self.tekoaly.aseta_siirto(pelaaja_siirto)
            self.tekoaly.anna_siirto()
            self.tekoaly.aseta_siirto(_)
            
        # Now after 'k', AI should predict 'p' and counter with 's'
        self.tekoaly.aseta_siirto("k")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"  # Scissors beats paper

    def test_eri_muistikoot(self):
        """Test different memory sizes"""
        for koko in [5, 10, 15, 20]:
            tekoaly = TekoalyParannettu(koko)
            assert len(tekoaly._muisti) == koko
            assert tekoaly._vapaa_muisti_indeksi == 0

    def test_anna_siirto_palauttaa_oikean_vastauksen_kivi_eniten(self):
        """Test that AI returns paper when rock is most common"""
        # Simulate pattern where player plays rock most after rock
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("k")
        
        siirto = self.tekoaly.anna_siirto()
        # Should counter with paper (p beats k)
        assert siirto == "p"

    def test_anna_siirto_palauttaa_oikean_vastauksen_paperi_eniten(self):
        """Test that AI returns scissors when paper is most common"""
        # Setup pattern where paper follows rock
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.aseta_siirto("k")
        
        siirto = self.tekoaly.anna_siirto()
        # Should predict paper and counter with scissors
        assert siirto == "s"

    def test_muisti_sailyy_oikein_tayton_jalkeen(self):
        """Test that memory order is preserved after filling"""
        # Add 15 items to 10-item memory
        siirrot = ["k", "p", "s", "k", "p", "s", "k", "p", "s", "k", "p", "s", "k", "p", "s"]
        for siirto in siirrot:
            self.tekoaly.aseta_siirto(siirto)
        
        # Last 10 items should be in memory
        odotettu_muisti = siirrot[-10:]
        assert self.tekoaly._muisti == odotettu_muisti
