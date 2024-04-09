#importálok modulokat
from abc import ABC, abstractmethod #absztrakt class és annak metódusa
from datetime import datetime #dátum modul


#osztalyok
#letrehozom a Szobak osztalyt a tulajdonsagaival
class Szobak(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
    
    @abstractmethod
    def get_ar(self):
        pass


#letrehozom az Egyagyasszobat, ami megorokli a Szobak osztaly tulajdonsagait es visszaadja az egyegyas szobanak az arat,
#amit alapbol adtam neki
class EgyagyasSzoba(Szobak):
    def __init__(self, szobaszam):
        super().__init__(ar=10000, szobaszam=szobaszam)
    
    def get_ar(self):
        return self.ar


#letrehozom a Ketagyasszobat, ami megorokli a Szobak osztaly tulajdonsagait es visszaadja a ketagyas szoba alaparat
#amit adtam neki
class KetagyasSzoba(Szobak):
    def __init__(self, szobaszam):
        super().__init__(ar=15000, szobaszam=szobaszam)
    
    def get_ar(self):
        return self.ar


#letrehozom magat a Szalloda osztalyat a tulajdonsagaival egyutt
#vannak benne tombok is, amik magat a szobakat (azok adatait) es a foglalasokat tartalmazzak, amint beletoltodik
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)
        #itt teszem a listaba a szobat

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum,)
                self.foglalasok.append(foglalas)
                return foglalas
        return None
    #itt teszem bele a foglalas listaba a foglalast, vegig iteralok a szobak listan es ha az i. elemnek(szoba) szobaszama megegyezik az Egyagyas vagy Ketagyas 
    #szoba szobaszamaval, akkor a foglalas az maga a Foglalas classnak a szoba es datum adata lesz, amit pedig a foglalasok listaba (tulajdonsagba) tolt bele

    def lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            #ez magaert beszel, lemondas eseten egy if-el atellenorzom a foglalasok listat es eltavolitom az adott foglalast
            
    def listaz_foglalasok(self):
        for foglalas in self.foglalasok:
            print(f"Foglalás: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")
            #egy for ciklussal vegig megyek a foglalasok listan, az i. elem lesz a foglalas es kiiratom a foglalasnak as szobaszamat es a datumat


#letrehozom a foglalas class-t, aminek szoba es datum tulajdonsagai vannak
class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum
        


#a mainre letrehozok egy fuggvenyt, hogy ha elinditom a programot, akkor automatikusan hozza letre ezeket
def main():
    szalloda = Szalloda("Példa Szálloda")
    szalloda.add_szoba(EgyagyasSzoba("101"))
    szalloda.add_szoba(EgyagyasSzoba("102"))
    szalloda.add_szoba(EgyagyasSzoba("103"))
    szalloda.add_szoba(KetagyasSzoba("201"))
    szalloda.add_szoba(KetagyasSzoba("202"))
    szalloda.add_szoba(KetagyasSzoba("203"))
    #szobakbol 3-3-at keszitek el

    today = datetime.now().strftime("%Y-%m-%d") #adott napi datum
    szalloda.foglalas("101", today) #a megjelolt szobakra adott napi datumra van foglalas
    szalloda.foglalas("102", "2024-03-26") #a megjelolt szobakra a megadott napokra van foglalas
    szalloda.foglalas("103", "2024-03-27")
    szalloda.foglalas("201", today)
    szalloda.foglalas("202", "2024-03-26") 
    #szalloda.foglalas("203", itt lehetne today, vagy egy datum de ezt uresen hagytam hogy lehessen ra foglalni)

    while True:
        #ezek a lehetosegek a user interface szempontjabol
        print("\n1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("0. Kilépés")
        choice = input("Válasszon egy műveletet: ")

    #ha az 1-est választja, akkor a foglalás fog lefutni
        if choice == "1":
            szobaszam = input("Adja meg a szoba számát: ")
            datum = input("Adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN): ")
            foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
            if foglalas_datum >= datetime.now():
                foglalas = szalloda.foglalas(szobaszam, datum)
                if foglalas:
                    print(f"Sikeres foglalás a szobára {szobaszam} a {datum} dátumra, a fizetendő összeg pedig:  ")
                else:
                    print("Hiba: A megadott szoba nem található vagy foglalt.")
            else:
                print("Hiba: Nem megfelelő dátum.")
        
    #ha a 2-est választja, akkor a foglalást lehet lemondani
        elif choice == "2":
            foglalas_szoba = input("Adja meg a foglalt szoba számát: ")
            foglalas_datum = input("Adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN): ")
            foglalas = None
            for fog in szalloda.foglalasok:
                if fog.szoba.szobaszam == foglalas_szoba and fog.datum == foglalas_datum:
                    foglalas = fog
                    break
            if foglalas:
                szalloda.lemondas(foglalas)
                print("Sikeres lemondás.")
            else:
                print("Hiba: A megadott foglalás nem található.")
        
    #ha a 3-ast választja, akkor kilistázódnak a foglalások
        elif choice == "3":
            szalloda.listaz_foglalasok()

    #ha a 4-est választja, akkor kilép az egészből
        elif choice == "0":
            print("Kilépés...")
            break
    
    #ha mást választ, akkor így kezeli a "hibát"
        else:
            print("Hibás választás. Kérem válasszon újra.")


if __name__ == "__main__":
    main()
