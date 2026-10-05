from sentence_transformers import SentenceTransformer, util

# 1. Load the AI Model
print("Loading AI Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Define the sentences we want to compare
word1 = "Car"
word2 = "Automobile"
word3 = "Apple"

# 3. Convert words into Vector Embeddings (Lists of numbers)
vector1 = model.encode(word1)
vector2 = model.encode(word2)
vector3 = model.encode(word3)

# 4. Calculate Cosine Similarity
similarity_car_auto = util.cos_sim(vector1, vector2)
similarity_car_apple = util.cos_sim(vector1, vector3)

# 5. Print the results
print("\n=== AI SEMANTIC SIMILARITY TEST ===")
print(f"Similarity between '{word1}' and '{word2}': {similarity_car_auto[0][0]:.4f}")
print(f"Similarity between '{word1}' and '{word3}': {similarity_car_apple[0][0]:.4f}")

# 1.0 means exact same meaning, 0.0 means completely unrelated