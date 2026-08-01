# E.V. AI Assistant - Build Roadmap

A dynamic, voice-only AI engineering partner inspired by Spider-Man's E.D.I.T.H./E.V. system.

## 🎯 Ultimate Goal
Build a fully autonomous voice agent that can:
1. ✅ **Voice Conversation** - Talk naturally without any interface
2. ⏳ **Long-term Memory** - Remember projects across sessions
3. ⏳ **Computer Control** - Execute commands, manage files, control apps
4. ⏳ **Web Search** - Search live internet for components/tutorials
5. ⏳ **Document Reading** - Parse PDFs, codebases, technical docs
6. ⏳ **Code Execution** - Write, run, and debug code autonomously
7. ⏳ **Hardware Integration** - Interface with Arduino, ESP32, sensors

---

## 📋 Phase-by-Phase Build Plan

### ✅ Phase 1: Voice Core (CURRENT)
**Status:** Complete  
**File:** `ev_phase1_voice_core.py`  
**Capabilities:**
- Voice input via microphone
- Voice output via TTS
- Dynamic conversation with Ollama + Llama 3.2
- Context memory within session
- No hardcoded topics - fully adaptive

**Test it:**
```bash
python ev_phase1_voice_core.py
```

---

### 🔜 Phase 2: Long-term Memory
**Goal:** Remember conversations and projects between sessions  
**Features to add:**
- SQLite database for conversation history
- Project context persistence
- Recall previous discussions automatically
- Vector embeddings for semantic search

**Next file:** `ev_phase2_memory.py`

---

### 🔜 Phase 3: Computer Control
**Goal:** Safely execute system commands and manage files  
**Features to add:**
- Safe shell command execution with confirmation
- File read/write operations
- Directory navigation
- Application launching
- Permission sandboxing

**Next file:** `ev_phase3_control.py`

---

### 🔜 Phase 4: Web Search
**Goal:** Access live internet information  
**Features to add:**
- DuckDuckGo/Google search integration
- Website content scraping
- Real-time component pricing
- Tutorial discovery
- News and documentation lookup

**Next file:** `ev_phase4_search.py`

---

### 🔜 Phase 5: Document Reading
**Goal:** Parse and understand documents  
**Features to add:**
- PDF text extraction
- Codebase analysis
- Markdown/HTML parsing
- Technical specification reading
- Image OCR (optional)

**Next file:** `ev_phase5_docs.py`

---

### 🔜 Phase 6: Advanced Code Operations
**Goal:** Write, execute, and debug code autonomously  
**Features to add:**
- Multi-language code generation
- Local code execution sandbox
- Error detection and auto-fix
- Unit test generation
- Git integration

**Next file:** `ev_phase6_code.py`

---

### 🔜 Phase 7: Hardware Integration
**Goal:** Interface with physical components  
**Features to add:**
- Serial communication (Arduino/ESP32)
- GPIO control (Raspberry Pi)
- Sensor data reading
- Actuator control
- IoT device management

**Next file:** `ev_phase7_hardware.py`

---

### 🔜 Phase 8: Full Integration
**Goal:** Combine all capabilities into unified agent  
**Features:**
- Seamless capability switching
- Multi-step autonomous workflows
- Voice interruption handling
- Background task management
- Self-correction loops

**Final file:** `ev_complete.py`

---

## 🛠️ Current Setup Requirements

### Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from ollama.com
```

### Pull Model
```bash
ollama pull llama3.2
```

### Install Python Dependencies
```bash
pip install ollama SpeechRecognition pyttsx3 pyaudio
```

### Test Microphone
```bash
# Run the phase 1 script
python ev_phase1_voice_core.py
```

---

## 🎙️ Usage Examples (Phase 1)

**Project Planning:**
> "Plan a project to build a smart weather station"

**Code Generation:**
> "Write a Python script to fetch weather API data and save it to CSV"

**Debugging:**
> "My Docker container keeps crashing with error 137, what could be wrong?"

**Technical Explanations:**
> "Explain how I2C communication works in simple terms"

**Dynamic Topics:**
> "I want to learn about quantum computing basics"
> "Help me plan my garden layout for maximum yield"
> "What's the best way to organize my photo library?"

---

## 🚀 What's Next?

**Ready to build Phase 2 (Long-term Memory)?**  
Just say: *"Build Phase 2"* or *"Add memory capabilities"*

Each phase builds on the previous one, maintaining the voice-only, dynamic nature while adding powerful new capabilities.
