import os
import sys
import logging
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
    """Test command classification with various screenshot commands"""
    # Initialize components
    command_learner = CommandLearner()
    advanced_features = AdvancedFeatures()
    
    # Test commands
    screenshot_commands = [
        "take a screenshot",
        "capture my screen",
        "screenshot now",
        "take a picture of my screen",
        "save my screen",
        "grab a screenshot",
        "capture screen",
        "take screenshot"
    ]
    
    system_info_commands = [
        "show system info",
        "what's my cpu usage",
        "show memory status",
        "check disk space"
    ]
    
    print("\n===== TESTING SCREENSHOT COMMANDS =====")
    for command in screenshot_commands:
        rule_category = get_command_category(command)
        ml_category = command_learner.predict_category(command)
        
        # Determine final category using the same logic as in process_command
        if rule_category in ["web_search", "system_control", "media_control", "screenshot", "system_info"]:
            category = rule_category
            method = "rule-based"
        else:
            category = ml_category if ml_category else rule_category
            method = "ML-based" if ml_category else "rule-based (fallback)"
        
        print(f"\nCommand: '{command}'")
        print(f"Rule-based category: {rule_category}")
        print(f"ML-based category: {ml_category}")
        print(f"Final category: {category} (using {method})")
        
        # Check if the classification is correct
        is_correct = category == "screenshot"
        print(f"Correct classification: {'✓' if is_correct else '✗'}")
    
    print("\n===== TESTING SYSTEM INFO COMMANDS =====")
    for command in system_info_commands:
        rule_category = get_command_category(command)
        ml_category = command_learner.predict_category(command)
        
        # Determine final category using the same logic as in process_command
        if rule_category in ["web_search", "system_control", "media_control", "screenshot", "system_info"]:
            category = rule_category
            method = "rule-based"
        else:
            category = ml_category if ml_category else rule_category
            method = "ML-based" if ml_category else "rule-based (fallback)"
        
        print(f"\nCommand: '{command}'")
        print(f"Rule-based category: {rule_category}")
        print(f"ML-based category: {ml_category}")
        print(f"Final category: {category} (using {method})")
        
        # Check if the classification is correct
        is_correct = category == "system_info"
        print(f"Correct classification: {'✓' if is_correct else '✗'}")

if __name__ == "__main__":
    test_command_classification() 