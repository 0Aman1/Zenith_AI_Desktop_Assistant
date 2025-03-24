import os
import sys
import logging
import json
from assistant.modules.nlp_learning import CommandLearner
from run import get_command_category, process_command
from assistant.modules.advanced_features import AdvancedFeatures

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_command_classification():
    """Comprehensive test of command classification with a wide range of commands"""
    # Initialize components
    command_learner = CommandLearner()
    advanced_features = AdvancedFeatures()
    
    # Test commands for all categories
    test_commands = {
        "screenshot": [
            "take a screenshot",
            "capture my screen",
            "screenshot now",
            "take a picture of my screen",
            "save my screen",
            "grab a screenshot",
            "capture screen",
            "take screenshot",
            "I need a screenshot",
            "can you take a screenshot for me"
        ],
        "system_info": [
            "show system info",
            "what's my cpu usage",
            "show memory status",
            "check disk space",
            "how much memory am I using",
            "tell me about my system",
            "is my cpu running hot",
            "check system resources"
        ],
        "web_search": [
            "search for python tutorials",
            "google the weather in New York",
            "look up recipe for chocolate cake",
            "find information about AI",
            "youtube funny cat videos",
            "search the web for news"
        ],
        "media_control": [
            "play music",
            "pause the song",
            "next track please",
            "volume up",
            "mute the audio",
            "previous song"
        ],
        "system_control": [
            "open notepad",
            "start chrome browser",
            "launch calculator",
            "close the current window",
            "restart my computer",
            "open file explorer"
        ]
    }
    
    # Results tracking
    results = {
        "total": 0,
        "correct": 0,
        "by_category": {}
    }
    
    # Test each category
    for category, commands in test_commands.items():
        print(f"\n===== TESTING {category.upper()} COMMANDS =====")
        
        category_results = {
            "total": len(commands),
            "correct": 0,
            "accuracy": 0
        }
        
        for command in commands:
            rule_category = get_command_category(command)
            ml_category = command_learner.predict_category(command)
            
            # Determine final category using the same logic as in process_command
            if rule_category in ["web_search", "system_control", "media_control", "screenshot", "system_info"]:
                final_category = rule_category
                method = "rule-based"
            else:
                final_category = ml_category if ml_category else rule_category
                method = "ML-based" if ml_category else "rule-based (fallback)"
            
            print(f"\nCommand: '{command}'")
            print(f"Rule-based category: {rule_category}")
            print(f"ML-based category: {ml_category}")
            print(f"Final category: {final_category} (using {method})")
            
            # Check if the classification is correct
            is_correct = final_category == category
            print(f"Correct classification: {'✓' if is_correct else '✗'}")
            
            # Update results
            results["total"] += 1
            if is_correct:
                results["correct"] += 1
                category_results["correct"] += 1
        
        # Calculate category accuracy
        category_results["accuracy"] = category_results["correct"] / category_results["total"] * 100
        results["by_category"][category] = category_results
        
        print(f"\nCategory {category} accuracy: {category_results['accuracy']:.2f}%")
    
    # Calculate overall accuracy
    results["accuracy"] = results["correct"] / results["total"] * 100
    
    # Print summary
    print("\n===== OVERALL RESULTS =====")
    print(f"Total commands tested: {results['total']}")
    print(f"Correctly classified: {results['correct']}")
    print(f"Overall accuracy: {results['accuracy']:.2f}%")
    print("\nAccuracy by category:")
    
    for category, cat_results in results["by_category"].items():
        print(f"  {category}: {cat_results['accuracy']:.2f}% ({cat_results['correct']}/{cat_results['total']})")
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("\nResults saved to test_results.json")

if __name__ == "__main__":
    test_command_classification() 