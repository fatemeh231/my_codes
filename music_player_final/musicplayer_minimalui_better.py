import os
import json
import pygame
from io import BytesIO
from tkinter import filedialog, StringVar
from PIL import Image, ImageTk
from customtkinter import *
from mutagen.mp3 import MP3
from mutagen import File as MutagenFile
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import psycopg2
import psycopg2.extras


# ============================================================
# DATABASE LAYER
# ============================================================

class Database:
    def __init__(
        self,
        host="localhost",
        port=5432,
        dbname="musicplayer",
        user="postgres",
        password="asal1234@",
    ):
        self.conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS songs (
                id SERIAL PRIMARY KEY,
                path TEXT UNIQUE,
                play_count INTEGER DEFAULT 0,
                features JSONB DEFAULT NULL
            );
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                id SERIAL PRIMARY KEY,
                song_path TEXT UNIQUE
            );
        """
        )

        self.conn.commit()

    # ---------- Songs ----------

    def add_song(self, path):
        self.cursor.execute(
            """
            INSERT INTO songs (path)
            VALUES (%s)
            ON CONFLICT (path) DO NOTHING;
        """,
            (path,),
        )
        self.conn.commit()

    def get_songs(self):
        self.cursor.execute("SELECT path FROM songs ORDER BY id;")
        return [row[0] for row in self.cursor.fetchall()]

    def delete_song(self, path):
        self.cursor.execute("DELETE FROM songs WHERE path = %s;", (path,))
        self.cursor.execute("DELETE FROM favorites WHERE song_path = %s;", (path,))
        self.conn.commit()

    # ---------- Play count ----------

    def increment_play_count(self, path):
        self.cursor.execute(
            """
            UPDATE songs
            SET play_count = play_count + 1
            WHERE path = %s;
        """,
            (path,),
        )
        self.conn.commit()

    def get_play_count(self, path):
        self.cursor.execute(
            "SELECT play_count FROM songs WHERE path = %s;",
            (path,),
        )
        row = self.cursor.fetchone()
        return row[0] if row else 0

    def get_most_played(self):
        self.cursor.execute("SELECT path FROM songs ORDER BY play_count DESC;")
        return [row[0] for row in self.cursor.fetchall()]

    def get_recently_added(self):
        self.cursor.execute("SELECT path FROM songs ORDER BY id DESC;")
        return [row[0] for row in self.cursor.fetchall()]

    # ---------- Favorites ----------

    def add_favorite(self, path):
        self.cursor.execute(
            """
            INSERT INTO favorites (song_path)
            VALUES (%s)
            ON CONFLICT (song_path) DO NOTHING;
        """,
            (path,),
        )
        self.conn.commit()

    def remove_favorite(self, path):
        self.cursor.execute(
            "DELETE FROM favorites WHERE song_path = %s;",
            (path,),
        )
        self.conn.commit()

    def get_favorites(self):
        self.cursor.execute("SELECT song_path FROM favorites;")
        return [row[0] for row in self.cursor.fetchall()]

    # ---------- Features (not used now, but kept) ----------

    def save_features(self, path, features_dict):
        self.cursor.execute(
            """
            UPDATE songs
            SET features = %s
            WHERE path = %s;
        """,
            (psycopg2.extras.Json(features_dict), path),
        )
        self.conn.commit()

    def get_features(self, path):
        self.cursor.execute(
            "SELECT features FROM songs WHERE path = %s;",
            (path,),
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    # ---------- Close ----------

    def close(self):
        self.cursor.close()
        self.conn.close()


# ============================================================
# MUSIC PLAYER
# ============================================================

class MusicPlayer:
    def __init__(self):
        # ---------- Backend ----------
        self.db = Database()
        self.seek_offset = 0
        self.last_seek_time = 0

        # ---------- Theme ----------
        self.theme_path = r"C:\Users\fatemeh\OneDrive\Desktop\customtkinter_additional_theme"
        self.default_theme = "carrot.json"
        self.current_theme = {}

        # ---------- Tk / Pygame ----------
        set_appearance_mode("light")
        set_default_color_theme("blue")
        pygame.mixer.init()

        self.app = CTk()
        self.app.title("Music Player")
        self.app.geometry("1100x700")

        self.app.grid_columnconfigure(0, weight=3)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)

        # ---------- State ----------
        self.song_list = self.db.get_songs()
        self.current_song = None
        self.song_duration = 0.0
        self.dragging = False

        self.view_mode = "All"
        self.sort_mode = "A-Z"
        self.search_var = StringVar()
        self.display_list = []

        # Theme targets
        self.frames = []
        self.buttons = []
        self.labels = []
        self.sliders = []
        self.textboxes = []
        self.combos = []

        # Anim flags
        self.volume_glow_active = False
        self.progress_pulse_on = False
        self.progress_pulse_state = 0
        self.favorite_animating = False

        # Widget refs
        self.volume_slider = None
        self.progress = None
        self.time_label = None
        self.favorite_btn = None
        self.cover = None
        self.playlist = None

        # ---------- UI ----------
        self.build_ui()
        self.refresh_playlist()

        # ---------- Theme load ----------
        self.current_theme = self.load_theme(self.default_theme)
        self.apply_theme(self.current_theme)

        self.app.protocol("WM_DELETE_WINDOW", self.close)
        self.app.mainloop()

    # ============================================================
    # LIST / FILTER / SORT
    # ============================================================

    def base_list(self):
        if self.view_mode == "Favorites":
            favs = set(self.db.get_favorites())
            return [s for s in self.song_list if s in favs]
        return list(self.song_list)

    def sorted_list(self, songs):
        if self.sort_mode == "A-Z":
            return sorted(songs, key=lambda p: os.path.basename(p).lower())
        if self.sort_mode == "Z-A":
            return sorted(songs, key=lambda p: os.path.basename(p).lower(), reverse=True)
        if self.sort_mode == "Most Played":
            return sorted(songs, key=lambda p: self.db.get_play_count(p), reverse=True)
        if self.sort_mode == "Recently Added":
            order = self.db.get_recently_added()
            idx = {p: i for i, p in enumerate(order)}
            return sorted(songs, key=lambda p: idx.get(p, 1_000_000))
        return songs

    def filtered_list(self):
        songs = self.sorted_list(self.base_list())
        q = self.search_var.get().strip().lower()
        if not q:
            return songs
        return [s for s in songs if q in os.path.basename(s).lower()]

    def refresh_playlist(self):
        self.display_list = self.filtered_list()
        self.playlist.configure(state="normal")
        self.playlist.delete("1.0", "end")

        favs = set(self.db.get_favorites())
        for i, s in enumerate(self.display_list):
            name = os.path.basename(s)
            count = self.db.get_play_count(s)
            mark = " ♥" if s in favs else ""
            self.playlist.insert("end", f"{i+1}. {name}  [{count}] {mark}\n")

        self.playlist.configure(state="disabled")
        self.update_playlist_highlight()

    def update_playlist_highlight(self):
        try:
            self.playlist.tag_delete("current")
        except:
            pass

        if self.current_song is None:
            return

        current_path = self.song_list[self.current_song]
        if current_path in self.display_list:
            line = self.display_list.index(current_path)
            start = f"{line+1}.0"
            end = f"{line+1}.end"
            self.playlist.configure(state="normal")
            self.playlist.tag_add("current", start, end)
            self.playlist.tag_config("current", background="#444444", foreground="#ffffff")
            self.playlist.configure(state="disabled")

    # ============================================================
    # THEME SYSTEM
    # ============================================================

    def mode_index(self):
        return 0 if get_appearance_mode().lower() == "light" else 1

    def load_theme(self, name):
        try:
            with open(os.path.join(self.theme_path, name), "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def pick(self, section, key, fallback=None):
        if key not in section:
            return fallback
        val = section[key]
        if isinstance(val, list):
            idx = self.mode_index()
            return val[idx] if idx < len(val) else val[0]
        return val

    def apply_theme(self, theme):
        if not theme:
            return

        t_app = theme.get("CTk", {})
        t_frame = theme.get("CTkFrame", {})
        t_btn = theme.get("CTkButton", {})
        t_lbl = theme.get("CTkLabel", {})
        t_sld = theme.get("CTkSlider", {})
        t_txt = theme.get("CTkTextbox", {})
        t_cmb = theme.get("CTkComboBox", {})

        bg = self.pick(t_app, "fg_color")
        if bg:
            self.app.configure(fg_color=bg)

        fr = self.pick(t_frame, "fg_color")
        for f in self.frames:
            if fr:
                f.configure(fg_color=fr)

        b_fg = self.pick(t_btn, "fg_color")
        b_hv = self.pick(t_btn, "hover_color")
        b_tx = self.pick(t_btn, "text_color")
        for b in self.buttons:
            cfg = {}
            if b_fg:
                cfg["fg_color"] = b_fg
            if b_hv:
                cfg["hover_color"] = b_hv
            if b_tx:
                cfg["text_color"] = b_tx
            if cfg:
                b.configure(**cfg)

        l_tx = self.pick(t_lbl, "text_color")
        for l in self.labels:
            if l_tx:
                l.configure(text_color=l_tx)

        s_fg = self.pick(t_sld, "fg_color")
        s_pr = self.pick(t_sld, "progress_color")
        s_bt = self.pick(t_sld, "button_color")
        s_hv = self.pick(t_sld, "button_hover_color")
        for s in self.sliders:
            cfg = {}
            if s_fg:
                cfg["fg_color"] = s_fg
            if s_pr:
                cfg["progress_color"] = s_pr
            if s_bt:
                cfg["button_color"] = s_bt
            if s_hv:
                cfg["button_hover_color"] = s_hv
            if cfg:
                s.configure(**cfg)

        t_fg = self.pick(t_txt, "fg_color")
        t_tx = self.pick(t_txt, "text_color")
        for t in self.textboxes:
            cfg = {}
            if t_fg:
                cfg["fg_color"] = t_fg
            if t_tx:
                cfg["text_color"] = t_tx
            if cfg:
                t.configure(**cfg)

        c_fg = self.pick(t_cmb, "fg_color")
        c_bd = self.pick(t_cmb, "border_color")
        c_bt = self.pick(t_cmb, "button_color")
        c_hv = self.pick(t_cmb, "button_hover_color")
        c_tx = self.pick(t_cmb, "text_color")
        for c in self.combos:
            cfg = {}
            if c_fg:
                cfg["fg_color"] = c_fg
            if c_bd:
                cfg["border_color"] = c_bd
            if c_bt:
                cfg["button_color"] = c_bt
            if c_hv:
                cfg["button_hover_color"] = c_hv
            if c_tx:
                cfg["text_color"] = c_tx
            if cfg:
                c.configure(**cfg)

    def change_theme(self, name):
        self.current_theme = self.load_theme(name)
        self.apply_theme(self.current_theme)

    def change_mode(self, mode):
        set_appearance_mode(mode.lower())
        self.apply_theme(self.current_theme)

    # ============================================================
    # VOLUME (PYCAW)
    # ============================================================

    def set_volume(self, v):
        vol = float(v)
        for s in AudioUtilities.GetAllSessions():
            if s.Process and s.Process.name() == "python.exe":
                s._ctl.QueryInterface(ISimpleAudioVolume).SetMasterVolume(vol, None)

    def on_volume_press(self, event):
        self.volume_glow_active = True
        if self.volume_slider:
            self.volume_slider.configure(progress_color="#3fa7e5", button_color="#3fa7e5")

    def on_volume_release(self, event):
        self.volume_glow_active = False
        if self.volume_slider:
            self.volume_slider.configure(progress_color="#1f6aa5", button_color="#1f6aa5")

    # ============================================================
    # SEARCH / VIEW / SORT
    # ============================================================

    def change_view(self, value):
        self.view_mode = value
        self.refresh_playlist()

    def change_sort(self, value):
        self.sort_mode = value
        self.refresh_playlist()

    def on_search_change(self, *_):
        self.refresh_playlist()

    # ============================================================
    # ALBUM ART
    # ============================================================

    def extract_album_art(self, path):
        try:
            audio = MutagenFile(path)
            if not audio or not audio.tags:
                return None
            for tag in audio.tags.values():
                if hasattr(tag, "data"):
                    data = tag.data
                    return Image.open(BytesIO(data)).resize((300, 300))
        except:
            return None
        return None

    def update_image(self, path=None):
        if path and os.path.exists(path):
            img = self.extract_album_art(path)
            if img is None:
                img = Image.new("RGB", (300, 300), "gray")
        else:
            img = Image.new("RGB", (300, 300), "gray")
        img_tk = ImageTk.PhotoImage(img)
        self.cover.configure(image=img_tk)
        self.cover.image = img_tk

    # ============================================================
    # FAVORITES
    # ============================================================

    def update_favorite_button(self):
        if not self.song_list or self.current_song is None:
            self.favorite_btn.configure(text="♡")
            return
        path = self.song_list[self.current_song]
        favs = self.db.get_favorites()
        self.favorite_btn.configure(text="❤️" if path in favs else "♡")

    def favorite_pop(self):
        if self.favorite_animating or not self.favorite_btn:
            return
        self.favorite_animating = True
        self.favorite_btn.configure(font=("Arial", 20))

        def shrink():
            self.favorite_btn.configure(font=("Arial", 16))
            self.favorite_animating = False

        self.app.after(130, shrink)

    def toggle_favorite(self):
        if not self.song_list or self.current_song is None:
            return
        path = self.song_list[self.current_song]
        favs = self.db.get_favorites()
        if path in favs:
            self.db.remove_favorite(path)
        else:
            self.db.add_favorite(path)
        self.update_favorite_button()
        self.favorite_pop()
        self.refresh_playlist()

    # ============================================================
    # PLAYBACK + PROGRESS + SEEK
    # ============================================================

    def format_time(self, sec):
        sec = int(sec)
        return f"{sec//60:02d}:{sec%60:02d}"

    def play(self, i):
        if 0 <= i < len(self.song_list):
            self.current_song = i
            path = self.song_list[i]
    
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
    
            try:
                self.song_duration = MP3(path).info.length
            except:
                self.song_duration = 0.0
    
            # ⭐ IMPORTANT: reset manual timer tracking
            self.seek_offset = 0
            self.last_seek_time = pygame.time.get_ticks() / 1000.0
    
            self.db.increment_play_count(path)
            self.update_image(path)
            self.update_favorite_button()
            self.refresh_playlist()
    
            # Reset slider + time
            self.progress.set(0)
            self.time_label.configure(
                text=f"00:00 / {self.format_time(self.song_duration)}"
            )
    
            self.update_progress()
            self.start_progress_pulse()

    def next(self):
        if self.song_list:
            self.play((self.current_song + 1) % len(self.song_list))

    def prev(self):
        if self.song_list:
            self.play((self.current_song - 1) % len(self.song_list))

    def pause(self):
        pygame.mixer.music.pause()
        self.stop_progress_pulse()

    def resume(self):
        pygame.mixer.music.unpause()
        self.start_progress_pulse()
        self.update_progress()

    def stop(self):
        pygame.mixer.music.stop()
        self.stop_progress_pulse()
        self.progress.set(0)
        self.time_label.configure(
            text=f"00:00 / {self.format_time(self.song_duration)}"
        )

    def update_progress(self):
        if self.dragging:
            return
    
        if pygame.mixer.music.get_busy():
            # Time since last seek
            now = pygame.time.get_ticks() / 1000.0
            pos = self.seek_offset + (now - self.last_seek_time)
    
            # Clamp
            if pos < 0:
                pos = 0
            if pos > self.song_duration:
                pos = self.song_duration
    
            # Update slider
            if self.song_duration > 0:
                percent = (pos / self.song_duration) * 100
                self.progress.set(percent)
    
            # Update timer
            self.time_label.configure(
                text=f"{self.format_time(pos)} / {self.format_time(self.song_duration)}"
            )
    
            self.app.after(200, self.update_progress)

    def seek(self, v):
        if self.song_duration > 0:
            new_pos = (float(v) / 100.0) * self.song_duration
    
            # Restart playback at new position
            pygame.mixer.music.play(start=new_pos)
    
            # Track offset manually
            self.seek_offset = new_pos
            self.last_seek_time = pygame.time.get_ticks() / 1000.0
    
            self.dragging = False
            self.update_progress()

    def start_seek(self, e):
        self.dragging = True

    # ============================================================
    # PROGRESS PULSE (SIMPLE)
    # ============================================================

    def start_progress_pulse(self):
        if self.progress_pulse_on:
            return
        self.progress_pulse_on = True
        self.progress_pulse_state = 0
        self._do_progress_pulse()

    def _do_progress_pulse(self):
        if not self.progress_pulse_on or not self.progress:
            return
        if pygame.mixer.music.get_busy():
            if self.progress_pulse_state == 0:
                self.progress.configure(progress_color="#1f6aa5")
                self.progress_pulse_state = 1
            else:
                self.progress.configure(progress_color="#3f88d1")
                self.progress_pulse_state = 0
            self.app.after(300, self._do_progress_pulse)
        else:
            self.progress.configure(progress_color="#1f6aa5")
            self.progress_pulse_on = False

    def stop_progress_pulse(self):
        self.progress_pulse_on = False
        if self.progress:
            self.progress.configure(progress_color="#1f6aa5")

    # ============================================================
    # LOAD SONGS
    # ============================================================

    def load_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio", "*.mp3 *.wav")])
        if files:
            for f in files:
                if f not in self.song_list:
                    self.song_list.append(f)
                    self.db.add_song(f)
            self.refresh_playlist()
            self.play(0)

    def load_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            for fname in os.listdir(folder):
                if fname.lower().endswith((".mp3", ".wav")):
                    path = os.path.join(folder, fname)
                    if path not in self.song_list:
                        self.song_list.append(path)
                        self.db.add_song(path)
            self.refresh_playlist()
            if self.song_list:
                self.play(0)

    # ============================================================
    # PLAYLIST CLICK
    # ============================================================

    def on_playlist_click(self, event):
        index = self.playlist.index(f"@{event.x},{event.y}")
        line = int(index.split(".")[0]) - 1
        if 0 <= line < len(self.display_list):
            path = self.display_list[line]
            if path in self.song_list:
                self.play(self.song_list.index(path))

    # ============================================================
    # DELETE SONG
    # ============================================================

    def delete_song(self):
        if self.current_song is None:
            return
        path = self.song_list[self.current_song]
        self.db.delete_song(path)
        self.song_list.remove(path)
        self.current_song = None
        pygame.mixer.music.stop()
        self.cover.configure(image=None)
        self.cover.image = None
        self.refresh_playlist()

    # ============================================================
    # BUILD UI
    # ============================================================

    def build_ui(self):
        # ---------- LEFT PANEL ----------
        left = CTkFrame(self.app, corner_radius=15)
        left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=3)
        left.grid_rowconfigure(2, weight=1)
        self.frames.append(left)

        title = CTkLabel(left, text="Now Playing", font=("Arial", 26, "bold"))
        title.grid(row=0, column=0, pady=(10, 0))
        self.labels.append(title)

        self.cover = CTkLabel(left, text="")
        self.cover.grid(row=1, column=0, pady=20)
        self.labels.append(self.cover)

        controls = CTkFrame(left, corner_radius=15)
        controls.grid(row=2, column=0, pady=10)
        self.frames.append(controls)

        cfg = {"width": 110, "height": 45, "corner_radius": 12}
        btns = [
            ("⏮ Prev", self.prev),
            ("⏸ Pause", self.pause),
            ("▶ Resume", self.resume),
            ("⏹ Stop", self.stop),
            ("⏭ Next", self.next),
        ]

        for t, cmd in btns:
            b = CTkButton(controls, text=t, command=cmd, **cfg)
            b.pack(side="left", padx=8, pady=10)
            self.buttons.append(b)

        self.favorite_btn = CTkButton(
            controls, text="♡", width=60, command=self.toggle_favorite, font=("Arial", 16)
        )
        self.favorite_btn.pack(side="left", padx=8, pady=10)
        self.buttons.append(self.favorite_btn)

        del_btn = CTkButton(
            controls, text="🗑 Delete", width=80, command=self.delete_song
        )
        del_btn.pack(side="left", padx=8, pady=10)
        self.buttons.append(del_btn)

        vol_label = CTkLabel(left, text="Volume", font=("Arial", 16))
        vol_label.grid(row=3, column=0, pady=(10, 0))
        self.labels.append(vol_label)

        self.volume_slider = CTkSlider(
            left,
            from_=0,
            to=1,
            width=320,
            command=lambda v: self.set_volume(v),
        )
        self.volume_slider.set(0.5)
        self.volume_slider.configure(progress_color="#1f6aa5", button_color="#1f6aa5")
        self.volume_slider.grid(row=4, column=0, pady=10)
        self.volume_slider.bind("<Button-1>", self.on_volume_press)
        self.volume_slider.bind("<ButtonRelease-1>", self.on_volume_release)
        self.sliders.append(self.volume_slider)

        # ---------- PROGRESS ----------
        pb_label = CTkLabel(self.app, text="Playback", font=("Arial", 16))
        pb_label.grid(row=1, column=0, sticky="w", padx=24)
        self.labels.append(pb_label)

        self.progress = CTkSlider(self.app, from_=0, to=100, command=self.seek)
        self.progress.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(30, 5)
        )
        self.progress.bind("<Button-1>", self.start_seek)
        self.progress.configure(progress_color="#1f6aa5")
        self.sliders.append(self.progress)

        self.time_label = CTkLabel(self.app, text="00:00 / 00:00", font=("Arial", 14))
        self.time_label.grid(row=1, column=0, columnspan=2, sticky="e", padx=24, pady=(0, 10))
        self.labels.append(self.time_label)

        # ---------- RIGHT PANEL ----------
        right = CTkFrame(self.app, corner_radius=15)
        right.grid(row=0, column=1, sticky="ns", padx=20, pady=20)
        self.frames.append(right)

        search_entry = CTkEntry(
            right, placeholder_text="Search...", textvariable=self.search_var, width=220
        )
        search_entry.pack(pady=(10, 5), padx=10)
        self.search_var.trace_add("write", self.on_search_change)

        pl_label = CTkLabel(right, text="Playlist", font=("Arial", 22, "bold"))
        pl_label.pack(pady=(5, 5))
        self.labels.append(pl_label)

        self.playlist = CTkTextbox(right, width=260, height=380, corner_radius=10)
        self.playlist.pack(pady=10, padx=10)
        self.playlist.bind("<Button-1>", self.on_playlist_click)
        self.textboxes.append(self.playlist)

        load_btn = CTkButton(
            right, text="🎵 Load Songs", command=self.load_songs, width=200, corner_radius=12
        )
        load_btn.pack(pady=5)
        self.buttons.append(load_btn)

        folder_btn = CTkButton(
            right, text="📁 Load Folder", command=self.load_folder, width=200, corner_radius=12
        )
        folder_btn.pack(pady=5)
        self.buttons.append(folder_btn)

        # ---------- BOTTOM BAR ----------
        theme_files = [f for f in os.listdir(self.theme_path) if f.endswith(".json")]

        bottom = CTkFrame(self.app, corner_radius=15)
        bottom.grid(row=2, column=0, columnspan=2, pady=10)
        self.frames.append(bottom)

        v_lbl = CTkLabel(bottom, text="View:", font=("Arial", 16))
        v_lbl.pack(side="left", padx=(10, 5))
        self.labels.append(v_lbl)

        view_box = CTkComboBox(
            bottom,
            values=["All", "Favorites"],
            width=140,
            command=self.change_view,
        )
        view_box.set("All")
        view_box.pack(side="left", padx=5)
        self.combos.append(view_box)

        s_lbl = CTkLabel(bottom, text="Sort:", font=("Arial", 16))
        s_lbl.pack(side="left", padx=(20, 5))
        self.labels.append(s_lbl)

        sort_box = CTkComboBox(
            bottom,
            values=["A-Z", "Z-A", "Most Played", "Recently Added"],
            width=180,
            command=self.change_sort,
        )
        sort_box.set("A-Z")
        sort_box.pack(side="left", padx=5)
        self.combos.append(sort_box)

        t_lbl = CTkLabel(bottom, text="Theme:", font=("Arial", 16))
        t_lbl.pack(side="left", padx=(20, 5))
        self.labels.append(t_lbl)

        theme_box = CTkComboBox(
            bottom,
            values=theme_files,
            width=200,
            command=self.change_theme,
        )
        theme_box.set(self.default_theme)
        theme_box.pack(side="left", padx=5)
        self.combos.append(theme_box)

        m_lbl = CTkLabel(bottom, text="Mode:", font=("Arial", 16))
        m_lbl.pack(side="left", padx=(20, 5))
        self.labels.append(m_lbl)

        mode_box = CTkComboBox(
            bottom,
            values=["Light", "Dark"],
            width=120,
            command=self.change_mode,
        )
        mode_box.set("Light")
        mode_box.pack(side="left", padx=5)
        self.combos.append(mode_box)

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):
        self.db.close()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.app.destroy()


if __name__ == "__main__":
    MusicPlayer()