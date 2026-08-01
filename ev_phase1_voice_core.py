"""
E.V. Voice Agent - Phase 1: Core Voice Loop with Ollama
Capabilities: Voice conversation, dynamic intent recognition, local LLM reasoning
"""
import speech_recognition as sr
import pyttsx3
import ollama
import json
import sys

class EVVoiceAgent:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Conversation history for context
        self.conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are E.V., a dynamic, voice-only AI engineering partner. "
                    "You have NO predefined topics. You adapt to whatever the user discusses. "
                    "Your capabilities include: "
                    "1. Writing and debugging code in any language. "
                    "2. Planning complex projects step-by-step. "
                    "3. Explaining technical concepts simply. "
                    "4. Searching for information (simulated via reasoning if no tool available). "
                    "5. Executing safe shell commands if explicitly requested and safe. "
                    "\n"
                    "CRITICAL INSTRUCTIONS:"
                    "- Listen to the user's voice input. "
                    "- Analyze the intent dynamically. "
                    "- If the user asks for code, generate it. "
                    "- If the user asks for a plan, create a structured plan. "
                    "- If the user reports an error, debug it logically. "
                    "- Do not assume the topic. Follow the user's lead completely. "
                    "- Keep responses concise and conversational for voice output. "
                    "- If a task requires multiple steps, think step-by-step internally before speaking."
                )
            }
        ]
        
        print("🕷️ E.V. Phase 1 Initialized - Voice Core Ready")

    def listen(self):
        """Listen for voice input with noise adjustment"""
        print("🎤 Listening...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("⏱️ Timeout - no speech detected")
                return None
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
                return None
            except Exception as e:
                print(f"🔇 Error listening: {e}")
                return None

    def speak(self, text):
        """Convert text to speech"""
        # Clean up text for better TTS
        text = text.replace("*", "").replace("#", "").replace("```", "")
        print(f"🤖 E.V.: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def loop_engine(self, user_input):
        """Dynamic loop: Evaluate → Decide → Respond → Learn"""
        # Add user input to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Call Ollama with Llama 3.2
            response = ollama.chat(
                model='llama3.2',
                messages=self.conversation_history,
                stream=False
            )
            
            assistant_message = response['message']['content']
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant", 
                "content": assistant_message
            })
            
            # Keep history manageable (last 20 messages)
            if len(self.conversation_history) > 20:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-19:]
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}. Let's try rephrasing."
            return error_msg

    def run(self):
        """Main voice interaction loop"""
        self.speak("E.V. Online. I am ready to work on any topic. What are we building or solving today?")
        
        while True:
            user_input = self.listen()
            
            if user_input:
                # Check for exit commands
                if any(word in user_input.lower() for word in ["exit", "quit", "shutdown", "goodbye"]):
                    self.speak("Shutting down. Goodbye.")
                    break
                
                # Process through loop engine
                response = self.loop_engine(user_input)
                self.speak(response)
            else:
                # No input detected, continue listening
                pass

if __name__ == "__main__":
    agent = EVVoiceAgent()
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
        sys.exit(0)
