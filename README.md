# Touchless Human-Computer Interaction

A real-time Python application that enables users to control system **volume** and **screen brightness** using **hand gestures** and **voice commands**, providing a contactless user experience.

## 🚀 Features
- 🎯 Control system volume using **Left Hand gestures**
- 💡 Control screen brightness using **Right Hand gestures**
- 🎙️ Voice command fallback (when no hand is detected)
- ⚡ Works in real-time using webcam

## 🧠 Tech Stack
- Python 3.10
- OpenCV
- MediaPipe
- NumPy
- pycaw (volume control)
- screen-brightness-control
- SpeechRecognition

## 🛠️ How to Run

1. Clone the repo or download the code.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the project:

```bash
python main.py
```

## 📸 How It Works

- Left Hand pinch (thumb + index): Adjusts Volume
- Right Hand pinch (thumb + index): Adjusts Brightness
- No hand for 3 seconds: Activates voice command listener

## 🧪 Tested On
- Standard PC (8GB RAM, Windows 10)
- Webcam (720p)
- Python 3.10

## 👨‍💻 Author
**Gode Sai Kiran**  
MCA Student, Anurag University  
Presented at 5th CONIT Conference 2025
