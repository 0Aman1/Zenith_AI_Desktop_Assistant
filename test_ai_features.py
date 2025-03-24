"""
from assistant.modules.huggingface_utils import HuggingFaceHelper
from assistant.modules.nlp_learning import CommandLearner
import time

def test_sentiment_analysis(hf):
    print('\n=== Testing Sentiment Analysis ===')
    test_texts = [
        'I am really happy with this assistant!',
        'This is frustrating and not working.',
        'The weather is nice today.',
        'I hate when things break.',
        'This is amazing and wonderful!'
    ]
    
    for text in test_texts:
        result = hf.analyze_sentiment(text)
        print(f'\nText: {text}')
        print(f'Sentiment: {result["sentiment"]}')
        print(f'Confidence: {result["score"]:.2f}')

def test_text_generation(hf):
    print('\n=== Testing Text Generation ===')
    prompts = [
        'The AI assistant can help you',
        'In the future, AI will',
        'The best feature of this system is'
    ]
    
    for prompt in prompts:
        print(f'\nPrompt: {prompt}')
        response = hf.generate_response(prompt, max_length=50)
        print(f'Generated: {response}')

def test_question_answering(hf):
    print('\n=== Testing Question Answering ===')
    context = '''
    The AI Desktop Assistant is a powerful tool that can help with various tasks.
    It can control media playback, search the web, take screenshots, and manage system operations.
    The assistant uses advanced AI features like sentiment analysis and natural language processing.
    It can also check weather, read news, and learn from user interactions.
    '''
    
    questions = [
        'What can the assistant do?',
        'What AI features does it use?',
        'Can it control media?',
        'How does it learn?'
    ]
    
    for question in questions:
        result = hf.answer_question(context, question)
        print(f'\nQuestion: {question}')
        print(f'Answer: {result["answer"]}')
        print(f'Confidence: {result["confidence"]:.2f}')

def test_intent_classification(hf):
    print('\n=== Testing Intent Classification ===')
    test_commands = [
        'Can you play some music for me?',
        'What\'s the weather like today?',
        'Open Chrome browser',
        'Search for Python tutorials',
        'Take a screenshot of my screen'
    ]
    
    possible_intents = [
        'play_music',
        'check_weather',
        'system_control',
        'web_search',
        'screenshot'
    ]
    
    for command in test_commands:
        result = hf.classify_intent(command, possible_intents)
        print(f'\nCommand: {command}')
        print(f'Detected Intent: {result["intent"]}')
        print(f'Confidence: {result["confidence"]:.2f}')

def test_command_learning(cl):
    print('\n=== Testing Command Learning ===')
    test_commands = [
        ('play some rock music', 'media_control'),
        ('what\'s the CPU usage', 'system_info'),
        ('search for cat videos', 'web_search'),
        ('take a screenshot', 'screenshot'),
        ('check weather in London', 'weather')
    ]
    
    print('Adding new commands to learn...')
    for command, category in test_commands:
        success = cl.add_command(command, category)
        print(f'Added "{command}" ({category}): {"Success" if success else "Failed"}')
    
    print('\nTesting prediction...')
    test_inputs = [
        'play jazz music',
        'show me system info',
        'search for dog videos',
        'capture my screen',
        'weather in New York'
    ]
    
    for command in test_inputs:
        category = cl.predict_category(command)
        print(f'\nInput: {command}')
        print(f'Predicted Category: {category}')

def main():
    print('Initializing AI components...')
    hf = HuggingFaceHelper()
    cl = CommandLearner()
    
    # Run tests
    test_sentiment_analysis(hf)
    time.sleep(1)  # Brief pause between tests
    
    test_text_generation(hf)
    time.sleep(1)
    
    test_question_answering(hf)
    time.sleep(1)
    
    test_intent_classification(hf)
    time.sleep(1)
    
    test_command_learning(cl)

if __name__ == '__main__':
    main()
""" 