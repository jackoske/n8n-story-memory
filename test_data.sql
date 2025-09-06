-- Test data for local development and testing

-- Insert test children
INSERT INTO children (name, age, reading_level, interests) VALUES 
('Alice', 7, 2, ARRAY['dragons', 'friendship', 'adventure']),
('Bob', 8, 3, ARRAY['pirates', 'treasure', 'ocean']),
('Emma', 6, 2, ARRAY['unicorns', 'magic', 'friendship']);

-- Insert test stories
INSERT INTO stories (child_id, story_text, difficulty, summary, keywords) VALUES 
(1, 'Once upon a time, there was a friendly dragon named Spark who loved making friends. Spark lived in a cave high up in the mountains, but he was lonely. One day, he decided to visit the village below to find some friends.', 2, 'A lonely dragon named Spark seeks friendship in a village', ARRAY['dragon', 'friendship', 'Spark', 'village']),

(1, 'Spark the dragon had made friends with the village children. They played together every day, flying through clouds and exploring magical forests. But one day, Spark had to help save the village from a terrible storm.', 3, 'Spark and his friends work together to save the village from a storm', ARRAY['dragon', 'Spark', 'storm', 'teamwork', 'village']),

(2, 'Captain Bob sailed his ship across the vast blue ocean. His crew of brave pirates searched for the legendary Golden Compass, a treasure that could grant any wish. But first, they had to solve three riddles left by the ancient pirate king.', 3, 'Captain Bob and crew search for the magical Golden Compass treasure', ARRAY['pirates', 'treasure', 'ocean', 'riddles', 'Captain Bob']),

(3, 'Luna the unicorn had beautiful rainbow wings, but she had never learned to fly. All the other unicorns in the magical forest could soar through the sky, but Luna was afraid of heights. Her friend Bella the butterfly offered to help.', 2, 'Luna the unicorn learns to overcome her fear of flying with help from Bella', ARRAY['unicorn', 'flying', 'friendship', 'Luna', 'Bella', 'wings']);

-- Insert test feedback
INSERT INTO feedback (story_id, child_id, rating, comprehension_score) VALUES 
(1, 1, 5, 85),
(2, 1, 4, 90),
(3, 2, 5, 88),
(4, 3, 4, 82);