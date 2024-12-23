# WhatsApp Chat Extractor

A Python-based tool for extracting WhatsApp conversations, media, and databases from Android devices.

## Features

- Extract WhatsApp databases and media files
- Maintain original folder structure
- Generate detailed extraction metadata
- Track media statistics (images, videos, documents)
- Complete logging system
- User-friendly interface with step-by-step guidance
- Support for multimedia content extraction

## Prerequisites

- Python 3.6 or higher
- Android Debug Bridge (ADB)
- USB cable for device connection
- Android device with WhatsApp installed
- USB Debugging enabled on the Android device

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-extractor.git
cd whatsapp-extractor
```

2. Install ADB:

### Windows
- Download [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools)
- Extract to a folder (e.g., C:\adb)
- Add the folder path to system environment variables

### macOS
```bash
brew install android-platform-tools
```

### Linux
```bash
sudo apt-get install android-tools-adb
```

## Device Setup

1. Enable Developer Options:
   - Go to Settings > About Phone
   - Find "Build Number"
   - Tap it 7 times
   - You'll see "You are now a developer" message

2. Enable USB Debugging:
   - Go to Settings > Developer Options
   - Enable "USB Debugging"
   - Connect your device to computer
   - Accept "Allow USB Debugging" prompt on your device

## Usage

1. Run the script:
```bash
python whatsapp_extractor.py
```

2. Follow the on-screen instructions:
   - Connect your Android device
   - Enable USB debugging when prompted
   - Specify backup destination folder
   - Wait for the extraction to complete

## Output Structure

```
WhatsApp_Backup_YYYYMMDD_HHMMSS/
├── Databases/
│   └── [WhatsApp database files]
├── Media/
│   ├── WhatsApp Images/
│   ├── WhatsApp Video/
│   ├── WhatsApp Audio/
│   └── WhatsApp Documents/
└── backup_metadata.json
```

## Metadata Format

The `backup_metadata.json` file contains:
```json
{
    "timestamp_backup": "YYYYMMDD_HHMMSS",
    "chat_folders": [
        {
            "name": "folder_name",
            "file_count": number_of_files
        }
    ],
    "media_stats": {
        "images": number_of_images,
        "videos": number_of_videos,
        "audio": number_of_audio_files,
        "documents": number_of_documents
    }
}
```

## Logging

- Logs are saved in `whatsapp_extraction_YYYYMMDD_HHMMSS.log`
- Contains detailed information about:
  - Extraction process
  - Errors encountered
  - File operations
  - System checks

## Troubleshooting

### ADB not found
```bash
Error: ADB not found in system
Solution: Ensure ADB is installed and added to PATH
```

### No device connected
```bash
Error: No Android device connected
Solution: Check USB connection and debugging status
```

### Backup error
```bash
Error: Backup creation failed
Solution: Check storage space and permissions
```

## Security Notes

- Keep backups secure - they contain sensitive data
- Don't share backup files with untrusted parties
- Consider encrypting backup folders
- Delete backups after use if not needed
- Use only trusted USB cables and computers

## Limitations

- Works only with Android devices
- Requires USB debugging enabled
- May not work with some Android versions
- Large backups may take significant time
- Some content may be inaccessible due to WhatsApp's encryption

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for personal use only. Respect privacy and applicable laws when extracting WhatsApp data. The authors are not responsible for misuse of this tool.

## Support

For support:
1. Check the log file for error details
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Contact the maintainers

## Future Enhancements

- [ ] Selective backup (chat-only or media-only)
- [ ] Date-based filtering
- [ ] Specific chat extraction
- [ ] GUI interface
- [ ] Backup compression
- [ ] Backup encryption
- [ ] Multi-device support
- [ ] Progress bar for large backups
- [ ] Cloud backup support
