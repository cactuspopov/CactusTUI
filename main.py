#!/usr/bin/env python3
"""CACTUSTUI — консольный лаунчер."""

import base64
import datetime
import getpass
import hashlib
import json
import os
import platform
import random
import secrets
import socket
import string
import sys
import time
import uuid
from pathlib import Path

CONFIG_PATH = Path.home() / ".cactustui.json"

# --- ТОЧНЫЙ ASCII-АРТ (Точки защищают от обрезки пробелов) ---
BANNER = r"""
.####...##....####..######.#...#..####..######.#...#..#####
#......#..#..#.........#...#...#.#.........#...#...#....#..
#......#..#..#.........#...#...#.#.........#...#...#....#..
#......####..#.........#...#...#..####.....#...#...#....#..
#......#..#..#.........#...#...#......#....#...#...#....#..
#......#..#..#.........#...#...#......#....#...#...#....#..
.####..#..#...####.....#....###....####.....#....###...###.
""".replace(".", " ")

RESET = "\033[0m"

# 256-цветные коды для терминала
THEMES = {
    "cactus":  {"accent": "\033[38;5;46m",  "border": "\033[38;5;35m",  "text": "\033[38;5;82m"},
    "default": {"accent": "\033[38;5;51m",  "border": "\033[38;5;33m",  "text": "\033[38;5;250m"},
    "neon":    {"accent": "\033[38;5;201m", "border": "\033[38;5;51m",  "text": "\033[38;5;226m"},
    "fire":    {"accent": "\033[38;5;196m", "border": "\033[38;5;208m", "text": "\033[38;5;226m"},
    "ocean":   {"accent": "\033[38;5;39m",  "border": "\033[38;5;27m",  "text": "\033[38;5;123m"},
}

DEFAULT_CONFIG = {"user": "user", "theme": "cactus", "animations": True}


# ---------- Базовые утилиты ----------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\n  Enter — продолжить...")


def load_config():
    if CONFIG_PATH.exists():
        try:
            return {**DEFAULT_CONFIG, **json.loads(CONFIG_PATH.read_text(encoding="utf-8"))}
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def theme_of(cfg):
    return THEMES.get(cfg.get("theme"), THEMES["cactus"])


def paint(text, cfg, role="accent"):
    return f"{theme_of(cfg)[role]}{text}{RESET}"


