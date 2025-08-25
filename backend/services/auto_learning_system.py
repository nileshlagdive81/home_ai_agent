import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import sqlite3
import threading
from collections import defaultdict, Counter

@dataclass
class UserInteraction:
    """User interaction record"""
    timestamp: float
    user_input: str
    intent_classified: str
    confidence: float
    entities_extracted: Dict[str, Any]
    response_given: str
    user_feedback: Optional[str] = None
    correction_made: Optional[str] = None
    session_id: Optional[str] = None

@dataclass
class LearningPattern:
    """Pattern learned from user interactions"""
    pattern: str
    intent: str
    confidence: float
    frequency: int
    last_seen: float
    entities: List[str]
    variations: List[str]

@dataclass
class UserPreference:
    """User preference learned from interactions"""
    user_id: str
    preferred_intents: List[str]
    preferred_locations: List[str]
    preferred_property_types: List[str]
    preferred_price_ranges: List[str]
    common_queries: List[str]
    last_updated: float

class AutoLearningSystem:
    """System for automatically learning from user interactions"""
    
    def __init__(self, db_path: str = "auto_learning.db"):
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path
        self.lock = threading.Lock()
        self._initialize_database()
        
        # Learning thresholds
        self.min_frequency_for_pattern = 3
        self.min_confidence_for_learning = 0.7
        self.max_patterns_per_intent = 50
        self.learning_cooldown = 3600  # 1 hour
        
        # Cached data
        self._cached_patterns = None
        self._cached_preferences = None
        self._last_cache_update = 0
    
    def _initialize_database(self):
        """Initialize SQLite database for storing learning data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # User interactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL NOT NULL,
                        user_input TEXT NOT NULL,
                        intent_classified TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        entities_extracted TEXT NOT NULL,
                        response_given TEXT NOT NULL,
                        user_feedback TEXT,
                        correction_made TEXT,
                        session_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Learned patterns table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS learned_patterns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pattern TEXT NOT NULL,
                        intent TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        frequency INTEGER DEFAULT 1,
                        last_seen REAL NOT NULL,
                        entities TEXT NOT NULL,
                        variations TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # User preferences table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT UNIQUE NOT NULL,
                        preferred_intents TEXT NOT NULL,
                        preferred_locations TEXT NOT NULL,
                        preferred_property_types TEXT NOT NULL,
                        preferred_price_ranges TEXT NOT NULL,
                        common_queries TEXT NOT NULL,
                        last_updated REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_timestamp ON user_interactions(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_intent ON user_interactions(intent_classified)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_patterns_intent ON learned_patterns(intent)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_preferences_user ON user_preferences(user_id)")
                
                conn.commit()
                self.logger.info("Auto-learning database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    def record_interaction(self, interaction: UserInteraction):
        """Record a user interaction for learning"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO user_interactions 
                    (timestamp, user_input, intent_classified, confidence, entities_extracted, 
                     response_given, user_feedback, correction_made, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    interaction.timestamp,
                    interaction.user_input,
                    interaction.intent_classified,
                    interaction.confidence,
                    json.dumps(interaction.entities_extracted),
                    interaction.response_given,
                    interaction.user_feedback,
                    interaction.correction_made,
                    interaction.session_id
                ))
                
                conn.commit()
                
                # Trigger learning if enough time has passed
                if time.time() - self._last_cache_update > self.learning_cooldown:
                    self._trigger_learning()
                
        except Exception as e:
            self.logger.error(f"Error recording interaction: {e}")
    
    def _trigger_learning(self):
        """Trigger the learning process"""
        try:
            self.logger.info("Triggering auto-learning process")
            
            # Learn new patterns
            self._learn_new_patterns()
            
            # Update user preferences
            self._update_user_preferences()
            
            # Update cache
            self._update_cache()
            
            self._last_cache_update = time.time()
            
        except Exception as e:
            self.logger.error(f"Error in learning process: {e}")
    
    def _learn_new_patterns(self):
        """Learn new patterns from user interactions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get recent interactions with high confidence
                cursor.execute("""
                    SELECT user_input, intent_classified, confidence, entities_extracted
                    FROM user_interactions 
                    WHERE confidence >= ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """, (self.min_confidence_for_learning, time.time() - 86400))  # Last 24 hours
                
                interactions = cursor.fetchall()
                
                # Group by intent
                intent_groups = defaultdict(list)
                for user_input, intent, confidence, entities in interactions:
                    intent_groups[intent].append((user_input, confidence, entities))
                
                # Learn patterns for each intent
                for intent, group in intent_groups.items():
                    self._learn_patterns_for_intent(intent, group)
                    
        except Exception as e:
            self.logger.error(f"Error learning new patterns: {e}")
    
    def _learn_patterns_for_intent(self, intent: str, interactions: List[Tuple[str, float, str]]):
        """Learn patterns for a specific intent"""
        try:
            # Extract common patterns
            patterns = self._extract_patterns_from_interactions(interactions)
            
            # Update or create learned patterns
            for pattern, confidence, entities in patterns:
                self._update_learned_pattern(intent, pattern, confidence, entities)
                
        except Exception as e:
            self.logger.error(f"Error learning patterns for intent {intent}: {e}")
    
    def _extract_patterns_from_interactions(self, interactions: List[Tuple[str, float, str]]) -> List[Tuple[str, float, List[str]]]:
        """Extract patterns from user interactions"""
        patterns = []
        
        # Group similar inputs
        input_groups = defaultdict(list)
        for user_input, confidence, entities in interactions:
            # Normalize input (remove specific values, keep structure)
            normalized = self._normalize_input(user_input)
            input_groups[normalized].append((user_input, confidence, entities))
        
        # Find patterns with sufficient frequency
        for normalized, group in input_groups.items():
            if len(group) >= self.min_frequency_for_pattern:
                # Calculate average confidence
                avg_confidence = sum(conf for _, conf, _ in group) / len(group)
                
                # Extract common entities
                common_entities = self._extract_common_entities(group)
                
                patterns.append((normalized, avg_confidence, common_entities))
        
        return patterns
    
    def _normalize_input(self, user_input: str) -> str:
        """Normalize user input to extract pattern structure"""
        # Replace specific values with placeholders
        normalized = user_input.lower()
        
        # Replace locations with [LOCATION]
        pune_locations = [
            "viman nagar", "kharadi", "hadapsar", "magarpatta", "wagholi", "lonikand",
            "koregaon park", "boat club", "model colony", "aundh", "baner", "balewadi",
            "kalyani nagar", "yerwada", "lohegaon", "chandannagar", "hinjewadi", "wakad",
            "pashan", "sus", "camp", "deccan", "fc road", "jm road", "shivajinagar"
        ]
        
        for location in pune_locations:
            normalized = normalized.replace(location, "[LOCATION]")
        
        # Replace property types with [PROPERTY_TYPE]
        property_types = ["1bhk", "2bhk", "3bhk", "villa", "apartment", "plot", "flat", "house"]
        for prop_type in property_types:
            normalized = normalized.replace(prop_type, "[PROPERTY_TYPE]")
        
        # Replace price indicators with [PRICE_RANGE]
        price_indicators = ["affordable", "budget", "cheap", "luxury", "premium", "expensive"]
        for indicator in price_indicators:
            normalized = normalized.replace(indicator, "[PRICE_RANGE]")
        
        # Replace amounts with [AMOUNT]
        import re
        normalized = re.sub(r'₹?\d+[LCR]?', '[AMOUNT]', normalized)
        
        return normalized.strip()
    
    def _extract_common_entities(self, group: List[Tuple[str, float, str]]) -> List[str]:
        """Extract common entities from a group of interactions"""
        entity_counts = Counter()
        
        for _, _, entities_str in group:
            try:
                entities = json.loads(entities_str)
                for entity_type, entity_value in entities.items():
                    if entity_value:
                        entity_counts[f"{entity_type}:{entity_value}"] += 1
            except:
                continue
        
        # Return entities that appear in at least half of the interactions
        threshold = len(group) / 2
        return [entity for entity, count in entity_counts.items() if count >= threshold]
    
    def _update_learned_pattern(self, intent: str, pattern: str, confidence: float, entities: List[str]):
        """Update or create a learned pattern"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if pattern already exists
                cursor.execute("""
                    SELECT id, frequency, confidence FROM learned_patterns 
                    WHERE pattern = ? AND intent = ?
                """, (pattern, intent))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing pattern
                    pattern_id, current_freq, current_conf = existing
                    new_freq = current_freq + 1
                    new_conf = (current_conf + confidence) / 2  # Average confidence
                    
                    cursor.execute("""
                        UPDATE learned_patterns 
                        SET frequency = ?, confidence = ?, last_seen = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (new_freq, new_conf, time.time(), pattern_id))
                    
                else:
                    # Create new pattern
                    cursor.execute("""
                        INSERT INTO learned_patterns 
                        (pattern, intent, confidence, frequency, last_seen, entities, variations)
                        VALUES (?, ?, ?, 1, ?, ?, ?)
                    """, (pattern, intent, confidence, time.time(), json.dumps(entities), json.dumps([])))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error updating learned pattern: {e}")
    
    def _update_user_preferences(self):
        """Update user preferences based on interactions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get unique users from recent interactions
                cursor.execute("""
                    SELECT DISTINCT session_id FROM user_interactions 
                    WHERE session_id IS NOT NULL AND timestamp >= ?
                """, (time.time() - 604800))  # Last 7 days
                
                user_sessions = cursor.fetchall()
                
                for (session_id,) in user_sessions:
                    if session_id:
                        self._update_preferences_for_user(session_id)
                        
        except Exception as e:
            self.logger.error(f"Error updating user preferences: {e}")
    
    def _update_preferences_for_user(self, session_id: str):
        """Update preferences for a specific user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user's recent interactions
                cursor.execute("""
                    SELECT intent_classified, entities_extracted, user_input
                    FROM user_interactions 
                    WHERE session_id = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """, (session_id, time.time() - 604800))  # Last 7 days
                
                interactions = cursor.fetchall()
                
                if not interactions:
                    return
                
                # Analyze preferences
                intents = Counter()
                locations = Counter()
                property_types = Counter()
                price_ranges = Counter()
                queries = Counter()
                
                for intent, entities_str, user_input in interactions:
                    intents[intent] += 1
                    queries[user_input] += 1
                    
                    try:
                        entities = json.loads(entities_str)
                        if entities.get("location"):
                            locations[entities["location"]] += 1
                        if entities.get("property_type"):
                            property_types[entities["property_type"]] += 1
                        if entities.get("price_range"):
                            price_ranges[entities["price_range"]] += 1
                    except:
                        continue
                
                # Create preference object
                preference = UserPreference(
                    user_id=session_id,
                    preferred_intents=[intent for intent, _ in intents.most_common(5)],
                    preferred_locations=[loc for loc, _ in locations.most_common(5)],
                    preferred_property_types=[prop for prop, _ in property_types.most_common(5)],
                    preferred_price_ranges=[price for price, _ in price_ranges.most_common(5)],
                    common_queries=[query for query, _ in queries.most_common(10)],
                    last_updated=time.time()
                )
                
                # Update database
                self._save_user_preference(preference)
                
        except Exception as e:
            self.logger.error(f"Error updating preferences for user {session_id}: {e}")
    
    def _save_user_preference(self, preference: UserPreference):
        """Save user preference to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences 
                    (user_id, preferred_intents, preferred_locations, preferred_property_types, 
                     preferred_price_ranges, common_queries, last_updated, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    preference.user_id,
                    json.dumps(preference.preferred_intents),
                    json.dumps(preference.preferred_locations),
                    json.dumps(preference.preferred_property_types),
                    json.dumps(preference.preferred_price_ranges),
                    json.dumps(preference.common_queries),
                    preference.last_updated
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error saving user preference: {e}")
    
    def _update_cache(self):
        """Update cached data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Cache learned patterns
                cursor.execute("""
                    SELECT pattern, intent, confidence, frequency, entities, variations
                    FROM learned_patterns 
                    ORDER BY frequency DESC, confidence DESC
                """)
                
                self._cached_patterns = []
                for row in cursor.fetchall():
                    pattern, intent, confidence, frequency, entities, variations = row
                    self._cached_patterns.append(LearningPattern(
                        pattern=pattern,
                        intent=intent,
                        confidence=confidence,
                        frequency=frequency,
                        last_seen=time.time(),
                        entities=json.loads(entities) if entities else [],
                        variations=json.loads(variations) if variations else []
                    ))
                
                # Cache user preferences
                cursor.execute("""
                    SELECT user_id, preferred_intents, preferred_locations, preferred_property_types,
                           preferred_price_ranges, common_queries, last_updated
                    FROM user_preferences
                """)
                
                self._cached_preferences = {}
                for row in cursor.fetchall():
                    user_id, intents, locations, prop_types, price_ranges, queries, last_updated = row
                    self._cached_preferences[user_id] = UserPreference(
                        user_id=user_id,
                        preferred_intents=json.loads(intents) if intents else [],
                        preferred_locations=json.loads(locations) if locations else [],
                        preferred_property_types=json.loads(prop_types) if prop_types else [],
                        preferred_price_ranges=json.loads(price_ranges) if price_ranges else [],
                        common_queries=json.loads(queries) if queries else [],
                        last_updated=last_updated
                    )
                
                self.logger.info(f"Cache updated: {len(self._cached_patterns)} patterns, {len(self._cached_preferences)} users")
                
        except Exception as e:
            self.logger.error(f"Error updating cache: {e}")
    
    def get_learned_patterns(self, intent: Optional[str] = None) -> List[LearningPattern]:
        """Get learned patterns, optionally filtered by intent"""
        if not self._cached_patterns:
            self._update_cache()
        
        if intent:
            return [p for p in self._cached_patterns if p.intent == intent]
        
        return self._cached_patterns
    
    def get_user_preferences(self, user_id: str) -> Optional[UserPreference]:
        """Get preferences for a specific user"""
        if not self._cached_preferences:
            self._update_cache()
        
        return self._cached_preferences.get(user_id)
    
    def get_popular_patterns(self, limit: int = 10) -> List[LearningPattern]:
        """Get most popular patterns across all intents"""
        if not self._cached_patterns:
            self._update_cache()
        
        # Sort by frequency and confidence
        sorted_patterns = sorted(
            self._cached_patterns,
            key=lambda p: (p.frequency, p.confidence),
            reverse=True
        )
        
        return sorted_patterns[:limit]
    
    def export_learning_data(self, filepath: str):
        """Export learning data to JSON file"""
        try:
            export_data = {
                "learned_patterns": [asdict(pattern) for pattern in self.get_learned_patterns()],
                "user_preferences": [asdict(pref) for pref in self._cached_preferences.values()],
                "export_timestamp": time.time(),
                "total_patterns": len(self._cached_patterns),
                "total_users": len(self._cached_preferences)
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Learning data exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error exporting learning data: {e}")
            raise
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get statistics about the learning system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total interactions
                cursor.execute("SELECT COUNT(*) FROM user_interactions")
                total_interactions = cursor.fetchone()[0]
                
                # Recent interactions (last 24 hours)
                cursor.execute("SELECT COUNT(*) FROM user_interactions WHERE timestamp >= ?", 
                             (time.time() - 86400,))
                recent_interactions = cursor.fetchone()[0]
                
                # Total patterns
                cursor.execute("SELECT COUNT(*) FROM learned_patterns")
                total_patterns = cursor.fetchone()[0]
                
                # Total users
                cursor.execute("SELECT COUNT(*) FROM user_preferences")
                total_users = cursor.fetchone()[0]
                
                # Intent distribution
                cursor.execute("""
                    SELECT intent_classified, COUNT(*) 
                    FROM user_interactions 
                    GROUP BY intent_classified
                """)
                intent_distribution = dict(cursor.fetchall())
                
                return {
                    "total_interactions": total_interactions,
                    "recent_interactions_24h": recent_interactions,
                    "total_patterns": total_patterns,
                    "total_users": total_users,
                    "intent_distribution": intent_distribution,
                    "cache_last_updated": self._last_cache_update,
                    "learning_cooldown": self.learning_cooldown
                }
                
        except Exception as e:
            self.logger.error(f"Error getting learning statistics: {e}")
            return {}

if __name__ == "__main__":
    # Test the auto-learning system
    learning_system = AutoLearningSystem("test_learning.db")
    
    # Test recording interactions
    test_interaction = UserInteraction(
        timestamp=time.time(),
        user_input="show me properties in Viman Nagar",
        intent_classified="SEARCH_PROPERTY",
        confidence=0.95,
        entities_extracted={"location": "Viman Nagar"},
        response_given="Here are properties in Viman Nagar...",
        session_id="test_user_123"
    )
    
    learning_system.record_interaction(test_interaction)
    
    # Test getting statistics
    stats = learning_system.get_learning_statistics()
    print("Learning System Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Test getting patterns
    patterns = learning_system.get_learned_patterns()
    print(f"\nLearned Patterns: {len(patterns)}")
    
    # Test getting user preferences
    prefs = learning_system.get_user_preferences("test_user_123")
    if prefs:
        print(f"\nUser Preferences: {prefs.preferred_intents}")
    
    # Export learning data
    learning_system.export_learning_data("test_learning_export.json")
