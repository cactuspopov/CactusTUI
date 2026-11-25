import os
import sys
import time
import random
import string
import hashlib
import base64
import uuid
import datetime
import platform
import getpass
import socket
import codecs
import urllib.request
import urllib.error

os.system('')  # включить ANSI в Windows 10+

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import init, Fore, Style
    init(autoreset=True)

P = Fore.MAGENTA
B = Style.BRIGHT
D = Style.DIM
R = Style.RESET_ALL
RED = Fore.RED
GREEN = Fore.GREEN

# ===================== БЛОЧНЫЙ ШРИФТ =====================
FONT = {
    'C': [".###.", "#....", "#....", "#....", ".###."],
    'A': [".###.", "#...#", "#####", "#...#", "#...#"],
    'T': ["#####", "..#..", "..#..", "..#..", "..#.."],
    'U': ["#...#", "#...#", "#...#", "#...#", ".###."],
    'S': [".####", "#....", ".###.", "....#", "####."],
    'O': [".###.", "#...#", "#...#", "#...#", ".###."],
    'L': ["#....", "#....", "#....", "#....", "#####"],
    'V': ["#...#", "#...#", "#...#", ".#.#.", "..#.."],
    '1': ["..#..", ".##..", "..#..", "..#..", ".###."],
    '.': [".....", ".....", ".....", ".....", "..#.."],
    '0': [".###.", "#...#", "#...#", "#...#", ".###."],
    ' ': [".....", ".....", ".....", ".....", "....."],
}