def spinner(cfg, seconds=0.35, text="генерация"):
    if not cfg.get("animations"):
        return
    frames = "|/-\\"
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {text} {frames[i % len(frames)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.07)
    sys.stdout.write("\r" + " " * 40 + "\r")


def clean_path(raw):
    return raw.strip().strip('"').strip("'")


def resolve_path(raw):
    p = Path(clean_path(raw)).expanduser()
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    return p


# ---------- Отрисовка интерфейса ----------

def print_banner(cfg):
    color = theme_of(cfg)["accent"]
    if cfg.get("animations"):
        for line in BANNER.strip("\n").split("\n"):
            sys.stdout.write(color + line + RESET + "\n")
            sys.stdout.flush()
            time.sleep(0.03)
    else:
        print(color + BANNER.strip("\n") + RESET)


def header(cfg):
    clear()
    print()
    print_banner(cfg)
    info = f"  user: {cfg['user']}  |  theme: {cfg['theme']}  |  animations: {cfg['animations']}"
    print(paint(info, cfg, "text"))
    print("  " + paint("─" * 60, cfg, "border"))


def draw_menu(items, title, cfg):
    print(f"\n  {paint(title, cfg)}")
    for key, name in items:
        print(f"    [{key}] {name}")


# ---------- Логика инструментов ----------

def make_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def count_file(raw_path):
    p = resolve_path(raw_path)
    if not p.exists():
        raise FileNotFoundError(f"не найден: {p}")
    if p.is_dir():
        raise IsADirectoryError(f"это папка, а нужен файл: {p}")
    lines = words = chars = 0
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            lines += 1
            words += len(line.split())
            chars += len(line)
    return p, lines, words, chars


def hash_file(p, algo):
    h = hashlib.new(algo)
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- Меню Настроек ----------

def settings_menu(cfg):
    while True:
        header(cfg)
        draw_menu([
            ("1", "Сменить имя"),
            ("2", "Сменить тему"),
            ("3", "Переключить анимации"),
            ("4", "Показать конфиг"),
            ("5", "Сбросить настройки"),
            ("0", "Назад"),
        ], "Настройки", cfg)
        choice = input("\n  > ").strip()

        if choice == "1":
            cfg["user"] = input("  Новое имя: ").strip() or cfg["user"]
            save_config(cfg)
        elif choice == "2":
            print(f"  Темы: {', '.join(THEMES)}")
            t = input("  Тема: ").strip().lower()
            if t in THEMES:
                cfg["theme"] = t
                save_config(cfg)
            else:
                print("  Нет такой темы")
                pause()
        elif choice == "3":
            cfg["animations"] = not cfg["animations"]
            save_config(cfg)
        elif choice == "4":
            header(cfg)
            print(json.dumps(cfg, indent=2, ensure_ascii=False))
            pause()
        elif choice == "5":
            if input("  Точно сбросить? [y/N] ").lower() == "y":
                cfg.clear()
                cfg.update(DEFAULT_CONFIG)
                save_config(cfg)
        elif choice == "0":
            return cfg


# ---------- Инструменты ----------

def password_tool(cfg):
    try:
        n = max(4, int(input("  Длина пароля [16]: ") or "16"))
    except ValueError:
        n = 16
    while True:
        header(cfg)
        spinner(cfg, 0.35, "генерация")
        print(f"\n  Пароль ({n} симв.): {paint(make_password(n), cfg)}\n")
        print("    [1] Ещё   [0] Назад")
        if input("  > ").strip() != "1":
            return


def counter_tool(cfg):
    header(cfg)
    try:
        p, lines, words, chars = count_file(input("  Путь к файлу: "))
        print(f"\n  Файл: {p}")
        print(f"  Строк: {lines}")
        print(f"  Слов:  {words}")
        print(f"  Символов: {chars}")
    except Exception as e:
        print(f"\n  Ошибка: {e}")
    pause()


def uuid_tool(cfg):
    header(cfg)
    try:
        n = min(100, max(1, int(input("  Сколько UUID [1]: ") or "1")))
    except ValueError:
        n = 1
    print()
    for _ in range(n):
        print(f"  {paint(str(uuid.uuid4()), cfg)}")
    pause()


def hash_tool(cfg):
    header(cfg)
    draw_menu([("1", "Хеш строки"), ("2", "Хеш файла"), ("0", "Назад")], "Хеш", cfg)
    mode = input("\n  > ").strip()
    if mode == "0":
        return
    algo = (input("  Алгоритм [md5/sha1/sha256]: ").strip().lower() or "sha256")
    if algo not in ("md5", "sha1", "sha256"):
        algo = "sha256"

    header(cfg)
    try:
        if mode == "1":
            data = input("  Строка: ").encode("utf-8")
            digest = hashlib.new(algo, data).hexdigest()
        elif mode == "2":
            p = resolve_path(input("  Путь к файлу: "))
            if not p.exists() or p.is_dir():
                raise FileNotFoundError(f"нет файла: {p}")
            digest = hash_file(p, algo)
        else:
            return
        print(f"\n  {algo}: {paint(digest, cfg)}")
    except Exception as e:
        print(f"\n  Ошибка: {e}")
    pause()


def base64_tool(cfg):
    while True:
        header(cfg)
        draw_menu([
            ("1", "Кодировать текст"),
            ("2", "Декодировать текст"),
            ("3", "Кодировать файл"),
            ("0", "Назад"),
        ], "Base64", cfg)
        c = input("\n  > ").strip()
        if c == "0":
            return
        header(cfg)
        try:
            if c == "1":
                out = base64.b64encode(input("  Текст: ").encode("utf-8")).decode()
                print(f"\n  {paint(out, cfg)}")
            elif c == "2":
                s = input("  Base64: ")
                out = base64.b64decode(s).decode("utf-8", errors="replace")
                print(f"\n  {paint(out, cfg)}")
            elif c == "3":
                p = resolve_path(input("  Путь к файлу: "))
                if not p.exists() or p.is_dir():
                    raise FileNotFoundError(f"нет файла: {p}")
                target = p.with_suffix(p.suffix + ".b64")
                target.write_text(base64.b64encode(p.read_bytes()).decode(), encoding="ascii")
                print(f"\n  Сохранено: {target}")
        except Exception as e:
            print(f"\n  Ошибка: {e}")
        pause()


def sysinfo_tool(cfg):
    header(cfg)
    print(f"  Пользователь: {paint(getpass.getuser(), cfg)}")
    print(f"  Хост:         {socket.gethostname()}")
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "неизвестен"
    print(f"  Локальный IP: {ip}")
    print(f"  ОС:           {platform.system()} {platform.release()}")
    print(f"  Python:       {platform.python_version()}")
    pause()


def random_tool(cfg):
    header(cfg)
    draw_menu([("1", "Случайное число"), ("2", "Кубики (D&D)"), ("0", "Назад")], "Рандом", cfg)
    c = input("\n  > ").strip()
    if c == "0":
        return
    header(cfg)
    try:
        if c == "1":
            a = int(input("  От: ") or "1")
            b = int(input("  До: ") or "100")
            if a > b:
                a, b = b, a
            print(f"\n  Результат: {paint(str(random.randint(a, b)), cfg)}")
        elif c == "2":
            n = int(input("  Сколько кубиков [1]: ") or "1")
            sides = int(input("  Сколько граней [6]: ") or "6")
            rolls = [random.randint(1, sides) for _ in range(n)]
            print(f"\n  Выпало: {rolls}")
            print(f"  Сумма:  {paint(str(sum(rolls)), cfg)}")
    except ValueError:
        print("\n  Ошибка: нужно ввести числа")
    pause()


def time_tool(cfg):
    header(cfg)
    draw_menu([
        ("1", "Timestamp -> Дата"),
        ("2", "Дата -> Timestamp"),
        ("0", "Назад")
    ], "Время", cfg)
    c = input("\n  > ").strip()
    if c == "0":
        return
    header(cfg)
    try:
        if c == "1":
            ts = float(input("  Unix Timestamp: "))
            dt = datetime.datetime.fromtimestamp(ts)
            print(f"\n  Дата: {paint(dt.strftime('%Y-%m-%d %H:%M:%S'), cfg)}")
        elif c == "2":
            ds = input("  Дата (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
            dt = datetime.datetime.strptime(ds, "%Y-%m-%d %H:%M:%S")
            print(f"\n  Timestamp: {paint(str(int(dt.timestamp())), cfg)}")
    except Exception as e:
        print(f"\n  Ошибка: {e}")
    pause()


def tools_menu(cfg):
    while True:
        header(cfg)
        draw_menu([
            ("1", "Генератор паролей"),
            ("2", "Счётчик строк/слов в файле"),
            ("3", "UUID-генератор"),
            ("4", "Хеш (md5/sha1/sha256)"),
            ("5", "Base64 кодирование/декодирование"),
            ("6", "Системная информация"),
            ("7", "Рандом и кубики"),
            ("8", "Конвертер времени"),
            ("9", "Назад"),
        ], "Инструменты", cfg)
        choice = input("\n  > ").strip()

        if choice == "1":   password_tool(cfg)
        elif choice == "2": counter_tool(cfg)
        elif choice == "3": uuid_tool(cfg)
        elif choice == "4": hash_tool(cfg)
        elif choice == "5": base64_tool(cfg)
        elif choice == "6": sysinfo_tool(cfg)
        elif choice == "7": random_tool(cfg)
        elif choice == "8": time_tool(cfg)
        elif choice == "9": return cfg


# ---------- О программе ----------

def about(cfg):
    clear()
    print_banner(cfg)
    print(f"""
  CACTUSTUI — консольный лаунчер.
  Версия: 0.6.1 (Fixed ASCII)
  Конфиг: {CONFIG_PATH}
  Темы: {', '.join(THEMES)}
""")
    pause()


# ---------- Точка входа ----------

def main():
    cfg = load_config()
    try:
        while True:
            header(cfg)
            draw_menu([
                ("1", "Настройки"),
                ("2", "Инструменты"),
                ("3", "О программе"),
                ("4", "Выход"),
            ], "Главное меню", cfg)
            choice = input("\n  > ").strip().lower()

            if choice == "1":   cfg = settings_menu(cfg)
            elif choice == "2": cfg = tools_menu(cfg)
            elif choice == "3": about(cfg)
            elif choice in ("4", "q"):
                clear()
                print("  Пока!")
                break
            else:
                print("  Нет такого пункта")
                pause()
    except KeyboardInterrupt:
        clear()
        print("  Прервано.")


if __name__ == "__main__":
    main()