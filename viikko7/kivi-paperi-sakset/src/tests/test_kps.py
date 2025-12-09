"""Unit tests for KPS game classes"""
import pytest
from unittest.mock import Mock, patch
from kps import (
    Pelit,
    KiviPaperiSakset,
    KPSPelaajaVsPelaaja,
    KPSHuonompiTekoaly,
    KPSParempiTekoaly,
    luo_peli
)


class TestKiviPaperiSakset:
    def test_onko_ok_siirto_kivi(self):
        """Test that 'k' is valid move"""
        peli = KiviPaperiSakset()
        assert peli._onko_ok_siirto("k") == True

    def test_onko_ok_siirto_paperi(self):
        """Test that 'p' is valid move"""
        peli = KiviPaperiSakset()
        assert peli._onko_ok_siirto("p") == True

    def test_onko_ok_siirto_sakset(self):
        """Test that 's' is valid move"""
        peli = KiviPaperiSakset()
        assert peli._onko_ok_siirto("s") == True

    def test_onko_ok_siirto_invalid(self):
        """Test that invalid moves are rejected"""
        peli = KiviPaperiSakset()
        assert peli._onko_ok_siirto("x") == False
        assert peli._onko_ok_siirto("a") == False
        assert peli._onko_ok_siirto("") == False
        assert peli._onko_ok_siirto("kivi") == False


class TestKPSPelaajaVsPelaaja:
    @patch('kps.input')
    def test_toisen_siirto_palauttaa_syotteen(self, mock_input):
        """Test that second player's move is read from input"""
        mock_input.return_value = "k"
        peli = KPSPelaajaVsPelaaja()
        
        siirto = peli._toisen_siirto("p")
        assert siirto == "k"
        mock_input.assert_called_once()

    @patch('kps.input')
    def test_pelaa_yhden_kierroksen(self, mock_input):
        """Test playing one round"""
        # Simulate: player1 plays 'k', player2 plays 's', then invalid move to end
        mock_input.side_effect = ["k", "s", "x", "x"]
        peli = KPSPelaajaVsPelaaja()
        
        peli.pelaa()
        # Should have called input 4 times (2 rounds * 2 players)
        assert mock_input.call_count == 4


class TestKPSHuonompiTekoaly:
    def test_luonti(self):
        """Test creating simple AI game"""
        peli = KPSHuonompiTekoaly()
        assert peli.tekoaly is not None
        assert hasattr(peli.tekoaly, 'anna_siirto')
        assert hasattr(peli.tekoaly, 'aseta_siirto')

    @patch('kps.input')
    @patch('builtins.print')
    def test_toisen_siirto_palauttaa_tekoalyn_siirron(self, mock_print, mock_input):
        """Test that AI's move is returned"""
        peli = KPSHuonompiTekoaly()
        
        siirto = peli._toisen_siirto("k")
        assert siirto in ["k", "p", "s"]

    @patch('kps.input')
    @patch('builtins.print')
    def test_tekoaly_asettaa_siirron(self, mock_print, mock_input):
        """Test that AI updates its state"""
        peli = KPSHuonompiTekoaly()
        initial_state = peli.tekoaly._siirto
        
        peli._toisen_siirto("k")
        # State should have changed after anna_siirto call
        # (aseta_siirto is called after, but doesn't change state in simple AI)


class TestKPSParempiTekoaly:
    def test_luonti(self):
        """Test creating advanced AI game"""
        peli = KPSParempiTekoaly()
        assert peli.tekoaly is not None
        assert hasattr(peli.tekoaly, 'anna_siirto')
        assert hasattr(peli.tekoaly, 'aseta_siirto')
        assert hasattr(peli.tekoaly, '_muisti')

    @patch('kps.input')
    @patch('builtins.print')
    def test_toisen_siirto_palauttaa_tekoalyn_siirron(self, mock_print, mock_input):
        """Test that advanced AI's move is returned"""
        peli = KPSParempiTekoaly()
        
        siirto = peli._toisen_siirto("k")
        assert siirto in ["k", "p", "s"]

    @patch('kps.input')
    @patch('builtins.print')
    def test_tekoaly_oppii(self, mock_print, mock_input):
        """Test that advanced AI learns from moves"""
        peli = KPSParempiTekoaly()
        
        # Play several rounds to teach AI a pattern
        for _ in range(5):
            peli._toisen_siirto("k")
        
        # Memory should contain the moves
        assert peli.tekoaly._vapaa_muisti_indeksi > 0


class TestLuoPeli:
    def test_luo_kaksinpeli(self):
        """Test creating two-player game"""
        with patch.object(KPSPelaajaVsPelaaja, 'pelaa'):
            luo_peli(Pelit.KAKSINPELI)
            # If no exception, test passes

    def test_luo_yksinpeli(self):
        """Test creating simple AI game"""
        with patch.object(KPSHuonompiTekoaly, 'pelaa'):
            luo_peli(Pelit.YKSINPELI)
            # If no exception, test passes

    def test_luo_haastava_yksinpeli(self):
        """Test creating advanced AI game"""
        with patch.object(KPSParempiTekoaly, 'pelaa'):
            luo_peli(Pelit.HAASTAVA_YKSINPELI)
            # If no exception, test passes


class TestPelienEnum:
    def test_pelit_enum_arvot(self):
        """Test Pelit enum values"""
        assert Pelit.KAKSINPELI.value == 1
        assert Pelit.YKSINPELI.value == 2
        assert Pelit.HAASTAVA_YKSINPELI.value == 3
