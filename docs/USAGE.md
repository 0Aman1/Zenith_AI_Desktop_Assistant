# AI Desktop Assistant Usage Guide

This document provides detailed information on how to use the AI Desktop Assistant effectively.

## Starting the Assistant

1. Open a terminal or command prompt
2. Navigate to the project directory
3. Run the assistant using:
   ```
   python run.py
   ```
4. The assistant will say "Ready" when it's listening for commands

## Command Usage

### System Control Commands

#### Application Management
- **Open applications**: "open chrome", "launch notepad", "start calculator"
- **Find applications**: If an application isn't found, the assistant will offer to search for it online

#### Window Management
- **Minimize**: "minimize window", "minimize current window"
- **Maximize**: "maximize window", "maximize current window" 
- **Restore**: "restore window", "normal window"
- **Close**: "close window", "close current window"

#### System Operations
- **Shutdown**: "shutdown computer", "power off", "turn off computer"
- **Restart**: "restart computer", "reboot system"
- **Log off**: "log off", "sign out"
- **Lock**: "lock computer", "lock pc", "lock system"

### System Information

- **General info**: "system information", "system info"
- **Specific metrics**:
  - "cpu usage", "processor usage"
  - "memory usage", "ram usage"
  - "disk usage", "disk space"
- **Battery**: "battery status", "battery level", "battery info"
- **Network**: "wifi status", "network info", "check wifi"
- **Time/Date**: "what's the time", "what's the date", "time and date"

### Media Controls

#### Volume Control
- **Adjust volume**: "increase volume", "decrease volume", "volume up", "volume down"
- **Set specific volume**: "set volume to 50 percent"
- **Mute/unmute**: "mute volume", "unmute volume"

#### Brightness Control
- **Adjust brightness**: "increase brightness", "decrease brightness", "brightness up", "brightness down"
- **Set specific brightness**: "set brightness to 70 percent"

#### Media Playback
- **Basic controls**: "play", "pause", "stop", "next", "previous"
- **These commands work with any active media player**

### YouTube and Web Integration

#### YouTube
- **Open YouTube**: "open youtube", "launch youtube"
- **Search on YouTube**: "search for cooking tutorials on youtube", "find music videos on youtube"
- **Play specific videos**:
  - "play first video from search results"
  - "play second video"
  - "play third video from search results"

#### Web Search
- **General searches**: "search for latest technology news", "search for recipes"
- **Google searches**: "google artificial intelligence", "google climate change"

### Information Requests

#### Weather
- **Local weather**: "what's the weather"
- **Specific location**: "weather in London", "what's the weather in Tokyo"

#### News
- **Headlines**: "show me the news", "get latest headlines", "news updates"

### Utility Features

#### Screenshots
- **Take screenshot**: "take screenshot", "capture screen", "take a picture of screen"
- Screenshots are saved to the "screenshots" folder with a timestamp

## Command Confidence

Each command will display its category and confidence score in the terminal:

```
Command: check battery | Category: system_info | Confidence: 0.95
```

- **High confidence (>0.7)**: The assistant is very certain about what you want
- **Medium confidence (0.4-0.7)**: The assistant has a reasonable guess
- **Low confidence (<0.4)**: The assistant is uncertain but will try its best

## Exiting the Assistant

- Say "exit", "quit", or "goodbye" to close the assistant

## Troubleshooting

### Speech Recognition Issues
- Speak clearly and at a moderate pace
- Minimize background noise
- Check that your microphone is working properly

### Command Execution Issues
- If a command fails, try rephrasing it
- Check the confidence score - low scores may indicate unclear commands
- Some commands require administrative privileges
- Ensure you have the necessary applications installed for app-specific commands

### System-Specific Issues
- **Windows**: Make sure you have the WMI module installed for brightness control
- **YouTube**: Ensure you have an active internet connection and a default browser
- **Volume/Media**: These commands work best when a media player is already running 