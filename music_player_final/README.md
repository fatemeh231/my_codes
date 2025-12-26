# 🎵 Advanced Python Music Player  
A modern, theme‑able, ML‑powered desktop music player built with **CustomTkinter**, **Pygame**, and **PostgreSQL**.  
Designed for smooth interaction, clean UI, and intelligent music recommendations.

---

## ✨ Features

### 🎧 Core Music Player
- Play / Pause / Next / Previous  
- Seek bar with smooth progress animation  
- Volume slider with glow effect  
- Album art extraction (MP3 embedded images)  
- Real‑time playback time display  

### ❤️ Favorites System
- Mark/unmark songs as favorites  
- Favorites stored in PostgreSQL  
- UI button updates instantly  
- Small “pop” animation for feedback  

### 🤖 Machine Learning Recommendations
- Extracts MFCC embeddings using **Librosa**  
- Clusters songs using **KMeans**  
- Recommends similar songs based on your favorites  
- Interactive popup with play buttons  

### 🎨 Custom Themes & Modes
- Load any `.json` theme dynamically  
- Light/Dark mode switching  
- Theme applies to:
  - Frames  
  - Buttons  
  - Labels  
  - Sliders  
  - Textboxes  
  - ComboBoxes  

### 📁 Playlist & Library Management
- Load individual songs  
- Load entire folders  
- Delete songs  
- Search bar with instant filtering  
- Sort by:
  - A–Z  
  - Z–A  
  - Most Played  
  - Recently Added  

### 🗄 PostgreSQL Database
Stores:
- Song paths  
- Play counts  
- Favorites  
- ML feature embeddings  
- Cluster IDs  

