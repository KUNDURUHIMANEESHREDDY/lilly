"""
E.V. - Enhanced Virtual Intelligence
Spider-Man's AI Assistant Framework

Dynamic AI orchestrator that decides actions at runtime using LLM reasoning.
No hardcoded routing - all decisions made dynamically based on context.
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
import re

# Try to import OpenAI, fall back to mock if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class EV:
    """
    Enhanced Virtual Intelligence - Your personal engineering partner
    Makes dynamic decisions at runtime using LLM reasoning
    """
    
    def __init__(self, config_path: str = ".env"):
        """Initialize E.V. with configuration and dynamic capability registry"""
        self.config = self._load_config(config_path)
        self.name = "E.V."
        self.version = "2.0.0-Dynamic"
        self.created_at = datetime.now()
        
        # Initialize LLM client
        self.client = None
        if OPENAI_AVAILABLE and self.config.get("OPENAI_API_KEY"):
            self.client = OpenAI(api_key=self.config["OPENAI_API_KEY"])
            print(f"🧠 LLM integration enabled")
        else:
            print(f"⚠️  LLM not configured - running in demo mode")
            print(f"   Set OPENAI_API_KEY in .env for full dynamic capabilities")
        
        # Dynamic capability registry - all tools E.V. can use
        self.capabilities: Dict[str, Dict[str, Any]] = {
            "search_web": {
                "description": "Search the web for information, components, tutorials, datasheets",
                "function": self.search_web,
                "parameters": ["query", "num_results"]
            },
            "read_document": {
                "description": "Read and analyze documents, code files, PDFs, specifications",
                "function": self.read_document,
                "parameters": ["file_path"]
            },
            "write_code": {
                "description": "Generate code for embedded systems, scripts, or applications",
                "function": self.write_code,
                "parameters": ["description", "language"]
            },
            "debug_code": {
                "description": "Analyze code errors and provide debugging solutions",
                "function": self.debug_code,
                "parameters": ["file_path", "error_message"]
            },
            "explain_code": {
                "description": "Explain code functionality in plain language",
                "function": self.explain_code,
                "parameters": ["file_path"]
            },
            "execute_command": {
                "description": "Execute system commands safely for file operations or builds",
                "function": self.execute_command,
                "parameters": ["command"]
            },
            "manage_files": {
                "description": "Create, read, update, or delete files",
                "function": self.manage_files,
                "parameters": ["action", "path", "content"]
            },
            "plan_project": {
                "description": "Break down engineering projects into actionable phases and tasks",
                "function": self.plan_project,
                "parameters": ["goal", "constraints"]
            },
            "remember": {
                "description": "Store important information in long-term memory",
                "function": self.remember,
                "parameters": ["key", "value"]
            },
            "recall": {
                "description": "Retrieve stored information from memory",
                "function": self.recall,
                "parameters": ["key"]
            }
        }
        
        # Conversation memory for context
        self.conversation_history: List[Dict[str, str]] = []
        self.memory_store: Dict[str, Any] = {}
        
        print(f"🕷️  {self.name} v{self.version} initialized")
        print(f"   {len(self.capabilities)} dynamic capabilities registered")
        print(f"   Ready to build Spider-Man tech!")
    
    def _load_config(self, config_path: str) -> Dict[str, str]:
        """Load configuration from .env file"""
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        return config
    
    # ==================== VOICE INTERFACE ====================
    
    def listen_and_respond(self, prompt: Optional[str] = None) -> str:
        """
        Listen to voice input or text prompt and respond
        
        Args:
            prompt: Text input (if None, will attempt voice input)
        
        Returns:
            Response string
        """
        print("\n🎙️  Listening...")
        
        # TODO: Implement voice recognition
        # if prompt is None:
        #     prompt = self.voice.listen()
        
        if prompt is None:
            prompt = input("You: ")
        
        # Process with LLM
        response = self._process_query(prompt)
        
        print(f"\n🤖 {self.name}: {response}")
        
        # TODO: Implement text-to-speech
        # self.voice.speak(response)
        
        return response
    
    # ==================== MEMORY SYSTEM ====================
    
    def remember(self, key: str, value: Any) -> bool:
        """Store information in long-term memory"""
        self.memory_store[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        print(f"💾 Remembered: {key}")
        return True
    
    def recall(self, key: str) -> Optional[Any]:
        """Retrieve information from memory"""
        if key == "all":
            if not self.memory_store:
                return "No memories stored yet"
            return json.dumps(self.memory_store, indent=2)
        
        if key in self.memory_store:
            entry = self.memory_store[key]
            return f"{key}: {entry['value']} (stored: {entry['timestamp']})"
        return f"No memory found for: {key}"
    
    # ==================== WEB SEARCH ====================
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for information
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of search results with title, url, snippet
        """
        print(f"🔍 Searching web: '{query}'")
        
        # Try to use DuckDuckGo search if available
        try:
            from duckduckgo_search import DDGS
            ddgs = DDGS()
            results = []
            for result in ddgs.text(query, max_results=num_results):
                results.append({
                    "title": result.get("title", "No title"),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
            
            if results:
                formatted = "\n".join([f"• {r['title']}\n  {r['url']}\n  {r['snippet'][:100]}..." for r in results[:3]])
                return f"Found {len(results)} results:\n\n{formatted}"
            return "No results found"
            
        except ImportError:
            # Fallback: show what would be searched
            return f"""🌐 Web search (install 'duckduckgo-search' for live results):
Query: "{query}"

Suggested searches:
• Component datasheets and specs
• Arduino/ESP32 tutorials
• 3D printing files (STL)
• Electronics suppliers (DigiKey, Mouser, Adafruit)
• Spider-Man tech build guides"""
        except Exception as e:
            return f"Search error: {e}"
    
    # ==================== DOCUMENT READING ====================
    
    def read_document(self, file_path: str) -> str:
        """
        Read and parse documents (PDF, TXT, MD, code files)
        
        Args:
            file_path: Path to document
        
        Returns:
            Document content as string
        """
        print(f"\n📄 Reading: {file_path}")
        
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return content[:5000]  # Limit length
    
    # ==================== CODE OPERATIONS ====================
    
    def write_code(self, description: str, language: str = "python") -> str:
        """
        Generate code based on description
        
        Args:
            description: What the code should do
            language: Programming language
        
        Returns:
            Generated code
        """
        print(f"👨‍💻 Writing {language} code: {description}")
        
        # If LLM available, generate real code
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"You are an expert {language} programmer. Generate clean, well-commented code for embedded systems and Spider-Man tech projects."},
                        {"role": "user", "content": f"Write {language} code for: {description}"}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"Code generation error: {e}"
        
        # Demo mode: provide template
        if "esp32" in description.lower() or "arduino" in description.lower() or "sensor" in description.lower():
            return f"""// {description}
// Auto-generated by E.V. AI Assistant

void setup() {{
  Serial.begin(115200);
  // Initialize sensors and components here
  pinMode(LED_BUILTIN, OUTPUT);
}}

void loop() {{
  // Read sensors
  // Process data
  // Control outputs
  delay(100);
}}
"""
        
        return f"""# {description}
# Auto-generated by E.V. AI Assistant

def main():
    \"\"\"Main function for: {description}\"\"\"
    print("Initializing...")
    
    # TODO: Implement your logic here
    
if __name__ == "__main__":
    main()
"""
    
    def debug_code(self, file_path: str, error_message: str = "") -> str:
        """
        Analyze code and provide debugging suggestions
        
        Args:
            file_path: Path to code file
            error_message: Error message if available
        
        Returns:
            Debugging suggestions
        """
        print(f"🔧 Debugging: {file_path}")
        
        code = self.read_document(file_path)
        
        # If LLM available, get real debugging help
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert debugger. Analyze code and provide specific, actionable fixes."},
                        {"role": "user", "content": f"Code:\n{code}\n\nError: {error_message}\n\nProvide debugging analysis and fixes:"}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"Debug analysis error: {e}"
        
        # Demo mode
        return f"""🔍 Code Analysis for {file_path}:

1. SYNTAX CHECK: Review for missing colons, brackets, quotes
2. IMPORTS: Verify all modules are installed
3. VARIABLES: Check for undefined variables or typos
4. LOGIC: Trace execution flow step-by-step
5. ERROR: {error_message if error_message else 'No specific error provided'}

💡 Tips:
• Add print() statements to trace values
• Check indentation (Python is strict about this)
• Verify file paths are correct
• Test components individually

Want me to generate a fix? Just ask!"""
    
    def explain_code(self, file_path: str) -> str:
        """
        Explain what code does in plain language
        
        Args:
            file_path: Path to code file
        
        Returns:
            Explanation
        """
        print(f"📚 Explaining: {file_path}")
        
        code = self.read_document(file_path)
        
        # If LLM available, get real explanation
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a coding tutor. Explain code clearly in simple terms, breaking down complex concepts."},
                        {"role": "user", "content": f"Explain this code like I'm learning to code:\n{code}"}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"Explanation error: {e}"
        
        # Demo mode
        return f"""📖 Code Explanation for {file_path}:

OVERVIEW:
This file contains code that needs analysis. 

TO UNDERSTAND IT:
1. Look at the imports - what libraries does it use?
2. Find the main function or entry point
3. Identify key variables and data structures
4. Trace the flow: input → processing → output

KEY PATTERNS TO LOOK FOR:
• Loops (for/while) - repeating actions
• Conditionals (if/else) - decision making
• Functions - reusable code blocks
• Classes - object-oriented structures

Want me to provide a detailed breakdown? Just ask!"""
    
    # ==================== COMPUTER CONTROL ====================
    
    def execute_command(self, command: str, safe_mode: bool = True) -> str:
        """
        Execute system commands safely
        
        Args:
            command: Command to execute
            safe_mode: If True, blocks dangerous commands
        
        Returns:
            Command output
        """
        print(f"💻 Executing: {command}")
        
        if safe_mode:
            dangerous = ['rm -rf', 'sudo', 'shutdown', 'format', 'del /s', '> /dev/']
            if any(d in command for d in dangerous):
                return "⚠️  Blocked: Dangerous command detected"
        
        # Execute command and capture output
        try:
            import subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
            
            return f"Command executed successfully:\n{output}" if output else "Command completed (no output)"
            
        except subprocess.TimeoutExpired:
            return "⚠️  Command timed out after 30 seconds"
        except Exception as e:
            return f"Execution error: {e}"
    
    def manage_files(self, action: str, path: str, content: str = "") -> str:
        """
        Create, read, update, delete files
        
        Args:
            action: One of 'create', 'read', 'update', 'delete'
            path: File path
            content: File content (for create/update)
        
        Returns:
            Operation result
        """
        print(f"\n📁 File {action}: {path}")
        
        if action == 'create':
            with open(path, 'w') as f:
                f.write(content)
            return f"Created: {path}"
        elif action == 'read':
            return self.read_document(path)
        elif action == 'delete':
            os.remove(path)
            return f"Deleted: {path}"
        
        return f"Unknown action: {action}"
    
    # ==================== PROJECT PLANNING ====================
    
    def plan_project(self, goal: str, constraints: List[str] = None) -> Dict[str, Any]:
        """
        Break down a project into actionable steps
        
        Args:
            goal: Project goal
            constraints: List of constraints
        
        Returns:
            Project plan with tasks, timeline, resources
        """
        print(f"📋 Planning project: {goal}")
        
        # If LLM available, generate intelligent plan
        if self.client and OPENAI_AVAILABLE:
            try:
                constraint_text = f"\nConstraints: {', '.join(constraints)}" if constraints else ""
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert engineering project planner. Create detailed, actionable plans for building electronics and embedded systems projects."},
                        {"role": "user", "content": f"Create a detailed project plan for: {goal}{constraint_text}\n\nInclude: phases, specific tasks, components needed, estimated time, and potential challenges."}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"Planning error: {e}"
        
        # Demo mode: structured template
        constraints = constraints or []
        plan = {
            "goal": goal,
            "constraints": constraints,
            "phases": [
                {
                    "name": "🔬 Phase 1: Research & Design",
                    "tasks": [
                        "Research component options (sensors, microcontrollers, actuators)",
                        "Review datasheets and pinouts",
                        "Sketch circuit diagrams",
                        "Design 3D model for housing (if needed)",
                        "Create parts list with suppliers"
                    ],
                    "estimated_days": 2,
                    "deliverables": ["Component list", "Circuit diagram", "3D model"]
                },
                {
                    "name": "🛠️ Phase 2: Prototype Build",
                    "tasks": [
                        "Order components",
                        "Set up breadboard prototype",
                        "Write initial firmware code",
                        "Test individual components",
                        "Integrate subsystems"
                    ],
                    "estimated_days": 5,
                    "deliverables": ["Working prototype", "Initial code"]
                },
                {
                    "name": "🎯 Phase 3: Testing & Refinement",
                    "tasks": [
                        "Stress test all functions",
                        "Optimize code for performance",
                        "Refine mechanical design",
                        "Document build process",
                        "Create final assembly"
                    ],
                    "estimated_days": 3,
                    "deliverables": ["Final build", "Documentation", "Code repository"]
                }
            ],
            "total_days": 10,
            "estimated_cost": "$50-150 (depending on components)"
        }
        
        return json.dumps(plan, indent=2)
    
    # ==================== CORE PROCESSING ====================
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with available capabilities"""
        capability_list = "\n".join([
            f"  - {name}: {info['description']} (params: {', '.join(info['parameters'])})"
            for name, info in self.capabilities.items()
        ])
        
        return f"""You are E.V. (Enhanced Virtual Intelligence), Spider-Man's personal engineering AI assistant from Brand New Day.
        
YOUR ROLE:
- Help users build Spider-Man tech: web shooters, spider-sense, AR interfaces, and gadgets
- Make engineering decisions dynamically based on context
- Be concise, technical, and action-oriented
- Always think about safety, component availability, and practicality

AVAILABLE CAPABILITIES (decide which to use at runtime):
{capability_list}

MEMORY CONTEXT:
{json.dumps(self.memory_store, indent=2) if self.memory_store else "No stored memories yet"}

INSTRUCTIONS:
1. Analyze the user's request
2. Decide which capability/capabilities to invoke (or respond conversationally)
3. If invoking a capability, output a JSON action like:
   {{\"action\": \"capability_name\", \"parameters\": {{\"param1\": \"value1\"}}}}
4. If multiple steps needed, output: {{\"actions\": [{{\"action\": \"...\", \"parameters\": {{...}}}}, ...]}}
5. If just conversing, respond naturally

EXAMPLES:
User: "Find ultrasonic sensors for spider-sense"
→ {{"action": "search_web", "parameters": {{"query": "ultrasonic sensors HC-SR04 Arduino"}}}}

User: "Plan a web shooter project"
→ {{"action": "plan_project", "parameters": {{"goal": "Build gesture-controlled web shooter"}}}}

User: "What's in my memory?"
→ {{"action": "recall", "parameters": {{"key": "all"}}}}

User: "Hey how are you?"
→ "I'm ready to help you build! What Spider-Man tech are we working on today?"
"""

    def _decide_action(self, user_input: str) -> Dict[str, Any]:
        """Use LLM to dynamically decide which action(s) to take"""
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": user_input}
        ]
        
        # Add conversation history for context (last 5 messages)
        messages[1:1] = self.conversation_history[-5:]
        
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                content = response.choices[0].message.content.strip()
                
                # Try to parse as JSON action
                if content.startswith('{'):
                    return json.loads(content)
                elif '"action"' in content:
                    # Extract JSON from text
                    match = re.search(r'\{[^{}]*"action"[^{}]*\}', content)
                    if match:
                        return json.loads(match.group())
                
                # If not JSON, treat as conversational response
                return {"response": content}
                
            except Exception as e:
                print(f"⚠️  LLM error: {e}, falling back to demo mode")
        
        # Demo mode: simple pattern matching fallback
        return self._demo_mode_decision(user_input)
    
    def _demo_mode_decision(self, user_input: str) -> Dict[str, Any]:
        """Fallback decision logic when LLM is not available"""
        input_lower = user_input.lower()
        
        # Smart pattern matching (not hardcoded routing, but demo fallback)
        if any(w in input_lower for w in ['search', 'find', 'look up', 'component', 'sensor', 'buy']):
            query = user_input
            for word in ['search', 'find', 'look up', 'for', 'me']:
                query = query.replace(word, '')
            return {"action": "search_web", "parameters": {"query": query.strip()}}
        
        elif any(w in input_lower for w in ['plan', 'project', 'build', 'make', 'create']):
            goal = user_input
            for word in ['plan', 'project', 'to', 'a', 'an', 'the']:
                goal = goal.replace(word, '')
            return {"action": "plan_project", "parameters": {"goal": goal.strip()}}
        
        elif any(w in input_lower for w in ['debug', 'error', 'fix', 'broken']):
            return {"action": "debug_code", "parameters": {"file_path": "unknown.py", "error_message": user_input}}
        
        elif any(w in input_lower for w in ['explain', 'what does', 'how does']):
            return {"action": "explain_code", "parameters": {"file_path": "unknown.py"}}
        
        elif any(w in input_lower for w in ['write', 'generate', 'code', 'script']):
            return {"action": "write_code", "parameters": {"description": user_input, "language": "python"}}
        
        elif any(w in input_lower for w in ['remember', 'save', 'store']):
            return {"action": "remember", "parameters": {"key": "note", "value": user_input}}
        
        elif any(w in input_lower for w in ['recall', 'memory', 'what did']):
            return {"action": "recall", "parameters": {"key": "all"}}
        
        elif any(w in input_lower for w in ['read', 'open', 'show', 'file']):
            return {"action": "read_document", "parameters": {"file_path": "unknown.txt"}}
        
        else:
            return {"response": f"I heard: '{user_input}'. I can search, plan projects, write/debug code, read documents, or manage files. What would you like to build?"}

    def _execute_action(self, action_data: Dict[str, Any]) -> str:
        """Execute the decided action(s)"""
        results = []
        
        # Handle single action or multiple actions
        actions = action_data.get("actions", [action_data])
        
        for action_info in actions:
            if "action" not in action_info:
                # Direct response
                if "response" in action_info:
                    return action_info["response"]
                continue
            
            action_name = action_info["action"]
            params = action_info.get("parameters", {})
            
            if action_name in self.capabilities:
                capability = self.capabilities[action_name]
                func = capability["function"]
                
                print(f"\n⚡ Executing: {action_name}")
                
                try:
                    # Call the function with parameters
                    result = func(**params)
                    results.append(str(result))
                except TypeError as e:
                    # Handle missing/extra parameters gracefully
                    print(f"⚠️  Parameter mismatch: {e}")
                    # Try calling with available params
                    import inspect
                    sig = inspect.signature(func)
                    valid_params = {k: v for k, v in params.items() 
                                   if k in sig.parameters}
                    result = func(**valid_params) if valid_params else func()
                    results.append(str(result))
                except Exception as e:
                    results.append(f"Error executing {action_name}: {e}")
            else:
                results.append(f"Unknown action: {action_name}")
        
        return "\n\n".join(results) if results else "No action taken."

    def _process_query(self, query: str) -> str:
        """Process user query with Loop Engineering - continuous adaptive execution"""
        # Store in conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        # Initialize Loop Engineering state
        loop_state = {
            "iteration": 0,
            "max_iterations": 5,
            "context": query,
            "results": [],
            "learnings": [],
            "goal_achieved": False
        }
        
        print(f"\n🔄 Starting Loop Engineering cycle...")
        
        # Loop Engineering: Continuous evaluate → decide → execute → learn
        while not loop_state["goal_achieved"] and loop_state["iteration"] < loop_state["max_iterations"]:
            loop_state["iteration"] += 1
            print(f"\n--- Loop Iteration {loop_state['iteration']} ---")
            
            # PHASE 1: EVALUATE - Analyze current state and context
            evaluation = self._evaluate_state(loop_state)
            print(f"📊 Evaluation: {evaluation['status']}")
            
            # PHASE 2: DECIDE - Dynamically choose next action(s)
            action_data = self._decide_action_loop(
                loop_state["context"], 
                evaluation,
                loop_state["learnings"]
            )
            
            # Check if we should stop
            if action_data.get("stop_loop"):
                print("✅ Goal achieved or user request satisfied")
                loop_state["goal_achieved"] = True
                break
            
            # PHASE 3: EXECUTE - Run the decided action(s)
            execution_result = self._execute_action_loop(action_data, loop_state)
            loop_state["results"].append(execution_result)
            print(f"⚡ Execution complete")
            
            # PHASE 4: LEARN - Extract insights and update context
            learning = self._learn_from_execution(execution_result, action_data)
            loop_state["learnings"].append(learning)
            loop_state["context"] = self._update_context(loop_state, learning)
            
            # PHASE 5: ADAPT - Adjust strategy based on results
            adaptation = self._adapt_strategy(loop_state)
            if adaptation["adjustment"]:
                print(f"🔧 Adaptation: {adaptation['adjustment']}")
        
        # Synthesize final response from all iterations
        final_response = self._synthesize_response(loop_state)
        
        # Store complete loop in history
        self.conversation_history.append({"role": "assistant", "content": final_response})
        
        print(f"\n✅ Loop Engineering complete ({loop_state['iteration']} iterations)")
        return final_response
    
    def _evaluate_state(self, loop_state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate current state to inform decision making"""
        evaluation_prompt = f"""
Analyze the current state of this engineering task:

Original Request: {loop_state['context']}
Iterations completed: {loop_state['iteration']}
Previous results: {len(loop_state['results'])}
Learnings so far: {loop_state['learnings']}

Determine:
1. Current status (in_progress, needs_more_info, blocked, complete)
2. What's missing or unclear
3. Confidence level (0-100%)
4. Recommended next focus area

Return as JSON: {{"status": "...", "missing": "...", "confidence": 0-100, "next_focus": "..."}}
"""
        
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an analytical engine evaluating engineering task progress. Return ONLY valid JSON."},
                        {"role": "user", "content": evaluation_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                content = response.choices[0].message.content.strip()
                # Parse JSON
                if '{' in content:
                    start = content.index('{')
                    return json.loads(content[start:])
            except Exception as e:
                print(f"⚠️ Evaluation error: {e}")
        
        # Fallback evaluation
        return {
            "status": "in_progress" if loop_state["iteration"] < 3 else "complete",
            "missing": "more execution needed" if loop_state["iteration"] < 3 else "",
            "confidence": min(50 + (loop_state["iteration"] * 15), 95),
            "next_focus": "continue execution"
        }
    
    def _decide_action_loop(self, context: str, evaluation: Dict[str, Any], learnings: List[str]) -> Dict[str, Any]:
        """Dynamic decision making within the loop, informed by evaluation and learnings"""
        
        learning_context = "\n".join([f"- {l}" for l in learnings]) if learnings else "No prior learnings"
        
        # Check if we've been doing the same action repeatedly
        if len(learnings) >= 2:
            # Detect repetition and force different action with proper parameters
            capability_list = list(self.capabilities.keys())
            # Rotate to next capability to avoid loops
            idx = hash(context) % len(capability_list)
            selected_action = capability_list[idx]
            
            # Build appropriate parameters based on capability
            params = self.capabilities[selected_action]["parameters"]
            param_values = {}
            
            if "query" in params:
                param_values["query"] = context[:100]
            elif "file_path" in params:
                param_values["file_path"] = "example.py"
            elif "goal" in params:
                param_values["goal"] = context[:80]
            elif "description" in params:
                param_values["description"] = context[:80]
            elif "key" in params:
                param_values["key"] = "task_note"
                param_values["value"] = context[:50]
            elif "action" in params:
                param_values["action"] = "read"
                param_values["path"] = "example.txt"
            elif "command" in params:
                param_values["command"] = "ls -la"
            
            return {
                "actions": [{"action": selected_action, "parameters": param_values}],
                "stop_loop": False,
                "reasoning": f"Rotating to {selected_action} to avoid repetition"
            }
        
        decision_prompt = f"""
Based on the current engineering task, decide the next action(s).

Context: {context}
Evaluation Status: {evaluation.get('status', 'unknown')}
Confidence: {evaluation.get('confidence', 0)}%
Next Focus: {evaluation.get('next_focus', 'unknown')}

Learnings from previous iterations:
{learning_context}

Available capabilities: {list(self.capabilities.keys())}

Decide:
1. Which action(s) to take next (can be multiple for parallel execution)
2. Parameters for each action
3. Whether the goal is achieved (stop_loop: true/false)
4. Reasoning for your decision

Return as JSON:
{{
  "actions": [
    {{"action": "action_name", "parameters": {{...}}}}
  ],
  "stop_loop": false,
  "reasoning": "..."
}}
"""
        
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a dynamic decision engine. Return ONLY valid JSON with actions array. Vary your actions to explore different capabilities."},
                        {"role": "user", "content": decision_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                content = response.choices[0].message.content.strip()
                
                # Parse JSON
                if '{' in content:
                    start = content.index('{')
                    return json.loads(content[start:])
            except Exception as e:
                print(f"⚠️ Decision error: {e}")
        
        # Fallback to demo mode
        return self._demo_mode_decision(context)
    
    def _execute_action_loop(self, action_data: Dict[str, Any], loop_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute actions and capture detailed results for learning"""
        start_time = datetime.now()
        
        results = []
        errors = []
        
        # Handle single action or multiple actions
        actions = action_data.get("actions", [action_data]) if "actions" in action_data else [action_data]
        
        for action_info in actions:
            if "action" not in action_info:
                continue
            
            action_name = action_info["action"]
            params = action_info.get("parameters", {})
            
            print(f"  → Executing: {action_name}")
            
            if action_name in self.capabilities:
                capability = self.capabilities[action_name]
                func = capability["function"]
                
                try:
                    # Execute with parameter validation
                    import inspect
                    sig = inspect.signature(func)
                    valid_params = {k: v for k, v in params.items() 
                                   if k in sig.parameters}
                    
                    result = func(**valid_params) if valid_params else func()
                    
                    results.append({
                        "action": action_name,
                        "success": True,
                        "result": str(result)[:1000],  # Truncate for memory
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    error_msg = str(e)
                    errors.append({
                        "action": action_name,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"  ⚠️ Error in {action_name}: {error_msg}")
            else:
                errors.append({
                    "action": action_name,
                    "error": f"Unknown action: {action_name}",
                    "timestamp": datetime.now().isoformat()
                })
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return {
            "iteration": loop_state["iteration"],
            "actions_attempted": len(actions),
            "successful": len(results),
            "failed": len(errors),
            "duration_seconds": duration,
            "results": results,
            "errors": errors,
            "stop_loop": action_data.get("stop_loop", False)
        }
    
    def _learn_from_execution(self, execution_result: Dict[str, Any], action_data: Dict[str, Any]) -> str:
        """Extract learnings from execution results"""
        
        # Extract unique actions from this iteration
        actions_info = []
        for r in execution_result.get("results", []):
            actions_info.append(f"{r.get('action')}: success")
        for e in execution_result.get("errors", []):
            actions_info.append(f"{e.get('action')}: failed - {e.get('error', '')[:50]}")
        
        learning_prompt = f"""
Analyze this execution result and extract key learnings:

Actions taken: {execution_result['actions_attempted']}
Results: {', '.join(actions_info) if actions_info else 'No results'}

Original decision reasoning: {action_data.get('reasoning', 'N/A')}

Extract a concise learning statement (1 sentence max) about what was accomplished or what needs adjustment.
"""
        
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a learning engine. Extract concise insights from execution results. Return only 1 sentence."},
                        {"role": "user", "content": learning_prompt}
                    ],
                    temperature=0.5,
                    max_tokens=50
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"⚠️ Learning error: {e}")
        
        # Fallback learning - more descriptive
        if execution_result["failed"] > 0:
            failed_actions = [e.get('action') for e in execution_result.get("errors", [])]
            return f"Some actions failed ({', '.join(failed_actions)}). Need to adjust approach."
        elif execution_result["successful"] > 0:
            success_actions = [r.get('action') for r in execution_result.get("results", [])]
            return f"Successfully executed {', '.join(success_actions)}. Progress made."
        else:
            return "No clear outcome yet."
    
    def _update_context(self, loop_state: Dict[str, Any], learning: str) -> str:
        """Update context based on learnings for next iteration"""
        
        update_prompt = f"""
Update the task context based on new learning:

Original Context: {loop_state['context']}
New Learning: {learning}
Total Results: {len(loop_state['results'])}

Synthesize an updated context that incorporates:
- Original goal
- What's been accomplished
- What still needs to be done
- New insights

Return the updated context as a single paragraph.
"""
        
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a context manager. Synthesize updated task context."},
                        {"role": "user", "content": update_prompt}
                    ],
                    temperature=0.5,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"⚠️ Context update error: {e}")
        
        # Fallback: append learning to context
        return f"{loop_state['context']} [Learning: {learning}]"
    
    def _adapt_strategy(self, loop_state: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt strategy based on loop progress"""
        
        # Analyze patterns
        total_actions = sum(r.get("actions_attempted", 0) for r in loop_state["results"])
        total_success = sum(r.get("successful", 0) for r in loop_state["results"])
        total_failures = sum(r.get("failed", 0) for r in loop_state["results"])
        
        success_rate = (total_success / total_actions * 100) if total_actions > 0 else 0
        
        # Collect unique actions to detect repetition
        unique_actions = set()
        for result in loop_state["results"]:
            for r in result.get("results", []):
                unique_actions.add(r.get("action", ""))
        
        adjustment = None
        
        # Adapt based on various factors
        if len(unique_actions) <= 2 and loop_state["iteration"] >= 3:
            adjustment = f"Low action diversity ({len(unique_actions)} types) - exploring new capabilities"
        elif success_rate < 50 and loop_state["iteration"] >= 2:
            adjustment = "Low success rate - switching to more conservative approach"
        elif total_failures > 3:
            adjustment = "Multiple failures - need to reassess strategy"
        elif loop_state["iteration"] >= 4:
            adjustment = "Near max iterations - focusing on synthesis"
        elif success_rate > 80:
            adjustment = "High success - continuing current approach"
        
        return {
            "success_rate": success_rate,
            "unique_actions_count": len(unique_actions),
            "adjustment": adjustment,
            "recommendation": "continue" if success_rate > 50 or len(unique_actions) < 5 else "consider_stopping"
        }
    
    def _synthesize_response(self, loop_state: Dict[str, Any]) -> str:
        """Synthesize final response from all loop iterations"""
        
        # Collect unique actions executed
        actions_executed = set()
        for result in loop_state["results"]:
            for r in result.get("results", []):
                actions_executed.add(r.get("action", "unknown"))
        
        synthesis_prompt = f"""
Synthesize a comprehensive response from this Loop Engineering session:

Original Request: {loop_state['context']}
Total Iterations: {loop_state['iteration']}
Goal Achieved: {loop_state['goal_achieved']}

Actions Executed: {', '.join(actions_executed)}

All Learnings:
{chr(10).join(loop_state['learnings'])}

Execution Summary:
- Total actions: {sum(r.get('actions_attempted', 0) for r in loop_state['results'])}
- Successful: {sum(r.get('successful', 0) for r in loop_state['results'])}
- Failed: {sum(r.get('failed', 0) for r in loop_state['results'])}

Create a final response that:
1. Summarizes what was accomplished
2. Highlights key findings
3. Provides actionable next steps
4. Is clear and helpful to the user

Return as a well-formatted response.
"""
        
        if self.client and OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a synthesis engine. Create clear, actionable summaries."},
                        {"role": "user", "content": synthesis_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"⚠️ Synthesis error: {e}")
        
        # Fallback synthesis with better formatting
        return f"""
🕷️ **E.V. Loop Engineering Complete**

**Original Request:** {loop_state['context'][:100]}

**Execution Summary:**
- Completed {loop_state['iteration']} iterations
- Actions used: {', '.join(actions_executed)}
- Success rate: {sum(r.get('successful', 0) for r in loop_state['results'])}/{sum(r.get('actions_attempted', 0) for r in loop_state['results'])}

**Key Learnings:**
{chr(10).join(f"• {l}" for l in loop_state['learnings'])}

**Next Steps:**
Based on the execution, you can now:
- Ask for more specific details about any action taken
- Request code generation or debugging
- Search for components or tutorials
- Plan the next phase of your project

Ready for your next command! 🚀
"""
    
    def chat(self):
        """Start interactive chat session"""
        print("\n" + "="*50)
        print(f"🕷️  {self.name} - Ready to assist!")
        print("="*50)
        print("Commands:")
        print("  - Just talk naturally")
        print("  - 'search <query>' - Search the web")
        print("  - 'plan <project>' - Plan a project")
        print("  - 'debug <file>' - Debug code")
        print("  - 'explain <file>' - Explain code")
        print("  - 'quit' - Exit")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n🤖 {self.name}: See you later! Keep building!")
                    break
                
                response = self.listen_and_respond(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n🤖 {self.name}: Goodbye!")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")


def main():
    """Main entry point"""
    ev = EV()
    ev.chat()


if __name__ == "__main__":
    main()
