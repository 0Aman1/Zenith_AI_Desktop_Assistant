"""
AI Orchestrator for managing all AI features seamlessly
"""
import threading
from queue import Queue
import logging
from typing import Dict, Any, Optional
from .huggingface_utils import HuggingFaceHelper
from .nlp_learning import CommandLearner

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        """Initialize AI components with background processing"""
        self.hf_helper = HuggingFaceHelper()
        self.command_learner = CommandLearner()
        
        # Queue for background processing
        self.ai_queue = Queue()
        self.results_cache: Dict[str, Any] = {}
        
        # Start background processing thread
        self.bg_thread = threading.Thread(target=self._process_ai_queue, daemon=True)
        self.bg_thread.start()
        
        # Context memory for better conversation flow
        self.context_memory = []
        self.max_context_items = 5
    
    def _process_ai_queue(self):
        """Background thread for processing AI tasks"""
        while True:
            try:
                task = self.ai_queue.get()
                if task is None:
                    break
                    
                task_type, data = task
                result = None
                
                if task_type == "sentiment":
                    result = self.hf_helper.analyze_sentiment(data)
                elif task_type == "intent":
                    result = self.hf_helper.classify_intent(data["text"], data["intents"])
                elif task_type == "qa":
                    result = self.hf_helper.answer_question(data["context"], data["question"])
                elif task_type == "generate":
                    result = self.hf_helper.generate_response(data)
                
                if result:
                    self.results_cache[f"{task_type}_{data}"] = result
                
            except Exception as e:
                logger.error(f"Error in AI background processing: {e}")
            finally:
                self.ai_queue.task_done()
    
    def add_to_context(self, item: Dict[str, Any]):
        """Add item to context memory"""
        self.context_memory.append(item)
        if len(self.context_memory) > self.max_context_items:
            self.context_memory.pop(0)
    
    def get_context(self) -> str:
        """Get formatted context string"""
        return "\n".join([
            f"User: {item['user']}\nAssistant: {item['assistant']}"
            for item in self.context_memory
        ])
    
    def preprocess_command(self, command: str) -> Dict[str, Any]:
        """Preprocess command with sentiment and intent analysis"""
        # Queue sentiment analysis
        self.ai_queue.put(("sentiment", command))
        
        # Get intent classification
        intents = ['media_control', 'system_control', 'web_search', 'info_request']
        self.ai_queue.put(("intent", {"text": command, "intents": intents}))
        
        # Add command to context
        self.add_to_context({"user": command, "assistant": None})
        
        # Return immediate basic analysis
        return {
            "command": command,
            "category": self.command_learner.predict_category(command),
            "context": self.get_context()
        }
    
    def generate_response(self, command: str, context: Optional[str] = None) -> str:
        """Generate natural language response"""
        if context:
            prompt = f"Context: {context}\nUser: {command}\nAssistant:"
        else:
            prompt = f"User: {command}\nAssistant:"
            
        self.ai_queue.put(("generate", prompt))
        
        # Return immediate response while background processing continues
        return self.hf_helper.generate_response(prompt, max_length=50)
    
    def answer_question(self, question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Answer questions using context"""
        if not context:
            context = self.get_context()
            
        self.ai_queue.put(("qa", {"context": context, "question": question}))
        
        # Get immediate answer
        result = self.hf_helper.answer_question(context, question)
        self.add_to_context({"user": question, "assistant": result["answer"]})
        return result
    
    def enhance_command(self, command: str, category: str) -> Dict[str, Any]:
        """Enhance command understanding with AI"""
        # Get sentiment to adjust response style
        sentiment = self.hf_helper.analyze_sentiment(command)
        
        # Generate natural response
        response = self.generate_response(command)
        
        # Add to learning system
        self.command_learner.add_command(command, category)
        
        return {
            "command": command,
            "category": category,
            "sentiment": sentiment,
            "response": response,
            "context": self.get_context()
        }
    
    def cleanup(self):
        """Clean up AI resources"""
        try:
            # Signal background thread to stop
            self.ai_queue.put(None)
            self.bg_thread.join(timeout=1)
            
            # Clear caches
            self.results_cache.clear()
            self.context_memory.clear()
            
        except Exception as e:
            logger.error(f"Error during AI cleanup: {e}") 