def truecolor(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def render_logo(text, glitch=False):
    rows = ["", "", "", "", ""]
    for ch in text:
        glyph = FONT.get(ch.upper() if ch.isalpha() else ch, FONT[' '])
        for r in range(5):
            line = ""
            for c in range(len(glyph[r])):
                if glyph[r][c] == '#':
                    line += random.choice("█▓▒░") if glitch and random.random() < 0.25 else "█"
                else:
                    line += " "
            rows[r] += line
    out = []
    for r in range(5):
        line = rows[r]
        colored = ""
        for i, c in enumerate(line):
            t = i / max(1, len(line) - 1)
            red   = int(90  + (220 - 90)  * t)
            green = int(10  + (130 - 10)  * t)
            blue  = int(160 + (255 - 160) * t)
            if c == ' ':
                colored += " "
            else:
                colored += truecolor(red, green, blue) + c
        out.append(colored + R)
    return "\n".join(out)

def animate_logo(text, duration=1.2):
    frames = int(duration / 0.08)
    for _ in range(frames):
        clear()
        print(render_logo(text, glitch=True))
        time.sleep(0.08)
    clear()
    print(render_logo(text, glitch=False))

# ===================== MATRIX RAIN =====================
def matrix_rain(duration=3):
    chars = "アイウエオカキクケコ0123456789ABCDEF$%#@!?<>{}[]"
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines - 5
    columns = [random.randint(-20, 0) for _ in range(width)]
    start = time.time()
    print("\033[?25l", end="")
    try:
        while time.time() - start < duration:
            line = ""
            for i in range(width):
                if 0 < columns[i] < height:
                    line += random.choice(chars)
                else:
                    line += " "
                columns[i] += 1
                if columns[i] > height + 10:
                    columns[i] = random.randint(-20, -5)
            print(f"{D}{P}{line}{R}")
            time.sleep(0.04)
            sys.stdout.write(f"\033[{height}A")
            sys.stdout.flush()
    except:
        pass
    print("\n" * (height + 2))
    print("\033[?25h", end="")

def progress_bar(label, duration=0.5):
    width = 30
    steps = 20
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar = "█" * filled + "░" * (width - filled)
        percent = int(100 * i / steps)
        sys.stdout.write(f"\r  {P}[{bar}]{R} {percent}% {D}{label}{R}")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def loading_screen():
    clear()
    matrix_rain(3)
    animate_logo("CACTUSTOOLS", 1.5)
    print(f"\n{D}  BEST & PRETTIEST FRAMEWORK — EDITION 2026{R}\n")
    time.sleep(0.5)
    modules = [
        "Инициализация ядра Cactus", "Загрузка модулей ядра",
        "Синхронизация сетевых интерфейсов", "Обход систем защиты",
        "Подключение к серверам", "Финальная настройка",
    ]
    for mod in modules:
        progress_bar(mod, 0.4)
    print(f"\n{P}{B}✓ Все модули загружены. Добро пожаловать в CACTUSTOOLS.{R}\n")
    time.sleep(1)
    input(f"{P}{B}Нажмите Enter для входа...{R}")

# ===================== UTILS =====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(f"\n{D}Нажмите Enter для продолжения...{R}")

# ===================== ORIGINAL TOOLS (1-8) =====================
def gen_password():
    clear()
    print(f"{P}{B}=== [1] ГЕНЕРАТОР ПАРОЛЕЙ ==={R}\n")
    try: length = int(input("Длина пароля: "))
    except: length = 16
    use_upper = input("Заглавные буквы? (д/н): ").lower() == 'д'
    use_digits = input("Цифры? (д/н): ").lower() == 'д'
    use_symbols = input("Символы? (д/н): ").lower() == 'д'
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    pwd = ''.join(random.choice(chars) for _ in range(length))
    print(f"\n{P}{B}Пароль: {pwd}{R}")
    score = sum([length>=12, length>=16, use_upper and use_digits and use_symbols, (use_upper or use_digits or use_symbols)])
    strength = ["Слабый", "Средний", "Хороший", "Сильный", "Очень сильный"][score]
    print(f"{D}Надёжность: {strength}{R}")
    pause()

def file_counter():
    clear()
    print(f"{P}{B}=== [2] СЧЁТЧИК СТРОК/СЛОВ ==={R}\n")
    path = input("Путь к файлу: ").strip().strip('"')
    if not os.path.isfile(path):
        print(f"{RED}Файл не найден!{R}"); return pause()
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    print(f"\n{P}Строк:    {B}{len(lines)}{R}")
    print(f"{P}Слов:     {B}{sum(len(l.split()) for l in lines)}{R}")
    print(f"{P}Символов: {B}{sum(len(l) for l in lines)}{R}")
    pause()

def uuid_gen():
    clear()
    print(f"{P}{B}=== [3] UUID ГЕНЕРАТОР ==={R}\n")
    print("1 — UUID4 (случайный)\n2 — UUID1 (на основе MAC/времени)")
    choice = input("Выбор: ")
    u = uuid.uuid1() if choice == '2' else uuid.uuid4()
    print(f"\n{P}{B}UUID: {u}{R}\n{D}Версия: {u.version}{R}")
    pause()

def hash_tool():
    clear()
    print(f"{P}{B}=== [4] ХЕШ ФУНКЦИИ ==={R}\n")
    text = input("Введите текст: ")
    print(f"\n{P}MD5:    {B}{hashlib.md5(text.encode()).hexdigest()}{R}")
    print(f"{P}SHA1:   {B}{hashlib.sha1(text.encode()).hexdigest()}{R}")
    print(f"{P}SHA256: {B}{hashlib.sha256(text.encode()).hexdigest()}{R}")
    print(f"{P}SHA512: {B}{hashlib.sha512(text.encode()).hexdigest()}{R}")
    pause()

def base64_tool():
    clear()
    print(f"{P}{B}=== [5] BASE64 ==={R}\n")
    print("1 — Кодировать\n2 — Декодировать")
    c = input("Выбор: ")
    text = input("Текст: ")
    try:
        res = base64.b64encode(text.encode()).decode() if c == '1' else base64.b64decode(text.encode()).decode()
        print(f"\n{P}{B}{'Base64' if c=='1' else 'Decoded'}: {res}{R}")
    except Exception as e:
        print(f"{RED}Ошибка: {e}{R}")
    pause()

def sys_info():
    clear()
    print(f"{P}{B}=== [6] СИСТЕМНАЯ ИНФОРМАЦИЯ ==={R}\n")
    info = [
        ("ОС", f"{platform.system()} {platform.release()}"),
        ("Архитектура", platform.machine()),
        ("Процессор", platform.processor() or "N/A"),
        ("Python", sys.version.split()[0]),
        ("Пользователь", getpass.getuser()),
        ("Имя ПК", platform.node()),
        ("Время", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("CWD", os.getcwd()),
    ]
    for k, v in info:
        print(f"{P}{k:15}: {B}{v}{R}")
    pause()

def random_dice():
    clear()
    print(f"{P}{B}=== [7] РАНДОМ И КУБИКИ ==={R}\n")
    print("1 — Бросить кубик (1-6)\n2 — Случайное число\n3 — Монетка")
    c = input("Выбор: ")
    if c == '1':
        n = int(input("Сколько кубиков? ") or 1)
        rolls = [random.randint(1, 6) for _ in range(n)]
        print(f"\n{P}{B}Результат: {rolls} = {sum(rolls)}{R}")
    elif c == '2':
        a, b = int(input("От: ")), int(input("До: "))
        print(f"\n{P}{B}Число: {random.randint(a, b)}{R}")
    elif c == '3':
        print(f"\n{P}{B}{random.choice(['Орёл', 'Решка'])}!{R}")
    pause()

def time_converter():
    clear()
    print(f"{P}{B}=== [8] КОНВЕРТЕР ВРЕМЕНИ ==={R}\n")
    print("1 — Unix timestamp → дата\n2 — Дата → Unix timestamp\n3 — Текущее время")
    c = input("Выбор: ")
    if c == '1':
        ts = int(input("Timestamp: "))
        print(f"\n{P}{B}{datetime.datetime.fromtimestamp(ts)}{R}")
    elif c == '2':
        s = input("Дата (YYYY-MM-DD HH:MM:SS): ")
        dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        print(f"\n{P}{B}Timestamp: {int(dt.timestamp())}{R}")
    elif c == '3':
        print(f"\n{P}Local: {B}{datetime.datetime.now()}{R}")
        print(f"{P}UTC:   {B}{datetime.datetime.utcnow()}{R}")
    pause()

# ===================== NEW TOOLS (9-18) =====================
def ip_network_tool():
    clear()
    print(f"{P}{B}=== [9] IP И СЕТЬ ==={R}\n")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"{P}Hostname:  {B}{hostname}{R}")
    print(f"{P}Local IP:  {B}{local_ip}{R}")
    print(f"{P}External IP: {B}", end="")
    try:
        ext_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf8')
        print(f"{ext_ip}{R}")
    except:
        print(f"{RED}Нет подключения к интернету{R}")
    pause()

def dns_resolver():
    clear()
    print(f"{P}{B}=== [10] DNS РЕЗОЛВЕР ==={R}\n")
    domain = input("Введите домен (например, google.com): ").strip()
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{P}Домен: {B}{domain}{R}")
        print(f"{P}IP:    {B}{ip}{R}")
    except socket.gaierror:
        print(f"\n{RED}Не удалось разрешить домен!{R}")
    pause()

def port_scanner():
    clear()
    print(f"{P}{B}=== [11] СКАНЕР ПОРТОВ ==={R}\n")
    target = input("IP или домен: ").strip()
    ports_str = input("Порты (через запятую, например 80,443,8080): ").strip()
    ports = [int(p.strip()) for p in ports_str.split(',') if p.strip().isdigit()]
    print(f"\n{D}Сканирование {target}...{R}\n")
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
            print(f"  {GREEN}[✓] Порт {port} открыт{R}")
        else:
            print(f"  {D}[✗] Порт {port} закрыт{R}")
        sock.close()
    print(f"\n{P}{B}Открытые порты: {open_ports}{R}")
    pause()

def url_unshortener():
    clear()
    print(f"{P}{B}=== [12] РАЗВОРАЧИВАТЕЛЬ ССЫЛОК ==={R}\n")
    url = input("Введите короткую ссылку: ").strip()
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        req = urllib.request.Request(url, method='HEAD')
        response = urllib.request.urlopen(req, timeout=5)
        print(f"\n{P}Исходная: {B}{url}{R}")
        print(f"{P}Финальная: {B}{response.url}{R}")
    except Exception as e:
        print(f"\n{RED}Ошибка: {e}{R}")
    pause()

def text_hex_bin():
    clear()
    print(f"{P}{B}=== [13] ТЕКСТ В HEX/BINARY ==={R}\n")
    text = input("Введите текст: ")
    hex_val = text.encode('utf-8').hex()
    bin_val = ' '.join(format(byte, '08b') for byte in text.encode('utf-8'))
    print(f"\n{P}HEX:    {B}{hex_val}{R}")
    print(f"{P}BINARY: {B}{bin_val}{R}")
    pause()

def caesar_cipher():
    clear()
    print(f"{P}{B}=== [14] ШИФР ЦЕЗАРЯ ==={R}\n")
    text = input("Текст: ")
    shift = int(input("Сдвиг (1-25): ") or 3)
    mode = input("1 — Шифровать, 2 — Дешифровать: ")
    if mode == '2':
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    print(f"\n{P}{B}Результат: {result}{R}")
    pause()

def rot13_tool():
    clear()
    print(f"{P}{B}=== [15] ROT13 ==={R}\n")
    text = input("Текст: ")
    print(f"\n{P}{B}ROT13: {codecs.encode(text, 'rot_13')}{R}")
    pause()

def ua_generator():
    clear()
    print(f"{P}{B}=== [16] ГЕНЕРАТОР USER-AGENT ==={R}\n")
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    ]
    print(f"\n{P}{B}Случайный User-Agent:{R}\n{D}{random.choice(uas)}{R}")
    pause()

