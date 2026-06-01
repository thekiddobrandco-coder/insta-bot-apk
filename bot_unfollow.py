#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOT UNFOLLOW - Versión APK MEJORADA
Dejar de seguir automáticamente
"""

import time
import random
from datetime import datetime

try:
    import uiautomator2 as u2
except ImportError:
    print("ERROR: pip install uiautomator2")
    exit(1)

class BotUnfollow:
    def __init__(self, logger=None):
        self.logger = logger
        self.device = None
        self.running = False
        self.stats = {
            "unfollows": 0,
            "scrolls": 0,
            "fails": 0,
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

    def go_to_profile(self):
        """Ir a mi perfil"""
        try:
            self.log("Yendo a mi perfil...")
            self.device.tap(985, 2120)  # Botón Perfil
            time.sleep(3)
            self.log("✅ Perfil abierto", "OK")
            return True
        except:
            return False

    def go_to_following(self):
        """Ir a Seguidos"""
        try:
            self.log("Abriendo Seguidos...")
            self.device.tap(900, 490)  # Botón Seguidos
            time.sleep(3)
            self.log("✅ Seguidos abierto", "OK")
            return True
        except:
            return False

    def find_siguiendo_buttons(self):
        """Buscar botones Siguiendo"""
        try:
            buttons = []
            for e in self.device.xpath('//*[@text="Siguiendo"]').all():
                b = e.info.get("bounds", {})
                if b:
                    cx = (b["left"] + b["right"]) // 2
                    cy = (b["top"] + b["bottom"]) // 2
                    if cy > 200:
                        buttons.append((cx, cy))
            return buttons
        except:
            return []

    def unfollow_user(self, x, y):
        """Hacer unfollow a un usuario"""
        try:
            # Tap en Siguiendo
            self.device.click(x, y)
            time.sleep(1.5)

            # Buscar "Dejar de seguir" (reintentar 8 veces)
            for intento in range(8):
                e = self.device.xpath('//*[@text="Dejar de seguir"]')
                if e.exists:
                    e.get().click()
                    time.sleep(1.0)

                    # Verificar si se completó
                    time.sleep(0.5)
                    if not self.device.xpath('//*[@text="Siguiendo"]').exists:
                        self.log(f"✅ Unfollow completado", "OK")
                        self.stats["unfollows"] += 1
                        return True
                    else:
                        self.log(f"⚠️ Unfollow falló, reintentando...", "WARN")
                        break

                time.sleep(1.0)

            # Si falla, hacer back
            self.device.press('back')
            time.sleep(0.5)
            self.stats["fails"] += 1
            self.log(f"❌ No se pudo completar unfollow", "WARN")
            return False

        except Exception as e:
            self.log(f"Error: {e}", "WARN")
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
        self.log(f"🚀 BOT UNFOLLOW INICIADO - Objetivo: {target}", "INFO")
        self.log("=" * 50, "INFO")

        if not self.connect():
            return False

        if not self.open_instagram():
            return False

        time.sleep(2)

        if not self.go_to_profile():
            return False

        time.sleep(2)

        if not self.go_to_following():
            return False

        time.sleep(2)

        empty_scrolls = 0
        while self.running and self.stats["unfollows"] < target:
            buttons = self.find_siguiendo_buttons()
            self.log(f"Encontrados {len(buttons)} botones Siguiendo")

            if not buttons:
                empty_scrolls += 1
                if empty_scrolls >= 5:
                    self.log("Sin más usuarios para unfollow", "WARN")
                    break
                self.scroll()
                time.sleep(1.5)
                continue

            empty_scrolls = 0

            for cx, cy in buttons:
                if not self.running or self.stats["unfollows"] >= target:
                    break

                self.unfollow_user(cx, cy)
                time.sleep(random.uniform(30, 60))  # Esperar entre unfollows

            self.scroll()
            time.sleep(1.5)

        self.log("=" * 50, "INFO")
        self.log(f"✅ BOT UNFOLLOW FINALIZADO", "OK")
        self.log(f"📊 Unfollows: {self.stats['unfollows']} | Fallos: {self.stats['fails']}", "OK")
        self.log("=" * 50, "INFO")
        self.running = False
        return True

    def stop(self):
        """Detener bot"""
        self.running = False
        self.log("⏹️ Bot detenido", "WARN")
