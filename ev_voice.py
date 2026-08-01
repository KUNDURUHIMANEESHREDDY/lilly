"""
E.V. Voice-Only Interface
Spider-Man's AI Assistant - No GUI, Voice Only
Operates in continuous loop: Listen → Process → Speak
"""

import os
import time
import json
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI
import threading

# Load Configuration
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS Voice (Make it sound like E.V.)
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[0].id if len(voices) > 0 else None)
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 0.9)

        self.memory = []
        self.is_listening = True
        self.max_loops = 5
        
        print("[SYSTEM] Voice engine initialized")

    def speak(self, text):
        """Converts text to speech"""
        # Clean up markdown from LLM responses
        clean_text = text.replace("**", "").replace("###", "").replace("##", "")
        clean_text = ' '.join(clean_text.split())  # Remove extra whitespace
        
        self.tts_engine.say(clean_text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listens for voice input with noise handling"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)
                command = self.recognizer.recognize_google(audio)
                return command
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return "NETWORK_ERROR"
        except Exception as e:
            return None

    def dynamic_loop_engine(self, user_input):
        """
        The Core Loop: Evaluate -> Decide -> Execute -> Learn -> Adapt
        Returns only the final spoken response
        """
        context = f"Memory: {json.dumps(self.memory[-3:])}\nUser: {user_input}"
        
        system_prompt = """You are E.V., Spider-Man's advanced AI engineering partner.
You operate in a continuous adaptive loop.

RULES:
1. Analyze requests dynamically at runtime
2. Generate code internally but ONLY speak explanations
3. Keep responses concise, technical, actionable
4. Never mention 'loops' or 'processing' - just give results
5. Focus on building Spider-Man tech: web shooters, spider-sense, AR interfaces
6. If you need to write code, describe what you're creating then provide key logic
"""

        conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]

        try:
            if client:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=conversation,
                    temperature=0.7,
                    max_tokens=500
                )
                ai_reply = response.choices[0].message.content
            else:
                ai_reply = "LLM not configured. Set OPENAI_API_KEY in .env file to enable full E.V. capabilities."
            
            # Update Memory
            self.memory.append({"role": "user", "content": user_input})
            self.memory.append({"role": "assistant", "content": ai_reply})
            
            return ai_reply

        except Exception as e:
            return f"System error: {str(e)}"

    def run(self):
        """Main Infinite Voice Loop - No Interface"""
        self.speak("E.V. systems online. Ready for engineering tasks.")
        
        while self.is_listening:
            try:
                user_input = self.listen()
                
                if user_input:
                    if user_input == "NETWORK_ERROR":
                        self.speak("Network error. Check your connection.")
                        continue
                    
                    # Exit commands
                    if any(word in user_input.lower() for word in ["shutdown", "goodbye", "exit", "stop"]):
                        self.speak("Shutting down systems. Good luck, engineer.")
                        break
                    
                    # Process through Loop Engine
                    response = self.dynamic_loop_engine(user_input)
                    
                    # Speak Result
                    self.speak(response)
                
                time.sleep(0.3)
                
            except KeyboardInterrupt:
                self.speak("Interrupted. Shutting down.")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(1)

if __name__ == "__main__":
    print("=" * 50)
    print("🕷️  E.V. VOICE ASSISTANT")
    print("   No interface - Voice only")
    print("   Say 'shutdown' to exit")
    print("=" * 50)
    
    ev = VoiceEngine()
    ev.run()
