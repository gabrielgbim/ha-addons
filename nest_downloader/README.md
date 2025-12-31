# Nest Video Downloader

This Home Assistant add-on automatically downloads video recordings from your Nest cameras using Google authentication.

## Features

- Automatic video download from Nest cameras
- Organizes videos by device name, year, month, and day
- Configurable refresh interval
- Skips already downloaded videos
- Works with Nest cameras using Google authentication via master token
- Support for multiple architectures (amd64, aarch64)

## Configuration

The add-on requires the following configuration:

- `GOOGLE_USERNAME`: Your Google account email
- `GOOGLE_MASTER_TOKEN`: Your Google master token (see instructions below)
- `BASE_PATH`: The path where videos will be saved (default: `/media`)
- `LOCAL_TIMEZONE`: Timezone for file organization (default: `America/New_York`)
- `REFRESH_INTERVAL`: Minutes between sync checks (default: `10`)

## Getting Your Google Master Token

To obtain your Google master token, use the [glocaltokens](https://github.com/leikoilar/glocaltokens) tool:

```bash
pip install glocaltokens
python -m glocaltokens get-master-token
```

Follow the prompts to authenticate and retrieve your master token.

## Installation

1. Add this repository to your Home Assistant instance
2. Install the "Nest Video Downloader" add-on
3. Configure your Google credentials and master token
4. Start the add-on

## Video Organization

Videos are organized in the following structure:
```
/media/
  └── [Camera Name]/
      └── [Year]/
          └── [Month]/
              └── [Day]/
                  └── YYYY-MM-DD_HH-MM-SS_[duration].mp4
```

## Credits

This add-on was developed based on the excellent work of:

- [NestVideoBackup](https://github.com/KaitoKid/NestVideoBackup) by KaitoKid
- [google-nest-telegram-sync](https://github.com/TamirMa/google-nest-telegram-sync) by TamirMa
- [Google Nest Camera Internal API](https://medium.com/@tamirmayer/google-nest-camera-internal-api-fdf9dc3ce167) article by Tamir Mayer

Special thanks to these developers for documenting the Nest API and providing reference implementations.

## Support

For issues and feature requests, please use the [GitHub repository](https://github.com/gabrielgbim/ha-addons).