def bulk_file_gen():
    clear()
    print(f"{P}{B}=== [17] МАССОВОЕ СОЗДАНИЕ ФАЙЛОВ ==={R}\n")
    folder = input("Имя папки: ").strip() or "dummy_files"
    count = int(input("Количество файлов: ") or 10)
    os.makedirs(folder, exist_ok=True)
    for i in range(count):
        with open(os.path.join(folder, f"file_{i:04d}.txt"), 'w') as f:
            f.write(f"Dummy content {i}\n")
    print(f"\n{P}{B}✓ Создано {count} файлов в папке '{folder}'{R}")
    pause()

def ping_tool():
    clear()
    print(f"{P}{B}=== [18] PING УТИЛИТА ==={R}\n")
    host = input("Хост или IP: ").strip()
    count = input("Количество пакетов (по умолч. 4): ").strip() or "4"
    param = '-n' if os.name == 'nt' else '-c'
    print(f"\n{D}Запуск ping {host}...{R}\n")
    os.system(f"ping {param} {count} {host}")
    pause()

# ===================== MAIN MENU =====================
def menu():
    first = True
    while True:
        clear()
        if first:
            animate_logo("CACTUSTOOLS", 0.8)
            first = False
        else:
            print(render_logo("CACTUSTOOLS"))
        print(f"{D}  BEST & PRETTIEST FRAMEWORK — EDITION 2026{R}")
        print(f"{P}  v1.0  |  18 модулей  |  онлайн{R}\n")
        
        tools = [
            "[1] Генератор паролей",        "[10] DNS Резолвер",
            "[2] Счётчик строк/слов",       "[11] Сканер портов",
            "[3] UUID-генератор",           "[12] Разворачиватель ссылок",
            "[4] Хеш (md5/sha1/sha256)",    "[13] Текст в Hex/Binary",
            "[5] Base64 кодирование",       "[14] Шифр Цезаря",
            "[6] Системная информация",     "[15] ROT13",
            "[7] Рандом и кубики",          "[16] Генератор User-Agent",
            "[8] Конвертер времени",        "[17] Массовое создание файлов",
            "[9] IP и Сеть",                "[18] Ping утилита",
        ]
        
        print(f"{P}{B}Инструменты:{R}\n")
        # Печатаем в две колонки
        for i in range(0, len(tools), 2):
            left = tools[i].ljust(30)
            right = tools[i+1] if i+1 < len(tools) else ""
            print(f"  {left} {right}")
            
        print(f"\n  {RED}[0] Выход{R}\n")
        
        try:
            choice = input(f"{P}>{R} ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        funcs = {
            '1': gen_password, '2': file_counter, '3': uuid_gen, '4': hash_tool,
            '5': base64_tool, '6': sys_info, '7': random_dice, '8': time_converter,
            '9': ip_network_tool, '10': dns_resolver, '11': port_scanner, '12': url_unshortener,
            '13': text_hex_bin, '14': caesar_cipher, '15': rot13_tool, '16': ua_generator,
            '17': bulk_file_gen, '18': ping_tool,
        }
        
        if choice == '0':
            print(f"\n{P}{B}Выход из CACTUSTOOLS. До связи!{R}")
            break
        elif choice in funcs:
            funcs[choice]()
        else:
            print(f"{RED}Неверный выбор!{R}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        loading_screen()
        menu()
    except KeyboardInterrupt:
        print(f"\n{P}Выход...{R}")
