import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import math
import psutil

from voice import listen, speak
from ai.brain import ask_ai
from core.executor import execute_plan


class JarvisGUI:

    def __init__(self, root):

        self.root = root

        # =====================================================
        # WINDOW
        # =====================================================

        self.root.title(
            "J.A.R.V.I.S - AI Desktop Assistant"
        )

        self.root.geometry(
            "1250x760"
        )

        self.root.configure(
            bg="#03070c"
        )

        self.root.resizable(
            False,
            False
        )

        # =====================================================
        # STATE
        # =====================================================

        self.listening = False
        self.processing = False
        self.running = True

        self.angle = 0

        # =====================================================
        # COLORS
        # =====================================================

        self.BG = "#03070c"
        self.PANEL = "#08111b"
        self.PANEL2 = "#0d1925"

        self.CYAN = "#00e5ff"
        self.BLUE = "#008cff"
        self.GREEN = "#00ff9d"
        self.RED = "#ff3158"
        self.ORANGE = "#ffae00"

        self.WHITE = "#e9faff"
        self.GRAY = "#78909c"

        # =====================================================
        # BUILD
        # =====================================================

        self.build_gui()

        self.update_clock()
        self.update_system_stats()
        self.animate_core()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    # =========================================================
    # BUILD GUI
    # =========================================================

    def build_gui(self):

        # =====================================================
        # TOP BAR
        # =====================================================

        top = tk.Frame(
            self.root,
            bg=self.PANEL,
            height=72
        )

        top.pack(
            fill="x"
        )

        logo = tk.Label(
            top,
            text="J.A.R.V.I.S",
            font=(
                "Segoe UI",
                25,
                "bold"
            ),
            fg=self.CYAN,
            bg=self.PANEL
        )

        logo.place(
            x=28,
            y=8
        )

        subtitle = tk.Label(
            top,
            text="JUST A RATHER VERY INTELLIGENT SYSTEM",
            font=(
                "Consolas",
                8
            ),
            fg=self.GRAY,
            bg=self.PANEL
        )

        subtitle.place(
            x=32,
            y=45
        )

        self.ai_status = tk.Label(
            top,
            text="● AI CORE ONLINE",
            font=(
                "Consolas",
                10,
                "bold"
            ),
            fg=self.GREEN,
            bg=self.PANEL
        )

        self.ai_status.place(
            x=490,
            y=28
        )

        self.clock = tk.Label(
            top,
            text="00:00:00",
            font=(
                "Consolas",
                18,
                "bold"
            ),
            fg=self.WHITE,
            bg=self.PANEL
        )

        self.clock.place(
            x=1060,
            y=20
        )

        # =====================================================
        # LEFT SIDEBAR
        # =====================================================

        sidebar = tk.Frame(
            self.root,
            bg=self.PANEL
        )

        sidebar.place(
            x=18,
            y=90,
            width=210,
            height=650
        )

        side_title = tk.Label(
            sidebar,
            text="CONTROL CENTER",
            font=(
                "Consolas",
                10,
                "bold"
            ),
            fg=self.CYAN,
            bg=self.PANEL
        )

        side_title.pack(
            pady=(20, 15)
        )

        self.side_button(
            sidebar,
            "🎤  Voice Command",
            self.start_listening
        )

        self.side_button(
            sidebar,
            "🌐  Open Google",
            lambda: self.run_command(
                "open Google"
            )
        )

        self.side_button(
            sidebar,
            "▶  Open YouTube",
            lambda: self.run_command(
                "open YouTube"
            )
        )

        self.side_button(
            sidebar,
            "🌐  Open Chrome",
            lambda: self.run_command(
                "open Chrome"
            )
        )

        self.side_button(
            sidebar,
            "📝  Open Notepad",
            lambda: self.run_command(
                "open Notepad"
            )
        )

        self.side_button(
            sidebar,
            "🔢  Calculator",
            lambda: self.run_command(
                "open calculator"
            )
        )

        self.side_button(
            sidebar,
            "📁  File Explorer",
            lambda: self.run_command(
                "open file explorer"
            )
        )

        self.side_button(
            sidebar,
            "📸  Screenshot",
            lambda: self.run_command(
                "take a screenshot"
            )
        )

        tk.Frame(
            sidebar,
            bg="#183040",
            height=1
        ).pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.side_button(
            sidebar,
            "🧠  AI Test",
            lambda: self.run_command(
                "tell me a short interesting fact"
            )
        )

        self.side_button(
            sidebar,
            "🗑  Clear Console",
            self.clear_console
        )

        self.side_button(
            sidebar,
            "✕  Exit JARVIS",
            self.close,
            danger=True
        )

        # =====================================================
        # CENTER
        # =====================================================

        center = tk.Frame(
            self.root,
            bg=self.BG
        )

        center.place(
            x=245,
            y=90,
            width=620,
            height=650
        )

        self.canvas = tk.Canvas(
            center,
            width=600,
            height=360,
            bg=self.BG,
            highlightthickness=0
        )

        self.canvas.pack()

        # =====================================================
        # STATUS
        # =====================================================

        self.status = tk.Label(
            center,
            text="SYSTEM ONLINE",
            font=(
                "Segoe UI",
                16,
                "bold"
            ),
            fg=self.GREEN,
            bg=self.BG
        )

        self.status.pack()

        self.status_detail = tk.Label(
            center,
            text="AI core ready. Waiting for command...",
            font=(
                "Consolas",
                9
            ),
            fg=self.GRAY,
            bg=self.BG
        )

        self.status_detail.pack(
            pady=(4, 15)
        )

        # =====================================================
        # VOICE BUTTON
        # =====================================================

        self.voice_button = tk.Button(
            center,
            text="🎤  ACTIVATE VOICE",
            command=self.start_listening,
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            fg=self.BG,
            bg=self.CYAN,
            activebackground=self.BLUE,
            activeforeground=self.WHITE,
            relief="flat",
            cursor="hand2",
            width=24,
            height=2
        )

        self.voice_button.pack(
            pady=5
        )

        # =====================================================
        # SYSTEM STATS
        # =====================================================

        stats = tk.Frame(
            center,
            bg=self.BG
        )

        stats.pack(
            pady=18
        )

        self.cpu_card = self.stat_card(
            stats,
            "CPU",
            "0%"
        )

        self.ram_card = self.stat_card(
            stats,
            "RAM",
            "0%"
        )

        self.disk_card = self.stat_card(
            stats,
            "DISK",
            "0%"
        )

        # =====================================================
        # RIGHT CONSOLE
        # =====================================================

        right = tk.Frame(
            self.root,
            bg=self.PANEL,
            bd=1,
            relief="solid"
        )

        right.place(
            x=880,
            y=90,
            width=350,
            height=650
        )

        console_title = tk.Label(
            right,
            text="AI COMMAND LOG",
            font=(
                "Consolas",
                12,
                "bold"
            ),
            fg=self.CYAN,
            bg=self.PANEL
        )

        console_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        # =====================================================
        # CONSOLE
        # =====================================================

        self.console = scrolledtext.ScrolledText(
            right,
            bg="#040a10",
            fg=self.WHITE,
            insertbackground=self.CYAN,
            font=(
                "Consolas",
                9
            ),
            relief="flat",
            wrap="word"
        )

        self.console.pack(
            padx=12,
            pady=10,
            fill="both",
            expand=True
        )

        self.console.config(
            state="disabled"
        )

        # =====================================================
        # INPUT
        # =====================================================

        entry_frame = tk.Frame(
            right,
            bg=self.PANEL
        )

        entry_frame.pack(
            fill="x",
            padx=12,
            pady=12
        )

        self.entry = tk.Entry(
            entry_frame,
            bg=self.PANEL2,
            fg=self.WHITE,
            insertbackground=self.CYAN,
            font=(
                "Segoe UI",
                10
            ),
            relief="flat"
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        self.entry.bind(
            "<Return>",
            lambda event: self.send_text()
        )

        send = tk.Button(
            entry_frame,
            text="SEND",
            command=self.send_text,
            font=(
                "Consolas",
                9,
                "bold"
            ),
            fg=self.BG,
            bg=self.CYAN,
            relief="flat",
            cursor="hand2"
        )

        send.pack(
            side="right",
            padx=(5, 0),
            ipady=7
        )

        # =====================================================
        # WELCOME
        # =====================================================

        self.add_message(
            "JARVIS",
            "Advanced AI core initialized."
        )

        self.add_message(
            "SYSTEM",
            "Natural language interface ready."
        )

        self.add_message(
            "SYSTEM",
            "Voice interface ready."
        )

    # =========================================================
    # SIDEBAR BUTTON
    # =========================================================

    def side_button(
        self,
        parent,
        text,
        command,
        danger=False
    ):

        color = (
            self.RED
            if danger
            else self.WHITE
        )

        button = tk.Button(
            parent,
            text=text,
            command=command,
            anchor="w",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=color,
            bg=self.PANEL,
            activebackground=self.PANEL2,
            activeforeground=self.CYAN,
            relief="flat",
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=10,
            pady=3,
            ipady=7
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def stat_card(
        self,
        parent,
        title,
        value
    ):

        frame = tk.Frame(
            parent,
            bg=self.PANEL,
            width=165,
            height=65
        )

        frame.pack(
            side="left",
            padx=5
        )

        frame.pack_propagate(
            False
        )

        tk.Label(
            frame,
            text=title,
            font=(
                "Consolas",
                8,
                "bold"
            ),
            fg=self.GRAY,
            bg=self.PANEL
        ).pack(
            pady=(8, 0)
        )

        label = tk.Label(
            frame,
            text=value,
            font=(
                "Consolas",
                15,
                "bold"
            ),
            fg=self.CYAN,
            bg=self.PANEL
        )

        label.pack()

        return label

    # =========================================================
    # CLOCK
    # =========================================================

    def update_clock(self):

        if not self.running:
            return

        now = datetime.datetime.now()

        self.clock.config(
            text=now.strftime(
                "%H:%M:%S"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )

    # =========================================================
    # SYSTEM STATS
    # =========================================================

    def update_system_stats(self):

        if not self.running:
            return

        try:

            cpu = psutil.cpu_percent()

            ram = psutil.virtual_memory().percent

            disk = psutil.disk_usage(
                "/"
            ).percent

            self.cpu_card.config(
                text=f"{cpu:.0f}%"
            )

            self.ram_card.config(
                text=f"{ram:.0f}%"
            )

            self.disk_card.config(
                text=f"{disk:.0f}%"
            )

        except Exception:
            pass

        self.root.after(
            1500,
            self.update_system_stats
        )

    # =========================================================
    # AI CORE ANIMATION
    # =========================================================

    def animate_core(self):

        if not self.running:
            return

        self.canvas.delete(
            "all"
        )

        cx = 300
        cy = 175

        self.angle += 3

        pulse = (
            5 *
            math.sin(
                self.angle *
                math.pi /
                40
            )
        )

        # Outer rings

        for radius in [
            145,
            125,
            105,
            82
        ]:

            self.canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                outline="#073c4b",
                width=1
            )

        # Main ring

        r = 62 + pulse

        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            outline=self.CYAN,
            width=3
        )

        # Rotating particles

        for i in range(12):

            angle = (
                self.angle +
                i * 30
            ) * math.pi / 180

            radius = 135

            x = (
                cx +
                math.cos(angle) *
                radius
            )

            y = (
                cy +
                math.sin(angle) *
                radius
            )

            size = 3

            self.canvas.create_oval(
                x - size,
                y - size,
                x + size,
                y + size,
                fill=self.CYAN,
                outline=""
            )

        # Core

        self.canvas.create_oval(
            cx - 48,
            cy - 48,
            cx + 48,
            cy + 48,
            fill="#061a25",
            outline=self.CYAN,
            width=3
        )

        # J

        self.canvas.create_text(
            cx,
            cy,
            text="J",
            font=(
                "Segoe UI",
                38,
                "bold"
            ),
            fill=self.CYAN
        )

        # Label

        self.canvas.create_text(
            cx,
            cy + 95,
            text="JARVIS AI CORE",
            font=(
                "Consolas",
                10,
                "bold"
            ),
            fill=self.GRAY
        )

        self.root.after(
            40,
            self.animate_core
        )

    # =========================================================
    # CONSOLE MESSAGE
    # =========================================================

    def add_message(
        self,
        sender,
        message
    ):

        try:

            self.console.config(
                state="normal"
            )

            time_now = datetime.datetime.now().strftime(
                "%H:%M:%S"
            )

            self.console.insert(
                "end",
                f"[{time_now}] {sender}\n"
            )

            self.console.insert(
                "end",
                f"{message}\n\n"
            )

            self.console.see(
                "end"
            )

            self.console.config(
                state="disabled"
            )

        except Exception:
            pass

    # =========================================================
    # TEXT COMMAND
    # =========================================================

    def send_text(self):

        if self.processing:
            return

        command = self.entry.get().strip()

        if not command:
            return

        self.entry.delete(
            0,
            "end"
        )

        self.run_command(
            command
        )

    # =========================================================
    # RUN COMMAND
    # =========================================================

    def run_command(
        self,
        command
    ):

        if self.processing:
            return

        if not command:
            return

        self.add_message(
            "YOU",
            command
        )

        self.status.config(
            text="AI THINKING",
            fg=self.CYAN
        )

        self.status_detail.config(
            text="Understanding your request..."
        )

        self.ai_status.config(
            text="● AI PROCESSING",
            fg=self.CYAN
        )

        self.processing = True

        threading.Thread(
            target=self.process_command,
            args=(command,),
            daemon=True
        ).start()

    # =========================================================
    # AI COMMAND PROCESSOR
    # =========================================================

    def process_command(
        self,
        command
    ):

        try:

            # -------------------------------------------------
            # AI BRAIN
            # -------------------------------------------------

            self.root.after(
                0,
                lambda: self.status_detail.config(
                    text="AI is planning the task..."
                )
            )

            plan = ask_ai(
                command
            )

            # -------------------------------------------------
            # SHOW PLAN
            # -------------------------------------------------

            self.root.after(
                0,
                lambda: self.add_message(
                    "AI PLAN",
                    str(plan)
                )
            )

            # -------------------------------------------------
            # EXECUTE
            # -------------------------------------------------

            self.root.after(
                0,
                lambda: self.status_detail.config(
                    text="Executing AI actions..."
                )
            )

            response = execute_plan(
                plan
            )

            # -------------------------------------------------
            # RESPONSE
            # -------------------------------------------------

            if response:

                self.root.after(
                    0,
                    lambda r=response:
                    self.add_message(
                        "JARVIS",
                        r
                    )
                )

                speak(
                    response
                )

            else:

                response = (
                    "I completed the task, "
                    "but I don't have a response."
                )

                self.root.after(
                    0,
                    lambda r=response:
                    self.add_message(
                        "JARVIS",
                        r
                    )
                )

                speak(
                    response
                )

        except Exception as error:

            error_text = (
                f"AI Error: {error}"
            )

            self.root.after(
                0,
                lambda e=error_text:
                self.add_message(
                    "ERROR",
                    e
                )
            )

        finally:

            self.root.after(
                0,
                self.set_ready
            )

    # =========================================================
    # VOICE START
    # =========================================================

    def start_listening(self):

        if self.listening:
            return

        if self.processing:
            return

        self.listening = True

        self.voice_button.config(
            text="🔴  LISTENING...",
            state="disabled",
            bg=self.RED
        )

        self.status.config(
            text="LISTENING",
            fg=self.RED
        )

        self.status_detail.config(
            text="Speak your command..."
        )

        self.ai_status.config(
            text="● VOICE ACTIVE",
            fg=self.RED
        )

        self.add_message(
            "SYSTEM",
            "Microphone activated. Speak now."
        )

        threading.Thread(
            target=self.voice_thread,
            daemon=True
        ).start()

    # =========================================================
    # VOICE THREAD
    # =========================================================

    def voice_thread(self):

        try:

            command = listen()

            if not command:

                self.root.after(
                    0,
                    lambda: self.add_message(
                        "SYSTEM",
                        "No command detected."
                    )
                )

                self.root.after(
                    0,
                    self.set_ready
                )

                return

            # Voice command received

            self.root.after(
                0,
                lambda c=command:
                self.add_message(
                    "YOU",
                    c
                )
            )

            self.root.after(
                0,
                lambda: self.status.config(
                    text="AI THINKING",
                    fg=self.CYAN
                )
            )

            self.root.after(
                0,
                lambda: self.status_detail.config(
                    text="Understanding voice command..."
                )
            )

            self.root.after(
                0,
                lambda: self.ai_status.config(
                    text="● AI PROCESSING",
                    fg=self.CYAN
                )
            )

            self.processing = True

            # -------------------------------------------------
            # AI BRAIN
            # -------------------------------------------------

            plan = ask_ai(
                command
            )

            self.root.after(
                0,
                lambda p=plan:
                self.add_message(
                    "AI PLAN",
                    str(p)
                )
            )

            # -------------------------------------------------
            # EXECUTE
            # -------------------------------------------------

            response = execute_plan(
                plan
            )

            if response:

                self.root.after(
                    0,
                    lambda r=response:
                    self.add_message(
                        "JARVIS",
                        r
                    )
                )

                speak(
                    response
                )

        except Exception as error:

            error_text = (
                f"Voice Error: {error}"
            )

            self.root.after(
                0,
                lambda e=error_text:
                self.add_message(
                    "ERROR",
                    e
                )
            )

        finally:

            self.root.after(
                0,
                self.set_ready
            )

    # =========================================================
    # READY STATE
    # =========================================================

    def set_ready(self):

        if not self.running:
            return

        self.listening = False
        self.processing = False

        self.voice_button.config(
            text="🎤  ACTIVATE VOICE",
            state="normal",
            bg=self.CYAN
        )

        self.status.config(
            text="SYSTEM ONLINE",
            fg=self.GREEN
        )

        self.status_detail.config(
            text="AI core ready. Waiting for command..."
        )

        self.ai_status.config(
            text="● AI CORE ONLINE",
            fg=self.GREEN
        )

    # =========================================================
    # CLEAR CONSOLE
    # =========================================================

    def clear_console(self):

        self.console.config(
            state="normal"
        )

        self.console.delete(
            "1.0",
            "end"
        )

        self.console.config(
            state="disabled"
        )

        self.add_message(
            "SYSTEM",
            "Console cleared."
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.running = False

        try:

            self.root.destroy()

        except Exception:
            pass


# =============================================================
# DIRECT RUN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = JarvisGUI(
        root
    )

    root.mainloop()