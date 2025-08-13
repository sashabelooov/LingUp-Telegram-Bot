import random

answer_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}

tests = {
    "Beginner": {
        "questions": {
            1: ["What is the correct form of the verb 'to be' for 'I'?", "is", "are", "am", "be"],
            2: ["Which word is a color?", "Book", "Blue", "Run", "Table"],
            3: ["What is the plural of 'cat'?", "Cat", "Cates", "Catses", "Cats"],
            4: ["Choose the correct article: ___ apple.", "A", "An", "The", "No"],
            5: ["What is the opposite of 'big'?", "Tall", "Large", "Small", "Wide"],
            6: ["Which is a correct greeting?", "Go!", "Sleep!", "Hello!", "Eat!"],
            7: ["What is the past tense of 'go'?", "Goes", "Went", "Gone", "Going"],
            8: ["Which word is a number?", "Fine", "Fire", "Five", "Fish"],
            9: ["What is the correct pronoun for 'Mary'?", "He", "It", "They", "She"],
            10: ["Which is a day of the week?", "January", "Monday", "Morning", "Summer"]
        },
        "answers": {
            1: "C", 2: "B", 3: "D", 4: "B", 5: "C",
            6: "C", 7: "B", 8: "C", 9: "D", 10: "B"
        }
    },
    "Elementary": {
        "questions": {
            1: ["What is the correct form: 'She ___ to school every day.'?", "go", "goes", "going", "gone"],
            2: ["Which word is an adjective?", "Quickly", "Run", "Happy", "Book"],
            3: ["What time ___ it?", "is", "are", "be", "am"],
            4: ["Choose the correct word: 'I ___ my homework.'", "do", "does", "doing", "did"],
            5: ["Which is a month?", "Monday", "March", "Evening", "Hour"],
            6: ["What is the past of 'eat'?", "Eated", "Ate", "Eaten", "Eating"],
            7: ["Which is correct: 'We ___ students.'?", "are", "is", "am", "be"],
            8: ["What is the opposite of 'fast'?", "Quick", "Slow", "High", "Big"],
            9: ["Which word is a noun?", "Run", "Happy", "Book", "Quickly"],
            10: ["Choose the correct sentence: 'I ___ to the park.'", "go", "goes", "going", "gone"]
        },
        "answers": {
            1: "B", 2: "C", 3: "A", 4: "A", 5: "B",
            6: "B", 7: "A", 8: "B", 9: "C", 10: "A"
        }
    },
    "Pre-Intermediate": {
        "questions": {
            1: ["Choose the correct tense: 'I ___ my homework yesterday.'", "do", "did", "done", "doing"],
            2: ["What does 'break down' mean?", "To stop working", "To cry", "To run fast", "To eat"],
            3: ["Which is correct: 'She ___ to the park.'?", "go", "goes", "went", "going"],
            4: ["What is the past of 'see'?", "Saw", "Seen", "See", "Seeing"],
            5: ["Which is a preposition?", "Under", "Jump", "Fast", "Good"],
            6: ["Choose the correct form: 'I ___ here since morning.'", "am", "was", "have been", "be"],
            7: ["What is a synonym for 'big'?", "Small", "Large", "Fast", "Tall"],
            8: ["Which sentence is correct?", "She don’t like coffee.", "She doesn’t like coffee.", "She not like coffee.", "She no likes coffee."],
            9: ["What is the past of 'buy'?", "Buyed", "Bought", "Buying", "Buys"],
            10: ["Which word means 'tired'?", "Sleepy", "Happy", "Quick", "Strong"]
        },
        "answers": {
            1: "B", 2: "A", 3: "C", 4: "A", 5: "A",
            6: "C", 7: "B", 8: "B", 9: "B", 10: "A"
        }
    },
    "Intermediate": {
        "questions": {
            1: ["Which sentence is in passive voice?", "The cat chased the mouse.", "The mouse was chased by the cat.", "The cat is chasing the mouse.", "The mouse chases the cat."],
            2: ["What is a synonym for 'happy'?", "Sad", "Angry", "Joyful", "Tired"],
            3: ["Choose the correct form: 'If I ___ rich, I would travel.'", "am", "was", "were", "be"],
            4: ["What does 'give up' mean?", "To stop trying", "To start", "To win", "To help"],
            5: ["Which is correct: 'I ___ him yesterday.'?", "see", "saw", "seen", "seeing"],
            6: ["Choose the correct tense: 'She ___ to Paris twice.'", "has been", "was", "is", "goes"],
            7: ["What is an antonym for 'difficult'?", "Hard", "Easy", "Complex", "Tough"],
            8: ["Which is correct: 'I ___ to the party if I have time.'?", "go", "will go", "went", "going"],
            9: ["What does 'run out of' mean?", "To use all of something", "To exercise", "To escape", "To win"],
            10: ["Choose the correct form: 'He ___ for two hours.'", "studies", "studied", "has been studying", "study"]
        },
        "answers": {
            1: "B", 2: "C", 3: "C", 4: "A", 5: "B",
            6: "A", 7: "B", 8: "B", 9: "A", 10: "C"
        }
    },
    "Upper-Intermediate": {
        "questions": {
            1: ["Choose the correct conditional: 'If I ___ you, I would apologize.'", "am", "was", "were", "be"],
            2: ["What does 'to look forward to' mean?", "To anticipate with pleasure", "To look at something in front", "To search for", "To avoid"],
            3: ["Which is correct: 'She ___ the report by tomorrow.'?", "finish", "finishes", "will finish", "finished"],
            4: ["What is an antonym for 'increase'?", "Grow", "Decrease", "Rise", "Expand"],
            5: ["Choose the correct form: 'I wish I ___ more time.'", "have", "had", "having", "has"],
            6: ["What does 'take for granted' mean?", "To appreciate", "To assume without question", "To reject", "To give away"],
            7: ["Which is correct: 'By this time next year, I ___ my degree.'?", "finish", "finished", "will have finished", "finishing"],
            8: ["What is a synonym for 'persuade'?", "Convince", "Prevent", "Confuse", "Ignore"],
            9: ["Choose the correct form: 'The book ___ last year.'", "is published", "was published", "published", "publishing"],
            10: ["What does 'put off' mean?", "To delay", "To start", "To finish", "To enjoy"]
        },
        "answers": {
            1: "C", 2: "A", 3: "C", 4: "B", 5: "B",
            6: "B", 7: "C", 8: "A", 9: "B", 10: "A"
        }
    }
}


async def get_random_questions():
    # 1. Tasodifiy level tanlaymiz
    level = random.choice(list(tests.keys()))

    # 2. Shu level ichidan tasodifiy savol tanlaymiz
    question_num = random.choice(list(tests[level]["questions"].keys()))

    # 3. Savol va to‘g‘ri javobni ajratib olamiz
    question = tests[level]["questions"][question_num]
    correct_answer_letter = tests[level]["answers"][question_num]
    correct_answer_index = answer_to_index[correct_answer_letter]

    return question, correct_answer_index

