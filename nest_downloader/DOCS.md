# Documentation

## About

The Nest Video Downloader add-on enables you to automatically download video recordings from your Nest cameras to your Home Assistant instance.

## Configuration

### Option: `nest_email`

Your Nest account email address. This is required to authenticate with the Nest API.

**Required**: Yes

### Option: `nest_password`

Your Nest account password. This is required to authenticate with the Nest API.

**Required**: Yes

### Option: `download_path`

The path where downloaded videos will be stored. By default, videos are saved to `/share/nest_videos`.

**Required**: No  
**Default**: `/share/nest_videos`

## Usage

1. Configure your Nest account credentials in the add-on configuration
2. Start the add-on
3. Videos will be automatically downloaded to the specified path
4. Access your videos through the Home Assistant file browser or media folder

## Troubleshooting

### Authentication Issues

If you experience authentication issues:
- Verify your Nest account credentials are correct
- Ensure your Nest account has access to the cameras
- Check the add-on logs for detailed error messages

### Storage Issues

If videos are not being saved:
- Verify the download path exists and is writable
- Check available disk space
- Review the add-on logs for permission errors

## Support

For additional help, please visit the [GitHub repository](https://github.com/gabrielgbim/ha-addons).
