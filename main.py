import numpy as np

# Definiujemy nasze dane
wagi = np.array([4, 6, 14, 2, 15, 3, 8, 16, 4, 12])
wartosci = np.array([12, 3, 3, 12, 14, 15, 12, 3, 1, 10])
waga_max = 68


# Stworzenie klasy Osobnik
class Osobnik:
    def __init__(self, genotyp=None):
        if genotyp is None:  # jeśli nie podano genotypu, losujemy go
            genotyp = np.random.randint(2, size=10)  # losowy ciąg 10 bitów
        self.genotyp = genotyp
        self.fenotyp = self.genotyp * wagi  # wagi przedmiotów w plecaku
        self.wartosc = sum(self.genotyp * wartosci)  # suma wartości przedmiotów w plecaku
        self.waga = sum(self.fenotyp)  # suma wag przedmiotów w plecaku
        self.ocena = self.wartosc if self.waga <= waga_max else 0  # dodajemy funkcję oceny


# Stworzenie populacji początkowej
def stworz_populacje(rozmiar_populacji):
    return [Osobnik() for _ in range(rozmiar_populacji)]


populacja = stworz_populacje(20)


def suma_ocen(populacja_do_oceny):
    return sum([osobnik.ocena for osobnik in populacja_do_oceny])


def selekcja_ruletka(populacja_do_selekcji):
    suma = suma_ocen(populacja_do_selekcji)
    los = np.random.uniform(0, suma)  # losujemy liczbę
    aktualna_suma = 0
    for osobnik in populacja_do_selekcji:
        aktualna_suma += osobnik.ocena
        if aktualna_suma > los:  # zwracamy pierwszego osobnika, dla którego suma ocen przekroczyła wylosowaną liczbę
            return osobnik


def krzyzowanie(osobnik1, osobnik2):
    punkt = np.random.randint(10)  # losujemy punkt krzyżowania
    genotyp_dziecka1 = np.concatenate((osobnik1.genotyp[:punkt], osobnik2.genotyp[punkt:]))  # tworzymy pierwsze dziecko
    genotyp_dziecka2 = np.concatenate((osobnik2.genotyp[:punkt], osobnik1.genotyp[punkt:]))  # tworzymy drugie dziecko
    return Osobnik(genotyp_dziecka1), Osobnik(genotyp_dziecka2)  # zwracamy nowe osobniki


def mutacja(osobnik):
    prawdopodobienstwo = 0.1  # prawdopodobieństwo mutacji
    for i in range(len(osobnik.genotyp)):
        if np.random.random() < prawdopodobienstwo:  # losujemy liczbę i jeśli jest mniejsza od prawdopodobieństwa,
            # mutujemy gen
            osobnik.genotyp[i] = 1 - osobnik.genotyp[i]  # zmieniamy 0 na 1 lub 1 na 0
            # po mutacji musimy zaktualizować fenotyp, wartość, wagę i ocenę osobnika
            osobnik.fenotyp = osobnik.genotyp * wagi
            osobnik.wartosc = sum(osobnik.genotyp * wartosci)
            osobnik.waga = sum(osobnik.fenotyp)
            osobnik.ocena = osobnik.wartosc if osobnik.waga <= waga_max else 0


def nowe_pokolenie(stara_populacja):
    nowa_populacja = []
    # dodajemy 5 najlepszych osobników z poprzedniego pokolenia
    nowa_populacja.extend(sorted(stara_populacja, key=lambda osobnik: osobnik.ocena, reverse=True)[:5])
    while len(nowa_populacja) < 20:  # dopóki nie mamy pełnej nowej populacji
        rodzic1, rodzic2 = selekcja_ruletka(stara_populacja), selekcja_ruletka(stara_populacja)  # wybieramy rodziców
        if np.random.random() < 0.8:  # z prawdopodobieństwem 0,8 przeprowadzamy krzyżowanie
            dziecko1, dziecko2 = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko1)  # przeprowadzamy mutację na dzieciach
            mutacja(dziecko2)
            nowa_populacja.append(dziecko1)  # dodajemy dzieci do nowej populacji
            if len(nowa_populacja) < 20:  # upewniamy się, że nie przekroczymy rozmiaru populacji
                nowa_populacja.append(dziecko2)
    return nowa_populacja  # zwracamy nową populację


populacja = nowe_pokolenie(populacja)  # pierwsza iteracja
populacja = nowe_pokolenie(populacja)  # druga iteracja

najlepszy_osobnik = max(populacja, key=lambda osobnik: osobnik.ocena)
print(f'Najlepszy osobnik ma genotyp: {najlepszy_osobnik.genotyp}')
print(f'Wartość przedmiotów w plecaku: {najlepszy_osobnik.wartosc}')
print(f'Waga przedmiotów w plecaku: {najlepszy_osobnik.waga}')
