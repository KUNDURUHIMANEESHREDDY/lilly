import os
import sys
import json
import time
import subprocess
import tempfile
import re
from datetime import datetime

# External Libraries (Install via: pip install ollama SpeechRecognition pyttsx3 duckduckgo-search pypdf2 pyaudio)
import speech_recognition as sr
import pyttsx3
from ollama import chat
from duckduckgo_search import ddg
from PyPDF2 import PdfReader

class EVUltimate:
    def __init__(self):
        # --- Configuration ---
        self.model = "llama3.2"
        self.memory_file = "ev_memory.json"
        self.safety_blocked = ["rm -rf", "sudo", "format", "del /s", "mkfs", "adb shell rm -rf"]
        
        # --- Initialization ---
        self.init_voice()
        self.load_memory()
        self.speak("E.V. Ultimate Online. All systems integrated. Mobile bridge ready. What are we working on?")

    def init_voice(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 1.0)
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {"history": [], "facts": []}

    def save_memory(self):
        if len(self.memory["history"]) > 20:
            self.memory["history"] = self.memory["history"][-20:]
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def listen(self):
        print("🎤 Listening...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️ You: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Listen error: {e}")
            return None

    def speak(self, text):
        print(f"🤖 E.V.: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def search_web(self, query):
        try:
            results = ddg(query, max_results=3)
            if not results:
                return "No web results found."
            summary = "Here's what I found online: "
            for i, r in enumerate(results):
                summary += f"{i+1}. {r['title']}: {r['body']}. "
            return summary
        except Exception as e:
            return f"Web search failed: {str(e)}"

    def read_document(self, filename):
        if not os.path.exists(filename):
            files = [f for f in os.listdir('.') if filename.lower() in f.lower()]
            if files:
                filename = files[0]
            else:
                return f"File {filename} not found in current directory."
        try:
            if filename.endswith('.pdf'):
                reader = PdfReader(filename)
                text = ""
                for page in reader.pages[:3]:
                    text += page.extract_text()
                return f"Content of {filename}: {text[:2000]}..."
            elif filename.endswith(('.py', '.js', '.txt', '.md', '.json')):
                with open(filename, 'r') as f:
                    return f"Content of {filename}: {f.read()[:2000]}"
            else:
                return "I can only read PDF, Text, Code, and Markdown files currently."
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def execute_code_or_command(self, code=None, command=None, language="python"):
        safety_check = False
        if command:
            for blocked in self.safety_blocked:
                if blocked in command:
                    return f"Safety Alert: Blocked dangerous command '{command}'."
            safety_check = True
        
        try:
            if code:
                with tempfile.NamedTemporaryFile(mode='w', suffix=f".{language}", delete=False) as f:
                    f.write(code)
                    temp_path = f.name
                cmd = [sys.executable, temp_path] if language == "python" else [command, temp_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                os.remove(temp_path)
                if result.returncode != 0:
                    return f"Execution Error: {result.stderr}. I will try to fix this."
                return f"Success: {result.stdout}"
            elif command and safety_check:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
                if result.returncode != 0:
                    return f"Command failed: {result.stderr}"
                return f"Command output: {result.stdout}"
        except Exception as e:
            return f"Execution failed: {str(e)}"
        return "Operation completed."

    def control_mobile(self, action, target=None):
        """Phase 7: Mobile Control via ADB"""
        try:
            # Check if ADB is available
            subprocess.run(["adb", "version"], capture_output=True, check=True)
            
            cmd = ""
            if action == "screenshot":
                cmd = "adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./mobile_screen.png"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return "Screenshot saved as mobile_screen.png"
                return f"Screenshot failed: {result.stderr}"
            
            elif action == "open_app" and target:
                # Simplified: tries to start activity by package name (requires known package)
                cmd = f"adb shell monkey -p {target} -c android.intent.category.LAUNCHER 1"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Opened app {target}"
                return f"Failed to open {target}. Ensure package name is correct."
            
            elif action == "text" and target:
                cmd = f'adb shell input text "{target}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return "Text sent to mobile." if result.returncode == 0 else "Failed to send text."
            
            elif action == "tap" and target:
                # Expecting "x y" coordinates
                cmd = f"adb shell input tap {target}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return "Tap executed." if result.returncode == 0 else "Tap failed."
            
            else:
                return "Unknown mobile command or missing target."
        except subprocess.CalledProcessError:
            return "ADB not found or phone not connected. Please check USB debugging."
        except Exception as e:
            return f"Mobile control error: {str(e)}"

    def dynamic_loop(self, user_input):
        context_prompt = f"""
        You are E.V., a dynamic voice-only AI assistant. 
        Current Date: {datetime.now().strftime('%Y-%m-%d')}
        User Memory: {json.dumps(self.memory['facts'])}
        
        Available Tools:
        1. search_web(query): Real-time info.
        2. read_document(filename): Analyze local files.
        3. execute_command(cmd): Shell commands.
        4. write_and_run_code(code): Python execution.
        5. control_mobile(action, target): Android control (actions: screenshot, open_app, text, tap).
        
        Instructions:
        - If user mentions "phone", "mobile", "android", or "adb", USE control_mobile.
        - Output format for tools: <tool=NAME>ARGUMENT</tool>
        - If no tool needed, reply naturally.
        
        User Input: {user_input}
        """
        
        messages = [{"role": "user", "content": context_prompt}]
        for msg in self.memory["history"][-5:]:
            messages.insert(1, msg)

        try:
            # Step 1: Decide if a tool is needed
            tool_prompt = f"Analyze: '{user_input}'. If a tool is needed, output ONLY: <tool=NAME>ARGUMENT</tool>. Else output 'NONE'."
            tool_response = chat(model=self.model, messages=[{"role": "user", "content": tool_prompt}])
            tool_text = tool_response['message']['content']
            
            tool_match = re.search(r'<tool=(\w+)>(.*?)</tool>', tool_text, re.DOTALL)
            final_response = ""
            
            if tool_match:
                tool_name = tool_match.group(1)
                arg = tool_match.group(2).strip()
                
                self.speak(f"Executing {tool_name}...")
                
                if tool_name == "search_web":
                    final_response = self.search_web(arg)
                elif tool_name == "read_document":
                    final_response = self.read_document(arg)
                elif tool_name == "execute_command":
                    final_response = self.execute_code_or_command(command=arg)
                elif tool_name == "write_and_run_code":
                    final_response = self.execute_code_or_command(code=arg, language="python")
                elif tool_name == "control_mobile":
                    # Parse action and target from arg (e.g., "open_app com.whatsapp")
                    parts = arg.split(maxsplit=1)
                    action = parts[0]
                    target = parts[1] if len(parts) > 1 else None
                    final_response = self.control_mobile(action, target)
            else:
                # Normal conversation
                response = chat(model=self.model, messages=messages)
                final_response = response['message']['content']
                if "remember" in user_input.lower() or "my name is" in user_input.lower():
                    self.memory["facts"].append(f"{user_input}: {final_response}")

            self.memory["history"].append({"role": "user", "content": user_input})
            self.memory["history"].append({"role": "assistant", "content": final_response})
            self.save_memory()
            
            return final_response

        except Exception as e:
            return f"Internal error: {str(e)}. Let's try again."

    def run(self):
        while True:
            user_input = self.listen()
            if user_input:
                if "exit" in user_input.lower() or "shutdown" in user_input.lower():
                    self.speak("Shutting down all systems. Goodbye.")
                    break
                response = self.dynamic_loop(user_input)
                self.speak(response)

if __name__ == "__main__":
    try:
        agent = EVUltimate()
        agent.run()
    except KeyboardInterrupt:
        print("\nStopped by user.")
