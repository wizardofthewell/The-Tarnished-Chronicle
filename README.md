# The Tarnished's Chronicle

**Boss tracking companion for Elden Ring**

[![License](https://img.shields.io/github/license/WizardOfTheWell/The-Tarnished-Chronicle?style=for-the-badge)](LICENSE)

---

## About

**The Tarnished's Chronicle** is a desktop application for Windows that tracks your boss completion progress in Elden Ring. It monitors your save file in real-time and provides a clean interface to see which bosses you've defeated.

This is a fork of the original project by [RysanekDavid](https://github.com/RysanekDavid/The-Tarnished-Chronicle), with significant bug fixes and improvements including:

- **Pure Python save file parsing** - No longer requires the external Rust CLI tool
- **Fixed boss tracking** - Correct event flag offsets for accurate boss status detection  
- **Working UI icons** - Unicode-based fallbacks eliminate missing asset errors
- **Cleaner codebase** - Removed debug files and test cruft

### Key Features

- **Real-time Boss Tracking** - Automatically detects defeated bosses by monitoring your save file
- **Location-based Organization** - Bosses organized by game areas with progression indicators
- **Comprehensive Coverage** - Includes both base game and Shadow of the Erdtree DLC bosses
- **Detailed Statistics** - Track playtime and completion percentages
- **Live Overlay** - In-game overlay showing your current progress
- **OBS Integration** - Export stats to text files for streaming setups
- **Seamless Coop Support** - Compatible with both Vanilla (.sl2) and Seamless Coop Mod (.co2) save files

---

## Installation

### Option 1: Download Release (Recommended)

1. Go to the [Releases](https://github.com/WizardOfTheWell/The-Tarnished-Chronicle/releases) page
2. Download `ER_Boss_Checklist_Setup.exe` from the latest release
3. Run the installer and follow the prompts
4. Launch from the Start Menu or Desktop shortcut

### Option 2: Build from Source

**Requirements:**
- Python 3.10 or higher
- Git

**Steps:**

1. Clone the repository
   ```bash
   git clone https://github.com/WizardOfTheWell/The-Tarnished-Chronicle.git
   cd The-Tarnished-Chronicle
   ```

2. Create virtual environment and install dependencies
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python -m src.main
   ```

**Building the Installer:**

To create a distributable installer:

```bash
# Install build tools
pip install pyinstaller

# Build executable
pyinstaller --clean build.spec

# Create installer (requires NSIS - https://nsis.sourceforge.io/)
makensis installer.nsi
```

The installer will be created as `ER_Boss_Checklist_Setup.exe`.

---

## First Setup

1. **Select Save File** - Browse to your Elden Ring save file:
   - Vanilla Elden Ring: `%APPDATA%\EldenRing\[Steam_ID]\ER0000.sl2`
   - Seamless Coop Mod: `%APPDATA%\EldenRing\[Steam_ID]\ER0000.co2`
2. **Choose Character** - Select which character slot you want to track
3. **Start Playing** - The app will automatically monitor your progress

---

## Features

### Boss Tracking

- Automatic detection of defeated bosses by monitoring your save file
- Bosses grouped by game region
- Completion percentage per area

### Live Overlay

- Customizable display with show/hide options
- Color and font size customization
- Always-on-top mode for visibility while gaming

### OBS Integration

- Exports stats to text files for OBS text sources
- Customizable text formats
- Real-time updates as you play

---

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.10+ (for running from source)
- **Dependencies**: PySide6, psutil, thefuzz, requests, packaging

---

## Known Issues

- Death counter may show incorrect values (save format research ongoing)
- Some sidebar icons display as Unicode symbols (cosmetic only)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Credits

- **Original Author**: [RysanekDavid](https://github.com/RysanekDavid) (Davosso)
- **Fork Maintainer**: [WizardOfTheWell](https://github.com/WizardOfTheWell)
- **FromSoftware** - For creating Elden Ring
