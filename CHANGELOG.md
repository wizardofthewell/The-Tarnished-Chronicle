# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-21

### Added
- Pure Python save file parser (no longer requires external Rust CLI tool)
- Unicode-based icon system for better compatibility
- Death count tracking from save files
- Improved playtime reading from profile summary

### Changed
- Complete rewrite of save file parsing logic
- Updated UI icons to use Unicode fallbacks
- Simplified installation process

### Fixed
- "Rust CLI tool not found" error - now uses pure Python implementation
- Boss tracking accuracy (141/207 bosses now correctly detected)
- Character slot detection and offset calculations
- Playtime display showing correct values

### Removed
- Dependency on external Rust CLI binary
- Auto-update feature (temporarily disabled for fork stability)

## [1.x.x] - Previous Releases

See the [original repository](https://github.com/RysanekDavid/The-Tarnished-Chronicle) for earlier version history.
