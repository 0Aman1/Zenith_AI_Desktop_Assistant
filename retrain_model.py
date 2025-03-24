import os
import sys
import logging
from assistant.modules.nlp_learning import CommandLearner
from assistant.modules.speech_utils import speak

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('retrain.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Retrain the command classification model with updated categories"""
    try:
        print("Starting model retraining...")
        
        # Initialize the command learner
        learner = CommandLearner()
        
        # Retrain the model
        success = learner.train_model()
        
        if success:
            print("Model retrained successfully!")
            print("The model now supports the following categories:")
            for category in learner.valid_categories:
                print(f"- {category}")
        else:
            print("Model retraining failed. Check the logs for details.")
            
    except Exception as e:
        logger.error(f"Error in retraining: {e}")
        print(f"An error occurred: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 