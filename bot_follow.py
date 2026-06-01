#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOT FOLLOW - Versión APK
Ganar seguidores automáticamente
"""

import time
import random
from datetime import datetime

try:
    import uiautomator2 as u2
except ImportError:
    print("ERROR: pip install uiautomator2")
    exit(1)

class BotFollow:
    def __init__(self, logger=None):
        self.logger = logger
        self.device = None
        self.running = False

        self.perfiles_semilla = [
            'mustelaespana',
            'nuk_es',
            'babybjorn',
            'cubillomerce',
            'maternidadconpatas',
            'mamibeofficial',
            'cambrass_spain'
        ]

        self.stats = {
            "follows": 0,
            "perfiles": 0,
            "scrolls": 0,
        }

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
            self.log(f"Error conectando: {e}", "ERROR")
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
            self.log(f"Error abriendo Instagram: {e}", "ERROR")
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
        self.log(f"🚀 BOT FOLLOW INICIADO - Objetivo: {target}", "INFO")
        self.log("=" * 50, "INFO")

        if not self.connect():
            return False

        if not self.open_instagram():
            return False

        time.sleep(3)

        for semilla in random.sample(self.perfiles_semilla, len(self.perfiles_semilla)):
            if not self.running:
                break

            if self.stats["follows"] >= target:
                break

            if not self.open_profile(semilla):
                continue

            time.sleep(2)

            # Entrar en SEGUIDORES
            try:
                self.device.tap(540, 330)  # Botón Seguidores
                time.sleep(3)
            except:
                pass

            # Scroll y follow
            for _ in range(random.randint(3, 5)):
                if not self.running or self.stats["follows"] >= target:
                    break

                buttons = self.find_follow_buttons()
                self.log(f"Encontrados {len(buttons)} botones Seguir")

                for cx, cy in buttons:
                    if self.stats["follows"] >= target:
                        break
                    if random.random() < 0.7:  # 70% de follow
                        self.follow_user(cx, cy)
                        time.sleep(random.uniform(3, 8))

                self.scroll()
                time.sleep(random.uniform(1.5, 2.5))

            self.device.press('back')
            time.sleep(1)
            self.device.press('back')
            time.sleep(2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ BOT FOLLOW FINALIZADO", "OK")
        self.log(f"📊 Estadísticas: {self.stats['follows']} follows", "OK")
        self.log("=" * 50, "INFO")
        self.running = False
        return True

    def stop(self):
        """Detener bot"""
        self.running = False
        self.log("⏹️ Bot detenido", "WARN")
