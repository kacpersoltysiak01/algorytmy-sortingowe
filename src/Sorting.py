import random
import time

# --------------------
# Funkcje sortujące
# --------------------

def InsertSort(_list):			#Funkcja sortujaca przez wstawianie
    for i in range(1, len(_list)):		#iteracja od drugiego elementu
        temp = _list[i]			#chwilowe zapamietanie biezacego elementu
        j = i - 1
        while j >= 0 and _list[j] > temp: 		#przesuwamy wieksze elementy w prawo
            _list[j + 1] = _list[j]
            j -= 1
        _list[j + 1] = temp			#wstawiamy element na wlasciwe miejsce

def BubbleSort(_list):			#funckja sortowania babelkowego 
    n = len(_list)				#dlugosc listy
    for i in range(n):
        for j in range(0, n - i - 1):		#porownanie elementow sasiadujacych
            if _list[j] > _list[j + 1]:		#jesli sa w zlej kolejnosci
                _list[j], _list[j + 1], = _list[j + 1], _list[j]		#zamiana

def Partition(_list, _start, _stop):				# funkcja podzialu do QuickSorta
    pivot_index = random.randint(_start, _stop)		#losowy pivot
    _list[pivot_index], _list[_stop] = _list[_stop], _list[pivot_index]		#liczba przebiegow
    pivot = _list[_stop]		#zapamietanie pivota
    i = _start
    for j in range(_start, _stop):			#iteracja po liscie
        if _list[j] < pivot or (_list[j] == pivot and random.randint(0, 2) == 1):			#1/3 szansy na przesuniecie
            _list[i], _list[j] = _list[j], _list[i]		#zamiana
            i += 1
    _list[i], _list[_stop] = _list[_stop], _list[i]
    return i			#zwrot pozycji pivota

def QuickSortR(_list, _start, _stop): 		#rekurencyjna wersja QuickSorta
    if _start < _stop:
        p = Partition(_list, _start, _stop)		#podzial
        QuickSortR(_list, _start, p - 1)		#sortowanie lewej czesci
        QuickSortR(_list, p + 1, _stop)			#sortowanie prawej czesci

def QuickSort(_list):		#Funkcja startowa QuickSorta
    QuickSortR(_list, 0, len(_list) - 1)

def QuickSortHybridR(_list, _start, _stop, threshold=10):		#quicksort + insertsort(dla malych przedzialow)
    if _stop - _start + 1 <= threshold: 		#jesli maly fragment (w tym przypadku <10)
        for i in range(_start + 1, _stop + 1):			#sortowanie przez wstawianie (InsertSort)
            temp = _list[i]
            j = i - 1
            while j >= _start and _list[j] > temp:
                _list[j + 1] = _list[j]
                j -= 1
            _list[j + 1] = temp
    elif _start < _stop:						# w przeciwnym razie zwykly QuickSort
        p = Partition(_list, _start, _stop)
        QuickSortHybridR(_list, _start, p - 1, threshold)
        QuickSortHybridR(_list, p + 1, _stop, threshold)

def QuickSortHybrid(_list):			#Funkcja startowa QuickInsertSorta
    QuickSortHybridR(_list, 0, len(_list) - 1)

# --------------------
# StepSort
# --------------------

def StepSort(_list, step=10):				#wstepne sortowanie co 10 elementow
    for i in range(0, len(_list), step):		
        end = min(i + step, len(_list))		#ustalam koniec fragmentu
        InsertSort(_list[i:end])		#sortujemy ten fragment przez wstawianie

# --------------------
# Pomiar czasu
# --------------------

def pomiar_czasu(func, data):			#pomiara czasu dzialania funkcji
    start = time.time()		#poczatek czasu
    func(data)			#wywolanie
    end = time.time()		#koniec czasu
    return (end - start) * 1000  # ms			#zwrot czasu w milisekundach

# --------------------
# Wydruk tabeli
# --------------------

def print_table(tytul, naglowek, wyniki):			#funkcja do czytelnego wypisania wynikow
    print(f"\n\n{tytul}") 
    print("=" * len(tytul))
    print(naglowek)
    print("-" * len(naglowek))
    for wiersz in wyniki:
        print(wiersz)

# --------------------
# Główna część programu
# --------------------

