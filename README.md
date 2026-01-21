# 🏰 The Tarnished's Chronicle

<div align="center">

**The ultimate boss tracking companion for Elden Ring**

[![License](https://img.shields.io/github/license/WizardOfTheWell/The-Tarnished-Chronicle?style=for-the-badge)](LICENSE)

</div>

---

## 📖 About

**The Tarnished's Chronicle** is a desktop application for Windows that tracks your boss completion progress in Elden Ring. It monitors your save file in real-time and provides a clean interface to see which bosses you've defeated.

This is a fork of the original project by [RysanekDavid](https://github.com/RysanekDavid/The-Tarnished-Chronicle), with significant bug fixes and improvements including:

- **Pure Python save file parsing** - No longer requires the external Rust CLI tool
- **Fixed boss tracking** - Correct event flag offsets for accurate boss status detection  
- **Working UI icons** - Unicode-based fallbacks eliminate missing asset errors
- **Cleaner codebase** - Removed debug files and test cruft

### ✨ Key Features

- **🎯 Real-time Boss Tracking** - Automatically detects defeated bosses by monitoring your save file
- **📍 Location-based Organization** - Bosses organized by game areas with progression indicators
- **⚔️ Comprehensive Coverage** - Includes both base game and Shadow of the Erdtree DLC bosses
- **📊 Detailed Statistics** - Track playtime and completion percentages
- **🎮 Live Overlay** - In-game overlay showing your current progress
- **📹 OBS Integration** - Export stats to text files for streaming setups
- **🔗 Seamless Coop Support** - Compatible with both Vanilla (.sl2) and Seamless Coop Mod (.co2) save files

---

## 🚀 Quick Start

### Running from Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/WizardOfTheWell/The-Tarnished-Chronicle.git
   cd The-Tarnished-Chronicle
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python -m src.main
   ```

### First Setup

1. **Select Save File** - Browse to your Elden Ring save file:
   - **Vanilla Elden Ring**: `%APPDATA%\EldenRing\[Steam_ID]\ER0000.sl2`
   - **Seamless Coop Mod**: `%APPDATA%\EldenRing\[Steam_ID]\ER0000.co2`
2. **Choose Character** - Select which character slot you want to track
3. **Start Playing** - The app will automatically monitor your progress!

---

## 📋 Features

### 🎯 Boss Tracking

- **Automatic Detection**: Monitors your save file for newly defeated bosses
- **Organized by Location**: Bosses grouped by game region
- **Progress Indicators**: See completion percentage per area

### 🎮 Live Overlay

- **Customizable Display**: Show/hide different stats
- **Color Customization**: Choose your preferred text color
- **Font Size Options**: Adjust overlay text size
- **Always on Top**: Overlay stays visible while gaming

### 📹 OBS Integration

- **Text File Export**: Exports stats to `.txt` files for OBS text sources
- **Customizable Formats**: Define your own text formats for each stat
- **Real-time Updates**: Files update automatically as you play

---

## 💻 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.10+ (for running from source)
- **Dependencies**: PySide6, psutil, thefuzz, requests, packaging

---

## 🐛 Known Issues

- Death counter reads as 0 (death offset location TBD)
- Some sidebar icons display as Unicode symbols (cosmetic only)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Credits

- **Original Author**: [RysanekDavid](https://github.com/RysanekDavid) (Davosso)
- **Fork Maintainer**: [WizardOfTheWell](https://github.com/WizardOfTheWell)
- **FromSoftware** - For creating Elden Ring

---

<div align="center">

**Made with ❤️ for the Elden Ring community**

</div>
