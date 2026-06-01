#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOT EXPLORER - Versión APK MEJORADA
Explorar comunidades de bebés y seguir usuarios
"""

import time
import random
from datetime import datetime

try:
    import uiautomator2 as u2
except ImportError:
    print("ERROR: pip install uiautomator2")
    exit(1)

class BotExplorer:
    def __init__(self, logger=None):
        self.logger = logger
        self.device = None
        self.running = False
        self.stats = {
            "follows": 0,
            "perfiles": 0,
            "scrolls": 0,
            "fails": 0,
        }

        # Hashtags y perfiles semilla
        self.hashtags = ['bebé', 'bebe', 'mamabebe', 'bebealamodaa']
        self.perfiles_semilla = [
            'mustelaespana',
            'nuk_es',
            'babybjorn',
            'cubillomerce',
            'maternidadconpatas',
            'mamibeofficial',
            'cambrass_spain'
        ]

    def log(self, msg, level="INFO"):
        """Log personalizado"""
        ts = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{ts}] [{level}] {msg}"
        if self.logger:
            if level == "INFO":
                self.logger.info(msg)
            elif level == "WARN":
                self.logger.warn(msg)
            elif level == "ERROR":
                self.logger.error(msg)
            elif level == "OK":
                self.logger.ok(msg)
        print(log_msg)

    def connect(self):
        """Conectar a dispositivo"""
        try:
            self.log("Conectando a dispositivo...")
            self.device = u2.connect()
            self.log("✅ Dispositivo conectado", "OK")
            return True
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            return False

    def open_instagram(self):
        """Abrir Instagram"""
        try:
            self.log("Abriendo Instagram...")
            self.device.app_start("com.instagram.android", stop=False)
            time.sleep(5)
            self.log("✅ Instagram abierto", "OK")
            return True
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            return False

    def open_profile(self, username):
        """Abrir perfil"""
        try:
            self.log(f"Abriendo @{username}...")
            self.device.shell(f"am start -a android.intent.action.VIEW -d 'https://www.instagram.com/{username}/'")
            time.sleep(3)
            self.stats["perfiles"] += 1
            return True
        except Exception as e:
            self.log(f"Error abriendo perfil: {e}", "WARN")
            return False

    def open_followers(self):
        """Abrir lista de Seguidores"""
        try:
            self.log("Abriendo Seguidores...")
            self.device.tap(540, 330)  # Botón Seguidores
            time.sleep(3)
            self.log("✅ Seguidores abierto", "OK")
            return True
        except:
            return False

    def find_follow_buttons(self):
        """Buscar botones Seguir"""
        try:
            buttons = []
            for e in self.device.xpath('//*[@text="Seguir"]').all():
                b = e.info.get("bounds", {})
                if b:
                    cx = (b["left"] + b["right"]) // 2
                    cy = (b["top"] + b["bottom"]) // 2
                    if cy > 200:
                        buttons.append((cx, cy))
            return buttons
        except:
            return []

    def follow_user(self, x, y):
        """Dar follow a un usuario"""
        try:
            self.device.click(x, y)
            time.sleep(random.uniform(1.0, 2.5))
            self.stats["follows"] += 1
            self.log(f"✅ Seguido (Total: {self.stats['follows']})", "OK")
            return True
        except Exception as e:
            self.log(f"Error en follow: {e}", "WARN")
            self.stats["fails"] += 1
            return False

    def scroll(self):
        """Scroll en pantalla"""
        try:
            width = 1080
            height = 2340
            x = width // 2 + random.randint(-50, 50)
            y_start = int(height * 0.65)
            y_end = y_start - random.randint(300, 600)
            self.device.swipe(x, y_start, x, y_end, duration=0.7)
            self.stats["scrolls"] += 1
            return True
        except:
            return False

    def run(self, target=50):
        """Ejecutar bot"""
        self.running = True
        self.log("=" * 50, "INFO")
        self.log(f"🚀 BOT EXPLORER INICIADO - Objetivo: {target}", "INFO")
        self.log("=" * 50, "INFO")

        if not self.connect():
            return False

        if not self.open_instagram():
            return False

        time.sleep(2)

        # Trabajar con perfiles semilla
        for semilla in random.sample(self.perfiles_semilla, min(3, len(self.perfiles_semilla))):
            if not self.running or self.stats["follows"] >= target:
                break

            if not self.open_profile(semilla):
                continue

            time.sleep(2)

            # Abrir seguidores
            if not self.open_followers():
                self.log("No se pudo abrir Seguidores", "WARN")
                self.device.press('back')
                continue

            # Scroll y follow
            empty_scrolls = 0
            for _ in range(random.randint(3, 5)):
                if not self.running or self.stats["follows"] >= target:
                    break

                buttons = self.find_follow_buttons()
                self.log(f"Encontrados {len(buttons)} botones Seguir")

                if not buttons:
                    empty_scrolls += 1
                    if empty_scrolls >= 3:
                        break
                    self.scroll()
                    time.sleep(1.5)
                    continue

                empty_scrolls = 0

                for cx, cy in buttons:
                    if not self.running or self.stats["follows"] >= target:
                        break

                    # 60% de follow rate
                    if random.random() < 0.6:
                        self.follow_user(cx, cy)
                        time.sleep(random.uniform(3, 8))

                self.scroll()
                time.sleep(random.uniform(1.5, 2.5))

            # Volver atrás
            self.device.press('back')
            time.sleep(1)
            self.device.press('back')
            time.sleep(2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ BOT EXPLORER FINALIZADO", "OK")
        self.log(f"📊 Follows: {self.stats['follows']} | Perfiles: {self.stats['perfiles']} | Fallos: {self.stats['fails']}", "OK")
        self.log("=" * 50, "INFO")
        self.running = False
        return True

    def stop(self):
        """Detener bot"""
        self.running = False
        self.log("⏹️ Bot detenido", "WARN")