if __name__ == "__main__":				#linia zeby plik dzialal wlaczony bezposrednio
    dlugosci = list(range(1000, 10001, 1000))				#lista dlugosci do testow (10 dlugosci od 100, 200, ...., 1000)

    # a) normalnene sortowanie
    normalne_wyniki = []			#lista na wyniki
    for n in dlugosci:				#dla kazdej dlugosci
        lista = [random.randint(0, 10000) for i in range(n)]		#losowanie listy w przedziale
        t1 = pomiar_czasu(InsertSort, lista.copy())		#czas InsertSort
        t2 = pomiar_czasu(BubbleSort, lista.copy())		#czas BubbleSort
        t3 = pomiar_czasu(QuickSort, lista.copy())		#czas QuickSort
        t4 = pomiar_czasu(QuickSortHybrid, lista.copy())		#czas QuickSorta z insertem
        normalne_wyniki.append(f"n = {n:<4} | {t1:9.3f} ms | {t2:9.3f} ms | {t3:9.3f} ms | {t4:9.3f} ms") #wypisanie wynikow pomiaru czasu dla roznych algorytmow
        #sortowania przy danej dlugosci listy, (n:<4 - wyrowananie do lewej na szerokosc 4 znakow), (t1-t4L9.3f - wstawienie wyniku jako zmiennoprzecinkowa na 9
        #znakow szerokosci z 3 miejscami po przecinku)
    print_table("normalnene sortowanie", "n       | Insert     | Bubble     | Quick      | QuickHybrid", normalne_wyniki) #wyswietlenie nazw funkcji na samej gorze 

    # b) Po StepSorcie
    stepsort_wyniki = []		#lista na wyniki po stepsorcie
    for n in dlugosci:
        lista = [random.randint(0, 10000) for i in range(n)]		#losowanie listy w przedziale
        base = lista.copy()		#kopia listy 
        StepSort(base)		#stepne sortowanie co 10
        t1 = pomiar_czasu(InsertSort, base.copy())
        t2 = pomiar_czasu(BubbleSort, base.copy())
        t3 = pomiar_czasu(QuickSort, base.copy())
        t4 = pomiar_czasu(QuickSortHybrid, base.copy())
        stepsort_wyniki.append(f"n = {n:<4} | {t1:9.3f} ms | {t2:9.3f} ms | {t3:9.3f} ms | {t4:9.3f} ms")
    print_table("StepSort (wstępne posortowanie co 10)", "n       | Insert     | Bubble     | Quick      | QuickHybrid", stepsort_wyniki)

    # c) Lista posortowana odwrotnie
    reverse_wyniki = []		#lista na wyniki dla odwrotnego sortowania
    for n in dlugosci:
        lista = sorted([random.randint(0, 10000) for i in range(n)], reverse=True)	#losowanie odwrotnej listy
        t1 = pomiar_czasu(InsertSort, lista.copy())
        t2 = pomiar_czasu(BubbleSort, lista.copy())
        t3 = pomiar_czasu(QuickSort, lista.copy())
        t4 = pomiar_czasu(QuickSortHybrid, lista.copy())
        reverse_wyniki.append(f"n = {n:<4} | {t1:9.3f} ms | {t2:9.3f} ms | {t3:9.3f} ms | {t4:9.3f} ms")
    print_table("Odwrotnie posortowana lista", "n       | Insert     | Bubble     | Quick      | QuickHybrid", reverse_wyniki)

    # d) Różne zakresy losowanych liczb
    zakresy = [10, 100, 1000, 10000, 100000]		#wypisanie roznych rangeow dla pomiarow
    for maks in zakresy:
        zakresy_wyniki = []		#lista na wyniki
        for n in dlugosci:
            lista = [random.randint(0, maks) for i in range(n)]		#losowanie listy w rangeie
            t1 = pomiar_czasu(InsertSort, lista.copy())
            t2 = pomiar_czasu(BubbleSort, lista.copy())
            t3 = pomiar_czasu(QuickSort, lista.copy())
            t4 = pomiar_czasu(QuickSortHybrid, lista.copy())
            zakresy_wyniki.append(f"n = {n:<4} | {t1:9.3f} ms | {t2:9.3f} ms | {t3:9.3f} ms | {t4:9.3f} ms")
        print_table(f"range wartości: 0 - {maks}", "n       | Insert     | Bubble     | Quick      | QuickHybrid", zakresy_wyniki)

