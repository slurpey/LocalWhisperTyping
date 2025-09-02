# 🧠 Complete Beginner's Guide to LocalWhisperTyping
*A step-by-step guide for absolute beginners. Every step is required. No programming knowledge expected.*

## ✅ What This Tool Does

This tool listens to your voice and types what you say automatically:
- Press `Ctrl + Shift` to start speaking
- When you release the keys, your words are typed automatically
- Works in any application (Word, email, web browsers, etc.)

## 🛑 How to Stop the Tool

You have three ways to stop the tool:
1. Press `Ctrl + Shift + Esc`
2. Right-click the microphone icon in the system tray → Quit
3. Close the black command window that opened when it started
   - ⚠️ **Important**: This window must remain open while using the tool (you may minimize it)

## 📁 What Files You Have

After downloading or cloning this repository, you have these important files:

- **`lloydswhisper.py`** - The main program (don't edit this)
- **`start_voice_typing.bat`** - Easy launcher file (double-click to start)
- **`requirements.txt`** - List of required components
- **`README.md`** - Technical documentation

---

## 🚀 Installation Steps

### 🧱 Step 1: Install Python

1. Go to: https://www.python.org/downloads/windows/
2. Click **Windows installer (64-bit)**
3. When the installer opens:
   - ✅ **CHECK THE BOX**: "Add Python to PATH"
   - Click: **Install Now**
4. Wait until installation is complete
5. Close the installer

### 🖥 Step 2: Open PowerShell as Administrator

1. Click the **Start menu**
2. Type: `powershell`
3. **Right-click** on "Windows PowerShell"
4. Click **"Run as administrator"**
5. A blue window opens with "Administrator:" in the title bar
6. Leave it open - you'll use it in the next step

### 📦 Step 3: Install Required Components

In the blue PowerShell window, copy and paste this **entire command**:

```powershell
pip install --upgrade pip && pip install openai-whisper sounddevice scipy numpy keyboard pystray pillow
```

1. Press **Enter**
2. Wait for it to finish (may take several minutes)
3. ⚠️ **Do not close PowerShell** - you'll use it again

### 📂 Step 4: Download and Place the Files

**Option A: If you downloaded a ZIP file:**
1. Extract the ZIP file to: `C:\Users\[YourName]\Documents\`
2. Rename the extracted folder to: `LocalWhisperTyping`
3. You should now have: `C:\Users\[YourName]\Documents\LocalWhisperTyping\`

**Option B: If you used git clone:**
1. In PowerShell, navigate to your Documents folder:
   ```powershell
   cd $env:USERPROFILE\Documents
   ```
2. Clone the repository:
   ```powershell
   git clone https://github.com/slurpey/LocalWhisperTyping.git
   ```

### 📝 Step 5: Edit the Batch File (If Needed)

**Most users can skip this step** - the included `start_voice_typing.bat` should work automatically.

If you have problems, you may need to edit the batch file:

1. **Right-click** on `start_voice_typing.bat`
2. Choose **"Edit"** or **"Open with > Notepad"**
   - ⚠️ **Do NOT double-click** - that would try to run it
3. If you need to specify exact paths, modify the Python command line

### ▶️ Step 6: Start the Tool

1. **Double-click** `start_voice_typing.bat`
2. A security window will appear asking:
   *"Do you want to allow this app to make changes to your device?"*
3. Click **"Yes"**
   - This permission is needed to:
     - Listen to your microphone
     - Simulate keyboard typing
     - Run in the background
4. A black command window will open and stay open
5. A microphone icon will appear near the clock (system tray)

⚠️ **Important**: 
- Do NOT close the black window
- You may minimize it or resize it
- Closing it will stop the tool completely

---

## 🧪 How to Use the Tool

### Basic Usage
1. **Press and hold** `Ctrl + Shift`
2. **Speak clearly** into your microphone
3. **Release both keys**
4. The tool types what you said automatically

### First Time Setup
- On first use, the tool will download the Whisper model (~150MB)
- This may take a few minutes
- After this, the tool starts much faster

### Tips for Best Results
- **Speak clearly** and at normal pace
- Use a **good quality microphone**
- **Minimize background noise**
- Keep recordings under 30 seconds for best performance

---

## 🔧 Troubleshooting

### "No audio devices found"
- Check that your microphone is plugged in and working
- Go to Windows Settings > Privacy > Microphone
- Make sure apps can access your microphone

### "Python is not recognized"
- You need to reinstall Python
- Make sure to check "Add Python to PATH" during installation

### Keyboard shortcuts don't work
- Try running the batch file as Administrator
- Check if another program is using the same shortcuts
- Right-click the tray icon → "Restart Hooks"

### Tool doesn't start
- Check the log file: `voice_typing.log` in the same folder
- Make sure all Python packages installed correctly
- Try running PowerShell as Administrator again

### Performance Issues
- Close unnecessary programs to free up memory
- Use a wired microphone instead of wireless
- Speak in a quiet environment

---

## 📋 Quick Reference Card

| Action | Keys/Method |
|--------|-------------|
| **Start Recording** | Hold `Ctrl + Shift` |
| **Stop Recording & Type** | Release `Ctrl + Shift` |
| **Exit Tool** | `Ctrl + Shift + Esc` |
| **Restart Hooks** | Right-click tray icon → "Restart Hooks" |
| **View Status** | Right-click tray icon → "Show Status" |
| **View Logs** | Right-click tray icon → "Open Log" |

---

## 🆘 Getting Help

If you're still having trouble:

1. **Check the log file**: `voice_typing.log` in your LocalWhisperTyping folder
2. **Read the technical documentation**: `README.md` in the same folder
3. **Try the manual startup method**: Open PowerShell, navigate to your folder, and run:
   ```powershell
   python lloydswhisper.py
   ```

---

*This guide covers the complete setup process for users with no programming experience. For advanced configuration and technical details, see README.md.*
