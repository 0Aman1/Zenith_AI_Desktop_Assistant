from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import os
from config import HUGGINGFACE_API_KEY

# Set the Hugging Face API token
os.environ["HUGGINGFACE_TOKEN"] = HUGGINGFACE_API_KEY

class HuggingFaceHelper:
    def __init__(self):
        """Initialize the Hugging Face pipelines"""
        # Sentiment analysis for understanding user's emotion
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        # Text generation for natural responses
        self.text_generator = pipeline(
            "text-generation",
            model="gpt2"
        )
        
        # Question answering for specific queries
        self.qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2"
        )
        
        # Intent classification for better command understanding
        self.intent_classifier = pipeline(
            "text-classification",
            model="facebook/bart-large-mnli"
        )
    
    def analyze_sentiment(self, text):
        """Analyze the sentiment of user's input"""
        try:
            result = self.sentiment_analyzer(text)
            return {
                'sentiment': result[0]['label'],
                'score': result[0]['score']
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {'sentiment': 'neutral', 'score': 0.5}
    
    def generate_response(self, prompt, max_length=100):
        """Generate a natural language response"""
        try:
            response = self.text_generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                pad_token_id=self.text_generator.tokenizer.eos_token_id
            )
            return response[0]['generated_text']
        except Exception as e:
            print(f"Error in text generation: {e}")
            return prompt
    
    def answer_question(self, context, question):
        """Answer a specific question based on context"""
        try:
            result = self.qa_pipeline({
                'context': context,
                'question': question
            })
            return {
                'answer': result['answer'],
                'confidence': result['score']
            }
        except Exception as e:
            print(f"Error in question answering: {e}")
            return {'answer': "I'm not sure about that.", 'confidence': 0}
    
    def classify_intent(self, text, possible_intents):
        """Classify the intent of user's input"""
        try:
            # Create pairs of text with each possible intent
            pairs = [f"{text} </s></s> {intent}" for intent in possible_intents]
            results = self.intent_classifier(pairs)
            
            # Find the best matching intent
            best_score = 0
            best_intent = possible_intents[0]
            
            for i, result in enumerate(results):
                if result['label'] == 'ENTAILMENT' and result['score'] > best_score:
                    best_score = result['score']
                    best_intent = possible_intents[i]
            
            return {
                'intent': best_intent,
                'confidence': best_score
            }
        except Exception as e:
            print(f"Error in intent classification: {e}")
            return {'intent': 'unknown', 'confidence': 0}

# Example usage functions
def example_sentiment():
    """Example of sentiment analysis"""
    hf = HuggingFaceHelper()
    text = "I'm really happy with how this assistant is working!"
    result = hf.analyze_sentiment(text)
    print(f"Text: {text}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Confidence: {result['score']:.2f}")

def example_response():
    """Example of text generation"""
    hf = HuggingFaceHelper()
    prompt = "The AI assistant is designed to"
    response = hf.generate_response(prompt)
    print(f"Prompt: {prompt}")
    print(f"Generated Response: {response}")

def example_qa():
    """Example of question answering"""
    hf = HuggingFaceHelper()
    context = "The AI assistant can help with tasks like setting reminders, checking weather, and playing music."
    question = "What can the AI assistant do?"
    result = hf.answer_question(context, question)
    print(f"Question: {question}")
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.2f}")

def example_intent():
    """Example of intent classification"""
    hf = HuggingFaceHelper()
    text = "Can you play some music for me?"
    possible_intents = ['play_music', 'check_weather', 'set_reminder']
    result = hf.classify_intent(text, possible_intents)
    print(f"Text: {text}")
    print(f"Detected Intent: {result['intent']}")
    print(f"Confidence: {result['confidence']:.2f}")

if __name__ == "__main__":
    # Run examples
    print("\nTesting Sentiment Analysis:")
    example_sentiment()
    
    print("\nTesting Text Generation:")
    example_response()
    
    print("\nTesting Question Answering:")
    example_qa()
    
    print("\nTesting Intent Classification:")
    example_intent() 