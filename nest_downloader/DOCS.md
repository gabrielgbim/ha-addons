# Documentation

## About

The Nest Video Downloader add-on automatically downloads video recordings from your Nest cameras to your Home Assistant instance. It uses Google authentication via master token to access your Nest devices and organizes videos by camera, date, and time.

## How It Works

The add-on:
1. Authenticates with Google using your master token
2. Discovers all Nest cameras on your account
3. Checks for new video events every X minutes (configurable)
4. Downloads videos that haven't been downloaded yet
5. Organizes them in a structured folder hierarchy

## Configuration

### Option: `GOOGLE_USERNAME`

Your Google account email address used with your Nest cameras.

**Required**: Yes  
**Type**: Email

### Option: `GOOGLE_MASTER_TOKEN`

Your Google master token for authentication. This is obtained using the glocaltokens tool.

**Required**: Yes  
**Type**: Password (sensitive)

### Option: `BASE_PATH`

The base directory where downloaded videos will be stored. Videos will be organized within this path by camera name and date.

**Required**: No  
**Default**: `/media`  
**Example**: `/media` will create `/media/Front Door Camera/2024/12/30/...`

### Option: `LOCAL_TIMEZONE`

The timezone used for organizing video files and timestamps. Videos are organized using this timezone for the folder structure.

**Required**: No  
**Default**: `America/New_York`  
**Example**: `America/Los_Angeles`, `Europe/London`, `Asia/Tokyo`

### Option: `REFRESH_INTERVAL`

The number of minutes to wait between checking for new videos.

**Required**: No  
**Default**: `10`  
**Type**: Integer (minutes)
**Recommendation**: Use 10-60 minutes depending on your needs

## Getting Your Google Master Token

You need to obtain a Google master token to authenticate with Nest services.

The easiest way to get your master token is using Docker:

```bash
docker run --rm -it breph/ha-google-home_get-token
```

Follow the interactive prompts:
1. Enter your Google account email
2. Enter your password (or app password)
3. The tool will display your master token

**Tip**: You can generate an app password from [Google App Passwords](https://myaccount.google.com/apppasswords) for added security. Make sure you're using the Google account that has access to your Nest cameras.

**Important**: Keep your master token secure - it provides access to your Google/Nest account.

## Video Organization

Videos are automatically organized in the following structure:

```
/media/
  └── [Camera Name]/
      └── [Year]/
          └── [Month]/
              └── [Day]/
                  └── YYYY-MM-DD_HH-MM-SS_[duration].mp4
```

**Example**:
```
/media/
  └── Front Door Camera/
      └── 2024/
          └── 12/
              └── 30/
                  └── 2024-12-30_14-23-45_30s000ms.mp4
                  └── 2024-12-30_18-45-12_45s250ms.mp4
```

## Usage

1. Configure your Google username and master token in the add-on configuration
2. Set your preferred timezone and refresh interval
3. Start the add-on
4. Monitor the logs to see video discovery and downloads
5. Access your videos through the Home Assistant Media Browser or directly via the file system

## Logs

The add-on provides detailed logging:
- Device discovery
- Number of events found
- Download progress
- Skipped videos (already downloaded)
- Any errors encountered

## Video Retention

The add-on downloads videos from approximately the last 4 hours (3 hours for free Nest Aware + 1 hour buffer). Videos are checked during each refresh interval, and only new videos are downloaded.

## Troubleshooting

### Authentication Issues

If you experience authentication issues:
- Verify your Google username (email) is correct
- Ensure your master token is valid and hasn't expired
- Try regenerating your master token using glocaltokens
- Check the add-on logs for detailed error messages

### No Devices Found

If no Nest cameras are discovered:
- Verify your cameras are properly set up in the Google Home app
- Ensure your account has access to the cameras
- Check that your cameras are Nest-branded devices
- Review the add-on logs for connection errors

### Videos Not Downloading

If videos are not being downloaded:
- Check that the BASE_PATH is accessible and writable
- Verify you have sufficient disk space
- Ensure your cameras have recorded events
- Check the logs for download errors
- Note: Only events from the last ~4 hours are available

### Storage Issues

If you encounter storage problems:
- Monitor your available disk space
- Consider increasing your refresh interval to reduce download frequency
- Set up automated cleanup of old videos if needed

## Performance

- The add-on runs continuously, checking for new videos at your configured interval
- Already downloaded videos are skipped automatically
- CPU and memory usage is minimal when idle
- Network usage depends on the number and size of videos being downloaded

## Support

For additional help, please visit the [GitHub repository](https://github.com/gabrielgbim/ha-addons).
