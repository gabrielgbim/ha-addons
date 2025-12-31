# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-12-30

### Added
- Initial release of Nest Video Downloader add-on
- Google authentication using master token via glocaltokens
- Automatic video download from Nest cameras
- Organized folder structure by camera name, year, month, and day
- Configurable refresh interval for checking new videos
- Timezone support for proper file organization
- Smart duplicate detection - skips already downloaded videos
- Detailed logging of sync operations
- Support for amd64 and aarch64 architectures
- Video files include duration in filename for easy identification

### Features
- Discovers all Nest cameras automatically
- Downloads videos from the last ~4 hours
- Creates structured directory hierarchy for easy browsing
- Minimal resource usage with configurable sync intervals
