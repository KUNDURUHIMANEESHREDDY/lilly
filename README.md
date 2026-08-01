# E.V. - Enhanced Virtual Intelligence
## Spider-Man's AI Assistant Framework

A **dynamic** personal engineering partner inspired by Spider-Man's E.D.I.T.H. and E.V. systems from *Brand New Day*.

### 🆕 What's New: Dynamic Decision Making

E.V. now decides actions **at runtime** using LLM reasoning instead of hardcoded if/else routing!

- ✅ **No Hardcoded Logic** - Actions decided dynamically based on context
- ✅ **LLM-Powered** - Uses GPT-4o-mini to analyze requests and choose capabilities
- ✅ **Context-Aware** - Remembers conversation history for better decisions
- ✅ **Extensible** - Easy to add new capabilities to the registry
- ✅ **Fallback Mode** - Works with pattern matching when LLM unavailable

## Capabilities

- 🧠 **Dynamic Decision Making** - Runtime action selection via LLM
- 🎙️ **Voice Conversation** - Natural speech interaction (ready for integration)
- 💾 **Long-term Memory** - Stores and recalls information across sessions
- 💻 **Computer Control** - Execute commands safely, manage files
- 🔍 **Web Search** - DuckDuckGo integration for component research
- 📄 **Document Reading** - Parse code files, text documents
- 👨‍💻 **Code Operations** - Write, debug, explain code with LLM assistance
- 📋 **Project Planning** - Break down complex builds into phases

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OpenAI API key for full dynamic capabilities

# Run E.V.
python ev_assistant.py

# Or try the demo
python demo_dynamic.py
```

## How Dynamic Decisions Work

### Before (Hardcoded):
```python
if "search" in query:
    return self.search_web(query)
elif "plan" in query:
    return self.plan_project(query)
# ... rigid if/else chain
```

### After (Dynamic):
```python
# LLM analyzes request and decides which capability to use
action_data = self._decide_action(query)
# Returns: {"action": "search_web", "parameters": {"query": "..."}}
# Or: {"action": "plan_project", "parameters": {"goal": "..."}}
# Or: {"response": "Conversational reply"}
result = self._execute_action(action_data)
```

## Architecture

```
ev_assistant.py          # Main orchestrator with dynamic decision engine
demo_dynamic.py          # Interactive demo of dynamic capabilities
requirements.txt         # Dependencies
.env.example            # Configuration template
README.md               # This file
```

### Core Components:

1. **Capability Registry** - Dictionary of all available actions
2. **System Prompt Builder** - Dynamically generates LLM instructions with available capabilities
3. **Decision Engine** (`_decide_action`) - LLM or fallback determines which action to take
4. **Action Executor** (`_execute_action`) - Runs the selected capability
5. **Memory System** - Stores context for multi-turn conversations

## Configuration

Edit `.env` with your API keys:

```bash
OPENAI_API_KEY=sk-your-key-here
```

**Without API key**: Runs in demo mode with pattern-matching fallback  
**With API key**: Full LLM-powered dynamic decision making

## Usage Examples

```python
from ev_assistant import EV

ev = EV()

# Dynamic chat - E.V. decides what to do
ev.listen_and_respond("Find ultrasonic sensors for spider-sense")
# → Automatically calls search_web

ev.listen_and_respond("Plan a web shooter project")
# → Automatically calls plan_project

ev.listen_and_respond("Write Arduino code for MPU6050")
# → Automatically calls write_code

# Direct capability access
ev.remember("my_controller", "ESP32 WROOM")
ev.recall("my_controller")

ev.search_web("HC-SR04 datasheet")
ev.plan_project("Build AR glasses with XREAL")
```

## Demo Output

Run `python demo_dynamic.py` to see dynamic decision making in action:

```
🧠 DECISION:
   Action: search_web
   Parameters: {"query": "ultrasonic sensors"}

✅ RESULT:
   Found 5 results:
   • HC-SR04 Ultrasonic Sensor...
   
🧠 DECISION:
   Action: plan_project
   Parameters: {"goal": "web shooter build"}

✅ RESULT:
   {
     "phases": [
       {"name": "Research & Design", "tasks": [...]},
       {"name": "Prototype Build", "tasks": [...]},
       ...
     ]
   }
```

## Hardware Integration

Designed to work with Spider-Man tech builds:
- **Web Shooters**: ESP32, solenoids, gesture sensors (MPU6050)
- **Spider-Sense**: Ultrasonic sensors (HC-SR04), LiDAR (VL53L0X), vibration motors
- **AR Interface**: XREAL Air glasses, Raspberry Pi 5, camera modules
- **E.V. Assistant**: Any system with Python and internet access

## Adding New Capabilities

Easy to extend! Just add to the capability registry in `__init__`:

```python
self.capabilities["new_feature"] = {
    "description": "What this does",
    "function": self.new_method,
    "parameters": ["param1", "param2"]
}
```

The LLM will automatically know about and use the new capability!

## License

MIT License - Build your own Spider-Man tech! 🕷️