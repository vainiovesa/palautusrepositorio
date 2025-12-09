from tuomari import Tuomari
from tekoaly import Tekoaly, TekoalyParannettu
from enum import Enum


MUISTIN_KOKO = 10


class Pelit(Enum):
    KAKSINPELI = 1
    YKSINPELI = 2
    HAASTAVA_YKSINPELI = 3


class KiviPaperiSakset:
    def pelaa(self):
        tuomari = Tuomari()

        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto(ekan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = self._ensimmaisen_siirto()
            tokan_siirto = self._toisen_siirto(ekan_siirto)

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    def _toisen_siirto(self, ensimmaisen_siirto):
        raise Exception("Tämä metodi pitää korvata aliluokassa")

    def _onko_ok_siirto(self, siirto):
        return siirto in ("k", "p", "s")


class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = input("Toisen pelaajan siirto: ")

        return tokan_siirto


class KPSTekoaly(KiviPaperiSakset):
    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = self.tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        self.tekoaly.aseta_siirto(ensimmaisen_siirto)

        return tokan_siirto


class KPSHuonompiTekoaly(KPSTekoaly):
    def __init__(self):
        self.tekoaly = Tekoaly()


class KPSParempiTekoaly(KPSTekoaly):
    def __init__(self):
        self.tekoaly = TekoalyParannettu(MUISTIN_KOKO)


def luo_peli(pelivalinta):
    pelit = {
        Pelit.KAKSINPELI: KPSPelaajaVsPelaaja(),
        Pelit.YKSINPELI: KPSHuonompiTekoaly(),
        Pelit.HAASTAVA_YKSINPELI: KPSParempiTekoaly()
    }

    peli = pelit[pelivalinta]
    peli.pelaa()
