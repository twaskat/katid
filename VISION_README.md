# 🔍 Vision Agent - AI Image Analyzer

A beautiful Gradio-based vision agent with a dark purple theme that analyzes and identifies content in images using Fireworks AI vision models.

## ✨ Features

- 🔥 **Fireworks AI Vision Integration** - Advanced image analysis using state-of-the-art vision models
- 🎨 **Same Beautiful Design** - Matching dark purple theme with Story Forge
- 📊 **Multiple Analysis Types** - Choose from 6 different analysis modes
- 🔍 **Smart Image Recognition** - Identify objects, scenes, text, emotions, and more
- 🔑 **Secure API Key Input** - Password-protected input for your API key
- 🤖 **Custom Model Selection** - Use any Fireworks vision model
- 🚀 **Auto Port Detection** - Automatically finds an available port
- 📱 **Termux Optimized** - Works perfectly on Android devices

## 📋 Prerequisites

Before running Vision Agent in Termux, you need to install Python and required packages:

```bash
# Update Termux packages
pkg update && pkg upgrade

# Install Python and pip
pkg install python

# Install required Python packages
pip install gradio requests
```

## 🚀 Running the App

### Quick Start
```bash
# Use the setup script
bash vision_setup.sh
```

### Manual Start
```bash
# Run the app directly
python vision_agent.py
```

### Access the App
The app will automatically:
- Find an available port (starting from 7861)
- Display the port number in the terminal
- Launch the web interface

Access it at: `http://localhost:PORT` (displayed in terminal)

## 📖 How to Use

1. **Enter API Key**: Paste your Fireworks API key in the secure input box
2. **Select Model**: Choose or enter a Fireworks vision model (default: llava-v1.5-7b-instruct)
3. **Choose Analysis Type**: Select what type of analysis you want
4. **Upload Image**: Click to upload an image from your device
5. **Analyze**: Click the "🔍 Analyze Image 🔍" button
6. **View Results**: Read the detailed analysis of your image

## 🔬 Analysis Types

### 📝 General Description
Provides a comprehensive description of the image including subjects, setting, colors, mood, and notable details.

### 🎯 Object Detection
Identifies and lists all objects visible in the image, including their positions and appearances.

### 🌆 Scene Understanding
Analyzes the scene, environment, what's happening, context, setting, and overall composition.

### 📄 Text Recognition (OCR)
Extracts and transcribes any text visible in the image, including its location.

### 😊 Emotion & Mood
Analyzes the emotional content, feelings, atmosphere, and emotional impact conveyed by the image.

### 🔬 Detailed Analysis
Provides an extremely comprehensive analysis covering all elements: objects, people, colors, lighting, composition, mood, and context.

## 🤖 Recommended Fireworks Vision Models

- `accounts/fireworks/models/llava-v1.5-7b-instruct` - Balanced vision model (default)
- `accounts/fireworks/models/llava-v1.6-34b-instruct` - Higher quality, more detailed
- `accounts/fireworks/models/nvlm-d-72b-instruct` - Best for complex scenes

## 🎯 Use Cases

- **Accessibility**: Describe images for visually impaired users
- **Content Analysis**: Understand what's in images
- **Text Extraction**: Get text from images (OCR)
- **Object Identification**: Find and list objects in photos
- **Scene Analysis**: Understand environments and contexts
- **Emotion Detection**: Analyze emotional content
- **Research**: Extract detailed information from visual data

## 📱 Termux Tips

### Increase Storage (if needed)
```bash
termux-setup-storage
```

### Keep App Running in Background
```bash
# Run in background
python vision_agent.py &

# Or use tmux for better session management
pkg install tmux
tmux new -s vision
python vision_agent.py
# Press Ctrl+B then D to detach session
# tmux attach -t vision to reattach
```

## 🖼️ Supported Image Formats

- JPEG/JPG
- PNG
- WebP
- GIF
- BMP
- TIFF

## ⚙️ Customization

You can customize the app by editing `vision_agent.py`:

- **Change theme colors**: Edit the `custom_css` variable
- **Add more analysis types**: Update the `analysis_type` dropdown and `analysis_prompts` dictionary
- **Modify analysis detail**: Adjust `max_tokens` in the payload
- **Change temperature**: Modify `temperature` parameter (0.7 is recommended for vision tasks)

## 🔧 Troubleshooting

**"Module not found" error?**
```bash
pip install gradio requests --upgrade
```

**API errors?**
- Verify your API key is correct
- Check your Fireworks account has available credits
- Ensure you're using a vision-capable model
- Check your internet connection

**Image not processing?**
- Try a different image format (PNG/JPEG recommended)
- Reduce image size if very large
- Check the image isn't corrupted

**Port already in use?**
The app automatically searches for available ports, so this shouldn't be an issue.

## 📄 License

This project is open source and available for personal and educational use.

## 💡 Tips for Best Results

- Use high-quality, clear images
- Good lighting improves analysis accuracy
- Larger images provide more detail
- Try different analysis types for comprehensive understanding
- Use "Detailed Analysis" for complete information

## 🎨 Design Features

- Matching theme with Story Forge for consistency
- Smooth animations and transitions
- Responsive design for mobile devices
- Intuitive user interface
- Beautiful dark purple gradient background

---

Made with 💜 using Gradio and Fireworks AI Vision