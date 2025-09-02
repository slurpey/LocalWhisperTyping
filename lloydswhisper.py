import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import keyboard
import tempfile
import os
import time
import ctypes
import logging
import threading
from datetime import datetime
import pystray
from PIL import Image, ImageDraw
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_typing.log'),
        logging.StreamHandler()
    ]
)

# Load Whisper model once (takes ~5–10s)
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Model loaded successfully!")

# Windows API for focus management
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Prevent duplicate triggers and track activity
is_recording = False
last_activity = time.time()
last_hotkey_test = time.time()
hotkey_failures = 0
tray_icon = None
service_active = True

def create_icon():
    """Create a simple microphone icon for the system tray"""
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple microphone shape
    draw.rectangle([24, 10, 40, 35], fill=(70, 130, 180, 255))
    for i in range(15, 32, 3):
        draw.line([27, i, 37, i], fill=(255, 255, 255, 255), width=1)
    draw.rectangle([30, 35, 34, 50], fill=(70, 130, 180, 255))
    draw.rectangle([20, 50, 44, 54], fill=(70, 130, 180, 255))
    
    return image

def check_audio_devices():
    """Check if audio input devices are available"""
    try:
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        if not input_devices:
            logging.warning("No input audio devices found!")
            return False
        return True
    except Exception as e:
        logging.error(f"Error checking audio devices: {e}")
        return False

def record_audio_dynamic(filename, fs=16000):
    """Record until Ctrl+Shift is released."""
    frames = []
    recording_started = False
    
    def callback(indata, frame_count, time_info, status):
        nonlocal recording_started
        if status:
            logging.warning(f"Audio callback status: {status}")
        frames.append(indata.copy())
        recording_started = True
    
    try:
        with sd.InputStream(samplerate=fs, channels=1, dtype='float32', callback=callback):
            start_time = time.time()
            while keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
                sd.sleep(100)
                if time.time() - start_time > 90:
                    logging.warning("Recording timeout reached (90s)")
                    break
        
        if frames and recording_started:
            audio = np.concatenate(frames, axis=0)
            if np.max(np.abs(audio)) > 0.001:
                wav.write(filename, fs, np.int16(audio * 32767))
                logging.info(f"Audio recorded: {len(frames)} frames, {len(audio)/fs:.2f}s")
                return True
            else:
                logging.warning("Only silence detected in recording")
                return False
        else:
            logging.warning("No audio frames captured")
            return False
    except Exception as e:
        logging.error(f"Error during audio recording: {e}")
        return False

def transcribe(filename):
    """Transcribe with Whisper model"""
    try:
        start_time = time.time()
        res = model.transcribe(filename)
        transcription_time = time.time() - start_time
        text = res.get("text", "").strip()
        logging.info(f"Transcription completed in {transcription_time:.2f}s: '{text}'")
        return text
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return ""

def on_hotkey():
    """Hotkey action: record, restore focus, and type into active window"""
    global is_recording, last_activity, hotkey_failures
    
    if is_recording:
        logging.info("Already recording, ignoring hotkey")
        return
    
    is_recording = True
    last_activity = time.time()
    hotkey_failures = 0  # Reset failure counter on successful trigger
    
    try:
        logging.info("Hotkey triggered - starting recording")
        
        if not check_audio_devices():
            logging.error("No audio devices available")
            return
        
        hwnd = user32.GetForegroundWindow()
        if hwnd == 0:
            logging.warning("Could not get foreground window")
        
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        path = tmp.name
        tmp.close()
        
        try:
            if record_audio_dynamic(path):
                text = transcribe(path)
                
                if text:
                    if hwnd != 0:
                        user32.SetForegroundWindow(hwnd)
                        time.sleep(0.2)
                    
                    keyboard.write(text)
                    logging.info(f"Successfully typed: '{text}'")
                else:
                    logging.info("No speech detected in transcription")
            else:
                logging.warning("Recording failed")
                
        finally:
            try:
                os.remove(path)
            except:
                logging.warning(f"Could not remove temp file: {path}")
                
    except Exception as e:
        logging.error(f"Unexpected error in hotkey handler: {e}", exc_info=True)
    finally:
        is_recording = False

def test_keyboard_hooks():
    """Test if keyboard hooks are still working"""
    global hotkey_failures, last_hotkey_test
    
    try:
        # Try to check key state - this will fail if hooks are broken
        keyboard.is_pressed('ctrl')
        keyboard.is_pressed('shift')
        
        # Try to get list of currently pressed keys
        pressed = keyboard._pressed_events
        
        last_hotkey_test = time.time()
        return True
    except Exception as e:
        hotkey_failures += 1
        logging.error(f"Keyboard hook test failed (failure #{hotkey_failures}): {e}")
        return False

