from kps import Pelit, luo_peli

def main():
    valinnat = {
        "a": Pelit.KAKSINPELI,
        "b": Pelit.YKSINPELI,
        "c": Pelit.HAASTAVA_YKSINPELI
    }

    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()

        if any(vastaus.endswith(letter) for letter in ("a", "b", "c")):
            vastaus = vastaus[-1]
            print(
                "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
            )
            luo_peli(valinnat[vastaus])
        else:
            break


if __name__ == "__main__":
    main()
