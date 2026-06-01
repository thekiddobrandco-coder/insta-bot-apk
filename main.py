#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTAGRAM BOT MASTER - APK
Interfaz Kivy para ejecutar 3 bots: Follow, Unfollow, Explorador
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock

import threading
import time
from datetime import datetime

# Importar bots
try:
    from bot_follow import BotFollow
    from bot_unfollow import BotUnfollow
    from bot_explorer import BotExplorer
except ImportError as e:
    print(f"Error importando bots: {e}")

# Configurar ventana
Window.size = (1080, 1920)
kivy.require('2.0')

# ==============================================================
# LOGGER PERSONALIZADO
# ==============================================================

class BotLogger:
    def __init__(self, callback=None):
        self.logs = []
        self.callback = callback
        self.max_logs = 500

    def write(self, msg, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{ts}] [{level}] {msg}"
        self.logs.append(log_line)

        # Mantener solo últimos N logs
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

        if self.callback:
            Clock.schedule_once(lambda dt: self.callback(log_line), 0)

    def info(self, msg):
        self.write(msg, "INFO")

    def warn(self, msg):
        self.write(msg, "WARN")

    def error(self, msg):
        self.write(msg, "ERROR")

    def ok(self, msg):
        self.write(msg, "OK")

    def get_logs(self):
        return "\n".join(self.logs[-100:])  # Últimos 100 logs

# ==============================================================
# BOT EXECUTOR
# ==============================================================

class BotExecutor:
    def __init__(self, logger):
        self.logger = logger
        self.running = False
        self.current_process = None
        self.thread = None

    def run_bot_follow(self):
        """Ejecutar Bot Follow"""
        self.logger.info("🚀 Iniciando BOT FOLLOW (Ganar Seguidores)...")
        self._execute_bot("bot_follow")

    def run_bot_unfollow(self):
        """Ejecutar Bot Unfollow"""
        self.logger.info("🚀 Iniciando BOT UNFOLLOW (Dejar de Seguir)...")
        self._execute_bot("bot_unfollow")

    def run_bot_explorer(self):
        """Ejecutar Bot Explorer (Comunidades)"""
        self.logger.info("🚀 Iniciando BOT EXPLORER (Comunidades)...")
        self._execute_bot("bot_explorer")

    def _execute_bot(self, bot_name):
        """Ejecutar un bot en thread separado"""
        if self.running:
            self.logger.warn("Ya hay un bot ejecutándose")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_bot_thread, args=(bot_name,), daemon=True)
        self.thread.start()

    def _run_bot_thread(self, bot_name):
        """Thread que ejecuta el bot"""
        try:
            if bot_name == "bot_follow":
                bot = BotFollow(logger=self.logger)
                bot.run(target=50)

            elif bot_name == "bot_unfollow":
                bot = BotUnfollow(logger=self.logger)
                bot.run(target=50)

            elif bot_name == "bot_explorer":
                bot = BotExplorer(logger=self.logger)
                bot.run(target=50)

            else:
                self.logger.error(f"Bot desconocido: {bot_name}")

        except Exception as e:
            self.logger.error(f"Error ejecutando {bot_name}: {e}")
        finally:
            self.running = False

    def stop_bot(self):
        """Detener bot en ejecución"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.logger.warn("⏹️ Bot detenido")
            except:
                pass
        self.running = False

# ==============================================================
# MAIN APP
# ==============================================================

class InstagramBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = BotLogger(callback=self.on_log)
        self.executor = BotExecutor(self.logger)
        self.log_label = None

    def on_log(self, log_msg):
        """Callback cuando hay nuevo log"""
        if self.log_label:
            self.log_label.text = self.logger.get_logs()

    def build(self):
        """Construir interfaz"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # HEADER
        header = Label(
            text="📱 INSTAGRAM BOT MASTER",
            size_hint_y=0.08,
            bold=True,
            font_size='24sp',
            color=(0.2, 0.6, 1.0, 1.0)
        )
        main_layout.add_widget(header)

        # BOTS GRID (3 botones principales)
        bots_grid = GridLayout(cols=1, spacing=10, size_hint_y=0.35)

        # Botón FOLLOW
        btn_follow = Button(
            text="👥 GANAR SEGUIDORES\n(Bot Follow)",
            size_hint_y=0.33,
            background_color=(0.2, 0.8, 0.3, 1.0),
            bold=True,
            font_size='18sp'
        )
        btn_follow.bind(on_press=self.on_click_follow)
        bots_grid.add_widget(btn_follow)

        # Botón UNFOLLOW
        btn_unfollow = Button(
            text="❌ DEJAR DE SEGUIR\n(Bot Unfollow)",
            size_hint_y=0.33,
            background_color=(1.0, 0.4, 0.2, 1.0),
            bold=True,
            font_size='18sp'
        )
        btn_unfollow.bind(on_press=self.on_click_unfollow)
        bots_grid.add_widget(btn_unfollow)

        # Botón EXPLORER
        btn_explorer = Button(
            text="🔍 EXPLORAR COMUNIDADES\n(Hashtag Bebés)",
            size_hint_y=0.33,
            background_color=(0.8, 0.2, 0.8, 1.0),
            bold=True,
            font_size='18sp'
        )
        btn_explorer.bind(on_press=self.on_click_explorer)
        bots_grid.add_widget(btn_explorer)

        main_layout.add_widget(bots_grid)

        # CONTROL BUTTONS
        control_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.08)

        btn_stop = Button(
            text="⏹️ STOP",
            background_color=(0.8, 0.2, 0.2, 1.0),
            bold=True
        )
        btn_stop.bind(on_press=self.on_click_stop)
        control_grid.add_widget(btn_stop)

        btn_clear = Button(
            text="🗑️ LIMPIAR LOGS",
            background_color=(0.5, 0.5, 0.5, 1.0),
            bold=True
        )
        btn_clear.bind(on_press=self.on_click_clear)
        control_grid.add_widget(btn_clear)

        main_layout.add_widget(control_grid)

        # LOGS (Scroll)
        logs_label = Label(
            text="[LOGS]",
            size_hint_y=0.49,
            markup=True,
            valign='top',
            font_size='12sp'
        )
        self.log_label = logs_label

        logs_scroll = ScrollView(size_hint_y=0.49)
        logs_scroll.add_widget(logs_label)
        main_layout.add_widget(logs_scroll)

        # Log inicial
        self.logger.ok("APP INICIADA - Selecciona un bot para empezar")

        return main_layout

    def on_click_follow(self, instance):
        """Click en Follow"""
        self.executor.run_bot_follow()

    def on_click_unfollow(self, instance):
        """Click en Unfollow"""
        self.executor.run_bot_unfollow()

    def on_click_explorer(self, instance):
        """Click en Explorer"""
        self.executor.run_bot_explorer()

    def on_click_stop(self, instance):
        """Click en Stop"""
        self.executor.stop_bot()
        self.logger.warn("⏹️ Deteniendo bot...")

    def on_click_clear(self, instance):
        """Click en Clear logs"""
        self.logger.logs = []
        self.log_label.text = "[LOGS LIMPIOS]"

if __name__ == '__main__':
    InstagramBotApp().run()
