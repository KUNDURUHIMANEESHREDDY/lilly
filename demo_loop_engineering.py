"""
Loop Engineering Demo for E.V. AI Assistant

Demonstrates the continuous adaptive execution loop:
EVALUATE → DECIDE → EXECUTE → LEARN → ADAPT
"""

from ev_assistant import EV


def demo_loop_engineering():
    """Showcase Loop Engineering in action"""
    
    print("="*60)
    print("🕷️  E.V. LOOP ENGINEERING DEMO")
    print("="*60)
    print()
    print("Loop Engineering is a dynamic decision-making framework where:")
    print("  1. EVALUATE - Analyze current state and progress")
    print("  2. DECIDE - Choose next actions based on context + learnings")
    print("  3. EXECUTE - Run actions and capture detailed results")
    print("  4. LEARN - Extract insights from execution")
    print("  5. ADAPT - Adjust strategy based on success/failure patterns")
    print()
    print("This runs for multiple iterations until goal is achieved!")
    print("="*60)
    print()
    
    # Initialize E.V.
    ev = EV()
    
    # Test queries that will trigger multi-iteration loops
    test_queries = [
        "Plan a web shooter project with ESP32 and sensors",
        "Search for ultrasonic sensors and create a spider-sense prototype"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"TEST QUERY {i}: {query}")
        print('='*60)
        
        response = ev._process_query(query)
        
        print(f"\n📝 FINAL RESPONSE:")
        print(response[:500] + "..." if len(response) > 500 else response)
        print()
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60)
    print()
    print("Key features demonstrated:")
    print("  ✓ Multi-iteration execution (up to 5 loops)")
    print("  ✓ Dynamic decision making at runtime")
    print("  ✓ Learning from each iteration")
    print("  ✓ Context evolution based on results")
    print("  ✓ Strategy adaptation based on success rates")
    print("  ✓ Synthesized final responses")
    print()
    print("To use with full LLM capabilities:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your OPENAI_API_KEY")
    print("  3. Run: python ev_assistant.py")
    print()


if __name__ == "__main__":
    demo_loop_engineering()
