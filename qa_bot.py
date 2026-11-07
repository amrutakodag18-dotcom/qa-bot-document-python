import re
import os
from collections import Counter

class DocumentQABot:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sections = []
        self.stop_words = set([
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
            "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", 
            "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
            "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
            "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
            "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
            "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", 
            "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
            "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
            "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
            "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
            "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
        ])
        self.index = self.load_and_index_document()

    def _read_file_content(self):
        if not os.path.exists(self.filepath):
            print(f"Error: File '{self.filepath}' not found.")
            return None

        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def load_and_index_document(self):
        content = self._read_file_content()
        if not content:
            return []

        self.sections = [s.strip() for s in content.split('\n\n') if s.strip()]
        
        index = []
        for i, section in enumerate(self.sections):
            tokens = self._tokenize(section)
            index.append({
                "section_id": i,
                "text": section,
                "tokens": Counter(tokens)
            })
        print(f"Successfully loaded '{self.filepath}' ({len(self.sections)} section(s) indexed).")
        return index

    def _tokenize(self, text):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return [w for w in words if w not in self.stop_words]

    def answer_question(self, question):
        if not self.index:
            return "No document loaded to search from."

        q_tokens = self._tokenize(question)
        if not q_tokens:
            return "Please ask a question with meaningful keywords."

        best_section = None
        max_score = 0

        for entry in self.index:
            score = sum(entry["tokens"][token] for token in q_tokens)
            if score > max_score:
                max_score = score
                best_section = entry["text"]

        if max_score == 0:
            return "Sorry, no relevant section matching your question was found in the document."
        
        return best_section

if __name__ == "__main__":
    print("--- Document Q&A Bot ---")
    file_name = input("Enter your document name (e.g., sample_document.txt): ").strip()
    if not file_name:
        file_name = "sample_document.txt"

    bot = DocumentQABot(file_name)
    
    if bot.index:
        print("\nBot ready! Ask questions based on your document (Type 'exit' to quit).\n")
        while True:
            user_q = input("Your Question: ")
            if user_q.strip().lower() == 'exit':
                print("Goodbye!")
                break
            answer = bot.answer_question(user_q)
            print(f"\nAnswer:\n{answer}\n" + "-"*60 + "\n")