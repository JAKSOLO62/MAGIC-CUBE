import network
import machine
import time
import json
import urequests
import struct

SSID = 'Wifi Rob'
PASSWORD = '693495989'
BASE_URL = 'http://192.168.2.206:5000'

SCL_PIN = 14  # GPIO14 (D5)
SDA_PIN = 12  # GPIO12 (D6)
MPU_ADDR = 0x68

def connect_wifi():
    print("📡 Łączenie z Wi-Fi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\n✅ Połączono z Wi-Fi:", sta_if.ifconfig())

def scan_i2c():
    print("🔍 Skanowanie I2C (SCL=GPIO14 / SDA=GPIO12)...")
    i2c = machine.I2C(scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN))
    devices = i2c.scan()
    print("🔎 Znalezione adresy I2C:", devices)
    return i2c if MPU_ADDR in devices else None

def mpu_init(i2c):
    i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')

def read_accel(i2c):
    data = i2c.readfrom_mem(MPU_ADDR, 0x3B, 6)
    x, y, z = struct.unpack('>hhh', data)
    return x, y, z

def threshold(x):
    if x > 12000:
        return 1
    if x < -12000:
        return -1
    if -2000 < x < 2000:
        return 0
    return None

def get_orientation(i2c):
    for _ in range(10):
        x, y, z = read_accel(i2c)
        orientation = (threshold(x), threshold(y), threshold(z))
        if None not in orientation:
            return orientation
        time.sleep(0.1)
    return None

def send_face(face):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(f"📦 Symuluję ścianę {face} @ {timestamp}")
    try:
        resp = urequests.post(BASE_URL + '/face', json={
            'face': face,
            'timestamp': timestamp
        })
        print("✅ Status:", resp.status_code)
        print("💬 Odpowiedź serwera:", resp.text)
    except Exception as e:
        print("❌ Błąd podczas wysyłania:", e)

# === GŁÓWNY PROGRAM ===
print("🚀 START main.py")
connect_wifi()
i2c = scan_i2c()

if i2c:
    try:
        mpu_init(i2c)
        orientation = get_orientation(i2c)
        face_map = {
            (0, 0, 1): 'A',
            (1, 0, 0): 'B',
            (0, 1, 0): 'C',
            (-1, 0, 0): 'D',
            (0, -1, 0): 'E',
            (0, 0, -1): 'F',
        }
        face = face_map.get(orientation, 'UNKNOWN')
    except Exception as e:
        print("⚠️ Błąd MPU:", e)
        face = 'SIM-MPUERR'
else:
    print("❌ MPU6050 NIE wykryty. Sprawdź połączenia!")
    face = 'SIM-NOMPU'

send_face(face)