def force_restart_hooks():
    """Aggressively restart keyboard hooks"""
    global hotkey_failures
    
    try:
        logging.warning("FORCE RESTARTING KEYBOARD HOOKS")
        
        # Unhook everything
        keyboard.unhook_all()
        time.sleep(0.5)
        
        # Clear internal state
        keyboard._pressed_events.clear()
        keyboard._physically_pressed_keys.clear()
        
        time.sleep(0.5)
        
        # Re-add hotkeys
        keyboard.add_hotkey("ctrl+shift", on_hotkey)
        keyboard.add_hotkey("ctrl+shift+esc", quit_application)
        
        time.sleep(0.5)
        
        # Test if it worked
        if test_keyboard_hooks():
            logging.info("Keyboard hooks successfully restarted!")
            hotkey_failures = 0
            return True
        else:
            logging.error("Hook restart failed")
            return False
            
    except Exception as e:
        logging.error(f"Failed to restart keyboard hooks: {e}")
        return False

def aggressive_monitor():
    """Aggressively monitor keyboard hook health"""
    global last_activity, hotkey_failures, service_active
    
    while service_active:
        try:
            time.sleep(15)  # Check every 15 seconds
            current_time = time.time()
            
            # Test keyboard hooks every 15 seconds
            if current_time - last_hotkey_test > 15:
                if not test_keyboard_hooks():
                    logging.warning("Keyboard hook test failed, attempting restart")
                    force_restart_hooks()
            
            # If we have multiple failures, try more aggressive recovery
            if hotkey_failures >= 3:
                logging.error(f"Multiple hook failures ({hotkey_failures}), forcing restart")
                force_restart_hooks()
            
            # Log status every 5 minutes
            if int(current_time) % 300 == 0:
                time_since_activity = current_time - last_activity
                logging.info(f"Service monitor: {time_since_activity:.0f}s since last activity, {hotkey_failures} failures")
                
        except Exception as e:
            logging.error(f"Monitor error: {e}")

def show_status(icon, item):
    """Show current status"""
    time_since_activity = time.time() - last_activity
    status = f"Last activity: {time_since_activity:.0f}s ago, Failures: {hotkey_failures}"
    logging.info(f"Status check - {status}")
    print(status)

def open_log(icon, item):
    """Open the log file"""
    try:
        os.startfile("voice_typing.log")
    except Exception as e:
        logging.error(f"Could not open log file: {e}")

def manual_restart_hooks(icon, item):
    """Manual hook restart from tray menu"""
    logging.info("Manual keyboard hook restart requested")
    force_restart_hooks()

def quit_application(icon=None, item=None):
    """Quit the application"""
    global tray_icon, service_active
    logging.info("Quitting voice typing service")
    service_active = False
    if tray_icon:
        tray_icon.stop()
    os._exit(0)

def setup_tray():
    """Set up the system tray icon"""
    global tray_icon
    
    icon_image = create_icon()
    
    menu = pystray.Menu(
        pystray.MenuItem("Voice Typing Service", show_status, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Show Status", show_status),
        pystray.MenuItem("Restart Hooks", manual_restart_hooks),
        pystray.MenuItem("Open Log", open_log),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", quit_application)
    )
    
    tray_icon = pystray.Icon("voice_typing", icon_image, "Voice Typing Service", menu)
    return tray_icon

if __name__ == "__main__":
    try:
        logging.info("Starting ROBUST voice typing service...")
        
        if not check_audio_devices():
            logging.error("No audio input devices found. Exiting.")
            exit(1)
        
        # Start aggressive monitoring thread
        monitor_thread = threading.Thread(target=aggressive_monitor, daemon=True)
        monitor_thread.start()
        
        print("Voice typing service ready!")
        print("Hold Ctrl+Shift to record, release to paste.")
        print("Press Ctrl+Shift+Esc to exit.")
        print("Console window will remain visible for stability.")
        
        # Set up hotkeys
        keyboard.add_hotkey("ctrl+shift", on_hotkey)
        keyboard.add_hotkey("ctrl+shift+esc", quit_application)
        
        # Initial hook test
        if not test_keyboard_hooks():
            logging.warning("Initial keyboard hook test failed!")
        
        # Set up system tray
        tray_icon = setup_tray()
        
        # REMOVED: Console window hiding code (causes hook issues)
        logging.info("Console window kept visible for keyboard hook stability")
        
        # Run the tray icon (this blocks)
        tray_icon.run()
        
    except KeyboardInterrupt:
        logging.info("Service stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
    finally:
        service_active = False
        logging.info("Voice typing service shutting down")