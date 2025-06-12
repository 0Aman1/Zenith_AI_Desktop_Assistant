# Test Commands for AI Desktop Assistant

This document provides a list of commands to test all available features in the AI Desktop Assistant. Use these commands to verify that each component is working correctly.

## Speech Recognition Tests

- "What can you do?" (Tests basic speech recognition)
- "Hello" (Tests basic speech recognition)
- "Thank you" (Tests basic speech recognition)

## System Control Commands

### Application Launch
- "Open Chrome"
- "Launch Notepad"
- "Start Calculator"
- "Open File Explorer"

### Window Management
- "Minimize window"
- "Maximize window"
- "Restore window"
- "Close window"
- "Switch window"

### System Operations
- "Lock computer"
- "What's my battery status"
- "Show CPU usage"
- "Show memory usage"
- "Show disk space"
- "Show WiFi status"

## Media Control Tests

### Volume Controls
- "Increase volume"
- "Decrease volume"
- "Volume up" 
- "Volume down"
- "Set volume to 50 percent"
- "Mute sound"
- "Unmute sound"

### Brightness Controls
- "Increase brightness"
- "Decrease brightness"
- "Brightness up"
- "Brightness down"
- "Set brightness to 70 percent"

### Media Playback
- "Play media"
- "Pause media"
- "Stop media"
- "Next track"
- "Previous track"
- "Play music"
- "Play video"

## YouTube Controls

### Search and Play
- "Play Arijit Singh song on YouTube"
- "Search for cooking tutorials on YouTube"
- "Show me documentaries on YouTube"
- "Play first video"
- "Play second video"

### Playback Controls
- "Pause YouTube video"
- "Resume YouTube video"
- "Skip 10 seconds"
- "Go back 10 seconds"
- "Increase playback speed"
- "Decrease playback speed"

## Web Search Commands

### General Search
- "Search for weather forecast"
- "Google latest news"
- "Look up recipe for pasta"
- "Search for Python tutorials"
### Information Queries
- "What's the time"
- "What's today's date"
- "Show news headlines"
- "Weather in Mumbai"
- "Weather forecast"

## Screenshot Commands
- "Take a screenshot"
- "Capture screen"
- "Screenshot"

## Compound Commands
- "Open Chrome and search for Python tutorials"
- "Decrease volume and play music"
- "Increase brightness and open Notepad"

## Command Learning Tests

### Similar Commands
- Use a slightly different phrasing of a previously successful command
- "Make the screen brighter" (after "Increase brightness")
- "Lower the sound" (after "Decrease volume")

### Command Suggestions
- Type in a partial command and see if suggestions appear
- Use an incorrectly spelled command to test fuzzy matching

## Testing Tips

1. **Start with basic commands** to ensure speech recognition is working
2. **Test one category at a time** to isolate any issues
3. **Note the confidence scores** displayed for each command
4. **Try variations** of commands to test the system's flexibility
5. **Test error handling** by intentionally using invalid commands

## Expected Behavior

- Commands with high confidence (>0.8) should execute immediately
- Commands with medium confidence (0.4-0.8) will execute but may show a warning
- Commands with low confidence (<0.4) may prompt for confirmation or default to web search
- The system should adapt to your speech patterns over time

## Troubleshooting

- If commands aren't recognized, check your microphone
- Ensure you're in a quiet environment
- Speak clearly and at a moderate pace
- If the system frequently defaults to web searches, check the error logs for clues 