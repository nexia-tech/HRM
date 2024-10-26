import random
import string

def generate_password(length=12):
    """
    Generates a random password of the specified length.

    Args:
        length (int, optional): Password length. Defaults to 12.

    Returns:
        str: Randomly generated password.
    """

    # Define character sets
    chars = {
        'lower': string.ascii_lowercase,
        'upper': string.ascii_uppercase,
        'numbers': string.digits,
        'special': string.punctuation
    }

    # Ensure password contains at least one character from each set
    password = [
        random.choice(chars['lower']),
        random.choice(chars['upper']),
        random.choice(chars['numbers']),
        random.choice(chars['special'])
    ]

    # Fill the rest of the password length with random characters
    for _ in range(length - 4):
        char_type = random.choice(list(chars.keys()))
        password.append(random.choice(chars[char_type]))

    # Shuffle the list to avoid the first characters always being from specific sets
    random.shuffle(password)

    # Join the list into a single string
    return ''.join(password)
