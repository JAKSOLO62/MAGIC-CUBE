# MAGIC-CUBE

Magic Cube to inteligentna kostka służąca do monitorowania czasu poświęcanego na różne
zadania. Każda z sześciu ścian kostki odpowiada innej aktywności (np. pracy nad projektem
A, przerwie, nauce). Użytkownik zmienia stronę kostki w zależności od tego, nad czym
pracuje, co umożliwia rejestrację czasu spędzonego na danym zadaniu. Urządzenie korzysta z
akcelerometru (czujnika MPU6050) do wykrywania orientacji przestrzennej oraz z modułu
Wi -Fi (ESP8266) do przesyłania danych do systemu rejestrującego. Projekt inspirowany
był potrzebą posiadania fizycznego narzędzia do śledzenia czasu pracy (podobnego do
rozwiązań dostępnych komercyjnie) oraz dążeniem do stworzenia niezależnego, bezprze-
wodowego urządzenia. Głównymi założeniami było zapewnienie komunikacji Wi-Fi bez
potrzeby korzystania z zewnętrznej aplikacji (kostka wysyła dane bezpośrednio do Internetu)
oraz maksymalne wydłużenie czasu pracy na baterii poprzez stosowanie trybów głębokiego
uśpienia mikrokontrolera.
