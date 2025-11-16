🐱 AI Cat Emotion Analysis Agent

This project implements a web-based agent that uses the Gemini API's Multimodality capabilities to analyze an uploaded image of a cat and determine its emotional state (e.g., Happy, Angry, Relaxed).

The application uses a secure Client/Server architecture:

Client (Customer Brower.html): Handles the user interface and image upload via JavaScript.

Server (emotion_server.py): A lightweight Flask server that securely handles the API key and sends the image data to Google's Gemini service.

🚀 Setup and Execution

Prerequisites

Python 3.8+ (Recommended: Python 3.9.6, matching your VSC setup).

npm (for Live Server) or a modern browser.

A valid Gemini API Key. (Obtained from Google AI Studio).

Step 1: Install Python Dependencies

Open your VSC integrated terminal and install the required packages:

pip install Flask flask-cors requests


Step 2: Configure the API Key (CRITICAL!)

You must insert your private Gemini API key into the backend logic file.

Open the file emotion_logic.py.

Find the line defining API_KEY and replace the placeholder with your actual key:

# emotion_logic.py
API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE" 


Step 3: Start the Python Server

Keep the terminal open in your project root directory and run the server. The server must be running before you open the client.

python emotion_server.py


The terminal will display output confirming the server is running on http://127.0.0.1:5000.

Step 4: Run the Client (Web Interface)

Open the Customer Brower.html file in VSC.

Right-click the file in the Explorer panel and select "Open with Live Server" (if you have the extension installed).

The chat interface will open in your browser, ready to analyze images.

🛠 Troubleshooting (403 Forbidden Error)

If you upload an image and the client displays an error like:

Image Analysis Failed. Check VSC Terminal for Server Error. Details: Final API call failed... Error: 403 Client Error: Forbidden

This is an Authentication Error. Here are the two most likely causes and solutions:

Problem

Cause

Solution

Invalid Key

The key in emotion_logic.py is expired or incorrect.

Double-check the key in emotion_logic.py against your Google AI Studio dashboard.

API Not Enabled

Your Google Cloud Project has not enabled the necessary API permissions for image analysis.

Go to your Google Cloud Console, ensure your project is selected, and verify that the Gemini API is enabled under "APIs & Services."

Always remember to stop the server (Ctrl+C) and restart it after changing the emotion_logic.py file.