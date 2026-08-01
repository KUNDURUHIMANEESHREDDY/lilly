#!/usr/bin/env python3
"""
E.V. Dynamic Decision Making Demo
Shows how E.V. decides actions at runtime instead of hardcoded routing
"""

from ev_assistant import EV
import json

def demo():
    print("=" * 60)
    print("🕷️  E.V. - Dynamic Decision Making Demo")
    print("=" * 60)
    
    ev = EV()
    
    test_cases = [
        "Hey E.V., how are you?",
        "Find me the best ultrasonic sensors for spider-sense",
        "I need to build web shooters with gesture control",
        "Plan a complete spider-sense project",
        "Write Arduino code for MPU6050 sensor",
        "Remember that I'm using ESP32 WROOM module",
        "What did I save about my microcontroller?",
        "Debug my code - it says pin not defined",
        "Explain how I2C communication works"
    ]
    
    print("\n" + "=" * 60)
    print("Testing Dynamic Decision Making")
    print("=" * 60)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {query}")
        print(f"{'='*60}")
        
        # Show what action E.V. decides to take
        action_data = ev._decide_action(query)
        
        print(f"\n🧠 DECISION:")
        if "action" in action_data:
            print(f"   Action: {action_data['action']}")
            print(f"   Parameters: {json.dumps(action_data.get('parameters', {}), indent=2)}")
        elif "response" in action_data:
            print(f"   Conversational response (no action needed)")
            print(f"   Response preview: {action_data['response'][:100]}...")
        
        # Execute the action
        result = ev._execute_action(action_data)
        
        print(f"\n✅ RESULT:")
        if isinstance(result, str):
            preview = result[:300] + "..." if len(result) > 300 else result
            print(f"   {preview}")
    
    print("\n" + "=" * 60)
    print("✨ Demo Complete!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("  ✓ Dynamic action selection at runtime")
    print("  ✓ No hardcoded if/else routing")
    print("  ✓ Context-aware decision making")
    print("  ✓ Multiple capability types")
    print("  ✓ Memory storage and recall")
    print("\nTo enable full LLM-powered decisions:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your OPENAI_API_KEY")
    print("  3. Run: python ev_assistant.py")
    print("=" * 60)

if __name__ == "__main__":
    demo()
