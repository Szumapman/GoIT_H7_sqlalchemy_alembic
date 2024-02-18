### GoIT moduł 2 web 
# Zadanie domowe #7
## Wprowadzenie
W tym zadaniu domowym będziemy kontynuować pracę z zadaniem domowym z poprzedniego modułu. W tym zadaniu domowym użyjemy bazy danych `postgres`, 
działającej w kontenerze `Docker`.
W wierszu poleceń, przejdż do katalgu zawierającego `Dockerfile` i uruchom polecenie:
```
docker build . -t TWOJA_NAZWA_KONTENERA
```
```
docker run -p 5432:5432 -d TWOJA_NAZWA_KONTENERA 
```
Zamiast **TWOJA_NAZWA_KONTENERA** wybierz nazwę kontenera.
## Kroki do wykonania zadania domowego:
### Krok pierwszy
Zaimplementuj swoje modele SQLAlchemy dla tabel: 
* Tabela studentów; 
* Tabela grup; 
* Tabela wykładowców; 
* Tabela przedmiotów ze wskazaniem wykładowcy, który uczy danego przedmiotu; 
* Tabela, w której każdy student ma oceny z przedmiotów ze wskazaniem, kiedy ocena została otrzymana;
### Krok drugi
Użyj `alembic`, aby utworzyć migracje w bazie danych.
### Krok trzeci
Napisz skrypt `seed.py` wypełnij wynikową bazę danych losowymi danymi 
(~30-50 studentów, 3 grupy, 5-8 przedmiotów, 3-5 wykładowców, do 20 ocen dla każdego studenta we wszystkich przedmiotach). 
Do wypełniania użyj pakietu `Faker`. Podczas wypełniania użyj mechanizmu sesji **SQLAlchemy**.
### Krok czwarty
Z bazy danych dokonaj następujących wyborów:
1. Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.
2. Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu.
3. Znajdź średni wynik w grupach dla określonego przedmiotu.
4. Znajdź średni wynik w grupie (w całej tabeli ocen).
5. Znajdź przedmioty, których uczy określony wykładowca.
6. Znajdź listę studentów w określonej grupie.
7. Znajdź oceny studentów w określonej grupie z danego przedmiotu.
8. Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.
9. Lista kursów, na które uczęszcza uczeń - z zad. 6 org: Znajdź listę przedmiotów zaliczonych przez danego studenta.
10. Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta.

Dla zapytań utwórz osobny plik `my_select.py`, który będzie zawierał `10` funkcji od `select_1` do `select_10`.
Funkcje powinny zwracać ten sam wynik, co w poprzednim zadaniu domowym. Podczas tworzenia zapytań korzystaj z mechanizmu sesji **SQLAlchemy**.

### Wskazówki i porady
To zadanie sprawdzi Twoją umiejętność korzystania z dokumentacji **SQLAlchemy**. Jednak od razu podamy Ci główne wskazówki i porady dotyczące rozwiązania.

Załóżmy, że mamy następujące zapytanie: Znajdź 5 studentów z najwyższym GPA we wszystkich przedmiotach.

Spróbujmy przetłumaczyć je na zapytanie ORM SQLAlchemy. Załóżmy, że mamy sesję w zmiennej `session`. Mamy opisane modele `Student` i `Grade` dla odpowiednich tabel. 
Zakładamy, że baza danych jest już wypełniona danymi. _SQLAlchemy_ przechowuje funkcje agregujące w obiekcie `func`. 
Musi on być specjalnie zaimportowany z `from sqlalchemy import func`, a następnie możemy użyć metod `func.round` i `func.avg`. 
Tak więc pierwszy wiersz zapytania SQL powinien wyglądać następująco: `session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))`.

Tutaj użyliśmy innej etykiety `label('avg_grade')`, aby ORM mógł nazwać pole ze średnią oceną za pomocą instrukcji `AS`.

Następnie `FROM grades g` jest zastępowane metodą `select_from(Grade)`. Zastąpienie instrukcji `JOIN` jest proste, jest to funkcja `join(Student)`, 
resztą zajmuje się _ORM_. Grupowanie według pola jest wykonywane przez funkcję `group_by(Student.id)`. 
Funkcja `order_by` odpowiada za sortowanie, które domyślnie sortuje jako `ASC`, ale wyraźnie potrzebujemy trybu rosnącego `DESC`, a także według pola `avg_grade`, 
które utworzyliśmy w zapytaniu. Importuj z `from sqlalchemy import func, desc` i ostateczną formę `order_by(desc('avg_grade'))`. 
Limit pięciu wartości to funkcja o tej samej nazwie `limit(5)`. To wszystko, nasze zapytanie jest gotowe. Ostateczna wersja zapytania dla SQLAlchemy ORM.

W przypadku pozostałych zapytań, należy zbudować je podobnie do powyższego przykładu. 
Ostatnia wskazówka: jeśli zdecydujesz się na tworzenie zagnieżdżonych zapytań, użyj [scalar-selects](https://docs.sqlalchemy.org/en/14/core/tutorial.html#scalar-selects)

## Zadanie dodatkowe
### Część pierwsza
W ramach dodatkowego zadania wykonaj następujące zapytania o zwiększonej złożoności:
1. Średnia ocena, jaką określony wykładowca wystawił pewnemu studentowi.
2. Oceny studentów w określonej grupie z określonego przedmiotu na ostatnich zajęciach.

### Część druga
Zamiast używać skryptu `seed.py` pomyśl i zaimplementuj pełnoprawny program **CLI** do operacji **CRUD** z bazą danych. 
Użyj do tego modułu [**argparse**](https://docs.python.org/3/library/argparse.html) . 
Użyj polecenia `--action` lub skróconej wersji `-a` dla operacji **CRUD** i polecenia `--model `(`-m`), aby określić, na którym modelu ma zostać wykonana operacja. 

Przykład: 
* `--action create -m Lecturer --lecturer_name 'Boris Jonson' --email b.jonson@email.com` — utworzenie wykładowcy;
* `--action list -m Lecturer` — wyświetlenie wszystkich wykładowców;
* `--action update -m Lecturer --id 3 --lecturer_name 'Andry Bezos'` — zaktualizowanie danych wykładowcy id=3;
* `--action remove -m Lecturer --id 3` — usunięcie wykładowcy z id=3;

Zaimplementuj te operacje dla każdego modelu.
> [!NOTE]
> Przykłady poleceń w terminalu:
> * Utworzenie wykładowcy:
> ```
> python3 cli_crud.py -a create -m Lecturer --lecturer_name 'Boris Jonson' --email b.jonson@email.com
> ```
> Utworzenie grupy:
> ```
> python3 cli_crud.py -a create -m Group --group_name 2A`
> ```

