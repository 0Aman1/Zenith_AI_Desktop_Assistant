# Command Reference Guide

This document provides a comprehensive list of available commands and their variations. Each command is categorized by its function and includes confidence scoring information.

## Video Control Commands

### Basic Playback
- **Play/Pause**: 
  - "play video" | "pause video" | "resume video" | "stop video"
  - Confidence: 0.95 (direct match)

### Navigation
- **Next/Previous**:
  - "next video" | "previous video" | "skip video" | "go back"
  - Confidence: 0.95 (direct match)

### Time Control
- **Seeking**:
  - "forward 10 seconds" | "backward 10 seconds"
  - "skip to [time]" | "jump to [minutes:seconds]"
  - Confidence: 0.9 (pattern match)

### YouTube Specific
- **Search and Play**:
  - "play [song/video name] on youtube"
  - "search for [query] on youtube"
  - "play first/second/third video"
  - Confidence: 0.9 (pattern match)

### Playback Controls
- **Speed**:
  - "increase/decrease playback speed"
  - "set playback speed to [0.25-2]x"
  - Confidence: 0.85 (pattern match)

## System Control Commands

### Application Control
- **Launch Applications**:
  - "open [application name]"
  - "launch [application name]"
  - "start [application name]"
  - Confidence: 0.9 (pattern match)

### Window Management
- **Window Controls**:
  - "minimize window"
  - "maximize window"
  - "restore window"
  - "close window"
  - Confidence: 0.9 (pattern match)

### System Operations
- **Power Controls**:
  - "shutdown computer" (requires confirmation)
  - "restart system" (requires confirmation)
  - "lock computer"
  - "log off"
  - Confidence: 0.95 (direct match)

## Media Control Commands

### Volume Control
- **Basic Controls**:
  - "increase/decrease volume"
  - "volume up/down"
  - "mute/unmute"
  - Confidence: 0.9 (pattern match)

### Specific Adjustments
- **Volume Levels**:
  - "set volume to [0-100] percent"
  - "volume [0-100]"
  - Confidence: 0.9 (pattern match)

### Brightness Control
- **Basic Controls**:
  - "increase/decrease brightness"
  - "brightness up/down"
  - Confidence: 0.9 (pattern match)

### Specific Adjustments
- **Brightness Levels**:
  - "set brightness to [0-100] percent"
  - "brightness [0-100]"
  - Confidence: 0.9 (pattern match)

## Information Commands

### System Information
- **Hardware Status**:
  - "show CPU usage"
  - "show memory usage"
  - "show disk space"
  - "battery status"
  - "wifi status"
  - Confidence: 0.9 (pattern match)

### Time and Date
- **Current Time**:
  - "what's the time"
  - "current time"
  - Confidence: 0.95 (direct match)
- **Current Date**:
  - "what's the date"
  - "current date"
  - Confidence: 0.95 (direct match)

## Web Integration Commands

### Web Search
- **General Search**:
  - "search for [query]"
  - "google [query]"
  - "look up [query]"
  - Confidence: 0.85 (pattern match)

### News and Weather
- **News**:
  - "show news"
  - "get latest headlines"
  - Confidence: 0.9 (pattern match)
- **Weather**:
  - "weather forecast"
  - "weather in [location]"
  - Confidence: 0.9 (pattern match)

## Screenshot Commands
- **Take Screenshot**:
  - "take screenshot"
  - "capture screen"
  - "screenshot"
  - Confidence: 0.95 (direct match)

## Command Variations and Context

### Follow-up Commands
- "a bit more" (after volume/brightness command)
- "little less" (after volume/brightness command)
- "again" or "repeat"
- Confidence: 0.85 (contextual match)

### Compound Commands
- "open chrome and play music"
- "decrease volume and pause video"
- Confidence: 0.8 (compound match)

## Confidence Scoring

Confidence scores indicate how certain the system is about understanding your command:
- 0.95-1.00: Direct match, highest confidence
- 0.85-0.94: Pattern match, high confidence
- 0.70-0.84: Contextual or compound match
- 0.50-0.69: ML-based prediction
- < 0.50: Low confidence, may need clarification

## Tips for Best Results

1. **Clear Speech**: Speak clearly and at a moderate pace
2. **Key Commands**: Use key phrases like "open", "play", "show" at the start
3. **Specific Terms**: Be specific with application names and actions
4. **Watch Confidence**: If confidence is low, try rephrasing
5. **Context Awareness**: Previous commands provide context for follow-ups 