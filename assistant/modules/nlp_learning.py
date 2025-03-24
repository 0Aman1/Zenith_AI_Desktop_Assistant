import os
import json
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import spacy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandLearner:
    def __init__(self):
        # Initialize paths
        self.model_dir = "models"
        self.data_dir = "training_data"
        self.model_path = os.path.join(self.model_dir, "command_classifier.joblib")
        self.commands_path = os.path.join(self.data_dir, "command_dataset.json")
        self.new_commands_path = os.path.join(self.data_dir, "new_commands.json")
        
        # Create necessary directories
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
        
        # Initialize NLP components
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Load the command dataset
        self.command_dataset = self.load_command_dataset()
        
        # Initialize or load the model
        self.model = self.load_or_create_model()
        
        # Define valid categories
        self.valid_categories = [
            "system_control", 
            "web_search", 
            "system_info", 
            "media_control", 
            "audio_control",  # New category
            "video_control",  # New category
            "screenshot", 
            "weather", 
            "news"
        ]
        
        # Load spaCy model for better text understanding
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = spacy.load('en_core_web_sm')

    def preprocess_text(self, text):
        """Enhanced text preprocessing"""
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token.isalnum() and token not in self.stop_words]
        
        # Join tokens back into text
        return ' '.join(tokens)

    def load_command_dataset(self):
        """Load the pre-trained command dataset"""
        try:
            if os.path.exists(self.commands_path):
                with open(self.commands_path, 'r') as f:
                    return json.load(f)
            logger.warning(f"Command dataset not found at {self.commands_path}")
            return {'commands': [], 'categories': {}}
        except Exception as e:
            logger.error(f"Error loading command dataset: {e}")
            return {'commands': [], 'categories': {}}

    def load_new_commands(self):
        """Load new commands that need verification"""
        try:
            if os.path.exists(self.new_commands_path):
                with open(self.new_commands_path, 'r') as f:
                    return json.load(f)
            return {'commands': [], 'categories': {}}
        except Exception as e:
            logger.error(f"Error loading new commands: {e}")
            return {'commands': [], 'categories': {}}

    def save_new_commands(self, new_commands):
        """Save new commands for manual review"""
        try:
            with open(self.new_commands_path, 'w') as f:
                json.dump(new_commands, f, indent=4)
            logger.info("New commands saved for review")
        except Exception as e:
            logger.error(f"Error saving new commands: {e}")

    def load_or_create_model(self):
        """Load existing model or create a new one with improved architecture"""
        try:
            if os.path.exists(self.model_path):
                logger.info("Loading existing model")
                return joblib.load(self.model_path)
            
            logger.info("Creating new model")
            return Pipeline([
                ('tfidf', TfidfVectorizer(
                    preprocessor=self.preprocess_text,
                    ngram_range=(1, 3),  # Include up to trigrams for better phrase matching
                    max_features=10000,  # Increase features for better discrimination
                    min_df=2,  # Minimum document frequency
                    use_idf=True,
                    sublinear_tf=True  # Apply sublinear tf scaling
                )),
                ('clf', RandomForestClassifier(
                    n_estimators=200,  # More trees for better accuracy
                    max_depth=15,  # Deeper trees for more complex patterns
                    min_samples_split=4,  # Require more samples to split
                    class_weight='balanced',  # Handle class imbalance
                    random_state=42
                ))
            ])
        except Exception as e:
            logger.error(f"Error loading/creating model: {e}")
            return None

    def save_model(self):
        """Save the trained model"""
        try:
            joblib.dump(self.model, self.model_path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def add_command(self, command, category):
        """Add a new command to the review queue instead of training immediately"""
        try:
            if not command or not category:
                logger.warning("Invalid command or category")
                return False
                
            # Validate category
            if category not in self.valid_categories:
                logger.warning(f"Invalid category: {category}")
                return False
                
            # Load existing new commands
            new_commands = self.load_new_commands()
            
            # Add new command to review queue
            timestamp = datetime.now().isoformat()
            new_commands['commands'].append({
                'text': command,
                'category': category,
                'timestamp': timestamp
            })
            
            if category not in new_commands['categories']:
                new_commands['categories'][category] = []
            new_commands['categories'][category].append(command)
            
            # Save to new commands file
            self.save_new_commands(new_commands)
            
            logger.info(f"Added new command to review queue: {command} ({category})")
            return True
        except Exception as e:
            logger.error(f"Error adding command to review queue: {e}")
            return False

    def train_model(self):
        """Train the model with improved validation and error handling"""
        try:
            if not self.command_dataset['commands']:
                logger.warning("No commands available for training")
                return False
                
            X = [cmd['text'] for cmd in self.command_dataset['commands']]
            y = [cmd['category'] for cmd in self.command_dataset['commands']]
            
            # Split data for validation
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            report = classification_report(y_test, y_pred)
            logger.info(f"Model evaluation:\n{report}")
            
            self.save_model()
            return True
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False

    def predict_category(self, command):
        """Predict category using only pre-trained data"""
        try:
            if not self.command_dataset['commands']:
                logger.warning("No training data available")
                return None
                
            # Use spaCy for entity recognition
            doc = self.nlp(command)
            entities = {ent.text: ent.label_ for ent in doc.ents}
            
            # Special handling for media commands
            command_lower = command.lower()
            
            # Media control commands
            if any(word in command_lower for word in ["pause", "stop", "next", "previous", "volume", "mute", "unmute", "louder", "quieter"]):
                logger.info(f"Direct category assignment: media_control for '{command}'")
                return "media_control"
            
            # File extension checks (high priority)
            # Video file extensions
            if any(ext in command_lower for ext in ["mp4", "avi", "mkv", "mov", "wmv", "flv"]):
                logger.info(f"Direct category assignment: video_control for '{command}'")
                return "video_control"
            
            # Audio file extensions
            if any(ext in command_lower for ext in ["mp3", "wav", "m4a", "flac", "ogg", "aac"]):
                logger.info(f"Direct category assignment: audio_control for '{command}'")
                return "audio_control"
            
            # Direct category assignment for clear media commands
            # Video commands
            if any(phrase in command_lower for phrase in ["play video", "watch video", "play movie", "watch movie", "start video"]) or \
               "video" in command_lower or "movie" in command_lower or "film" in command_lower or \
               (("watch" in command_lower or "view" in command_lower) and 
                not any(word in command_lower for word in ["news", "weather"])):
                logger.info(f"Direct category assignment: video_control for '{command}'")
                return "video_control"
            
            # Audio commands    
            if any(phrase in command_lower for phrase in ["play music", "play song", "play audio", "listen to music", "start music"]) or \
               "music" in command_lower or "song" in command_lower or "audio" in command_lower or \
               any(word in command_lower for word in ["tune", "melody", "track", "playlist", "listen"]):
                logger.info(f"Direct category assignment: audio_control for '{command}'")
                return "audio_control"
            
            # Make prediction with confidence score
            prediction = self.model.predict([command])[0]
            probabilities = self.model.predict_proba([command])[0]
            confidence = np.max(probabilities)
            
            # Log prediction details
            logger.info(f"Command: {command}")
            logger.info(f"Predicted category: {prediction}")
            logger.info(f"Confidence: {confidence:.2f}")
            
            # Return None if confidence is too low (lowered threshold)
            if confidence < 0.3:  # Decreased from 0.6 to 0.3
                logger.warning("Low confidence prediction")
                return None
                
            return prediction
        except Exception as e:
            logger.error(f"Error predicting category: {e}")
            return None

    def get_similar_commands(self, command, category=None):
        """Get similar commands from history with improved similarity scoring"""
        try:
            if not self.command_dataset['commands']:
                return []
                
            if category and category in self.command_dataset['categories']:
                commands = self.command_dataset['categories'][category]
            else:
                commands = [cmd['text'] for cmd in self.command_dataset['commands']]
                
            # Use spaCy for similarity comparison
            doc1 = self.nlp(command)
            similarities = []
            
            for cmd in commands:
                doc2 = self.nlp(cmd)
                similarity = doc1.similarity(doc2)
                similarities.append((cmd, similarity))
                
            # Return top 3 most similar commands
            return sorted(similarities, key=lambda x: x[1], reverse=True)[:3]
        except Exception as e:
            logger.error(f"Error finding similar commands: {e}")
            return []

    def get_command_suggestions(self, partial_command):
        """Get command suggestions based on partial input with fuzzy matching"""
        try:
            if not self.command_dataset['commands']:
                return []
                
            all_commands = [cmd['text'] for cmd in self.command_dataset['commands']]
            suggestions = []
            
            # Convert to lowercase for case-insensitive matching
            partial_command = partial_command.lower()
            
            for cmd in all_commands:
                cmd_lower = cmd.lower()
                if cmd_lower.startswith(partial_command):
                    suggestions.append(cmd)
                elif partial_command in cmd_lower:
                    suggestions.append(cmd)
                    
            return suggestions[:5]  # Return top 5 suggestions
        except Exception as e:
            logger.error(f"Error getting command suggestions: {e}")
            return []

    def update_model(self):
        """Manual method to update the model with verified commands"""
        try:
            # Load new verified commands
            new_commands = self.load_new_commands()
            
            if not new_commands['commands']:
                logger.info("No new commands to verify")
                return False
            
            # Add verified commands to the main dataset
            self.command_dataset['commands'].extend(new_commands['commands'])
            
            # Update categories
            for category, commands in new_commands['categories'].items():
                if category not in self.command_dataset['categories']:
                    self.command_dataset['categories'][category] = []
                self.command_dataset['categories'][category].extend(commands)
            
            # Save updated dataset
            with open(self.commands_path, 'w') as f:
                json.dump(self.command_dataset, f, indent=4)
            
            # Train model with updated data
            self.train_model()
            
            # Clear new commands file
            self.save_new_commands({'commands': [], 'categories': {}})
            
            logger.info("Model updated with verified commands")
            return True
        except Exception as e:
            logger.error(f"Error updating model: {e}")
            return False 