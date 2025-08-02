import random

my_list = list(range(1, 101))

random_number = random.choice(my_list)

print(f"The randomly selected number is: {random_number}")

async def beginner_test(qn):
    test = {
        "Beginner": {
            1: ["What is the correct greeting in the morning?", "Good night", "Good morning", "Good evening", "Good afternoon"]
        },
        "Answer":{
            1: "B"
        }
    }
    return test["Beginner"][qn],test["Answer"][qn]