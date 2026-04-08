import serial          # do komunikacji po UART
import matplotlib.pyplot as plt  # do wykresu
import matplotlib.animation as animation
import re               # do parsowania wartości float z tekstu

# ---------------------
# KONFIGURACJA PORTU UART
# ---------------------
PORT = 'COM8'           # zamień na swój port COM
BAUDRATE = 38400         # zgodnie z ustawieniami STM32

# otwieramy port szeregowy
ser = serial.Serial(PORT, BAUDRATE, timeout=1)  # timeout=1s, żeby nie wieszać programu

# ---------------------
# FUNKCJA PARSUJĄCA LINIE
# ---------------------
def parse_voltage(line):
    """
    Funkcja próbuje wyciągnąć liczbę zmiennoprzecinkową z linii
    formatu 'V: 0.370'. Jeśli nie znajdzie, zwraca None.
    """
    match = re.search(r'V:\s*([0-9.]+)', line)
    if match:
        return float(match.group(1))
    return None

# ---------------------
# LISTY DO WYKRESU
# ---------------------
voltages = []   # tu będziemy przechowywać napięcia
times = []      # tu czas (indeks pomiaru)

# ---------------------
# FUNKCJA ANIMACJI MATPLOTLIB
# ---------------------
def update(frame):
    """
    Funkcja wywoływana co klatkę animacji. Odczytuje linie z UART i aktualizuje wykres.
    """
    line = ser.readline().decode('ascii', errors='ignore').strip()  # odczyt linii z UART
    voltage = parse_voltage(line)
    if voltage is not None:
        voltages.append(voltage)
        times.append(len(times))  # po prostu licznik próbek, 1 sekunda między odczytami
        ax.clear()
        ax.plot(times, voltages, label="Napięcie [V]")
        ax.set_ylim(0, 3.3)
        ax.set_xlabel("Pomiar nr")
        ax.set_ylabel("Napięcie [V]")
        ax.set_title("Odczyt napięcia z STM32")
        ax.legend()
        ax.grid(True)

# ---------------------
# TWORZENIE WYKRESU
# ---------------------
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, interval=1000)  # 1000ms = 1 sekunda

plt.show()

# ---------------------
# ZAMKNIĘCIE PORTU PO ZAMKNIĘCIU WYKRESU
# ---------------------
ser.close()