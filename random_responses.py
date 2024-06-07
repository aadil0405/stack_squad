import random


def random_string():
    random_list = [
        "Oh! It appears you wrote something I don't understand yet",
        "Do you mind trying to rephrase that?",
        "I'm terribly sorry, I didn't quite catch that.",
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]