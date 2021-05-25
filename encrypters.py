import random
import string

lower = string.ascii_lowercase
upper = string.ascii_uppercase
random.seed(1)


def caesar_cipher(message, shift=random.randint(1, 26)):
    """A Caesar or shift cipher shifts each letter of a message a number of positions in the alphabet.
    Use negative shift for left shifts and positive for right shifts."""

    encrypted_message = ""
    for ch in message:
        if ch in lower:
            encrypted_message += lower[(lower.index(ch) + shift) % len(lower)]
        elif ch in upper:
            encrypted_message += upper[(upper.index(ch) + shift) % len(upper)]
        else:
            encrypted_message += ch
    return encrypted_message


def rot13(message):
    return caesar_cipher(message, 13)


def vigenere_cipher(message: str, keyword="a") -> str:
    encrypted_message = ""
    for i, ch in enumerate(message):
        key = keyword[i % len(keyword)].lower()
        encrypted_message += caesar_cipher(ch, lower.index(key))
    return encrypted_message


def vigenere_decipher(message: str, keyword: str = "a") -> str:
    decrypted_message = ""
    for i, ch in enumerate(message):
        key = keyword[i % len(keyword)].lower()
        decrypted_message += caesar_cipher(ch, -lower.index(key))
    return decrypted_message


def alberti_cipher(message, index="a",
                   min_characters_before_change=10,
                   max_characters_before_change=20):
    """In the Alberti Cipher there are two disks, one with upper case ordered letter
    and the other one with lowercase randomly shuffled letters.
    Sender and receiver should have the same lowercase disk in order to use it.
    A letter is selected as index The first capital letter indicates """

    encrypted_message = ""
    lower_circle = "zxvtrpnljhfdbacegikmoqsuwy"
    assert len(upper) == len(lower_circle)

    message_index = 0
    disk_changes = 0

    while message_index < len(message):
        key = random.choice(upper)
        encrypted_message += key
        disk_changes += 1
        for _ in range(random.randint(min_characters_before_change, max_characters_before_change)):
            if message.lower()[message_index] in lower_circle:
                encrypted_message += lower_circle[
                    upper.index(message[message_index].upper()) - (upper.index(key) - lower_circle.index(index)) % len(
                        lower_circle)]
            else:
                encrypted_message += message[message_index]
            message_index += 1
            if message_index >= len(message):
                break

    return encrypted_message


def alberti_decipher(message, index="a"):
    """A function that decipher a message that used an Alberti cipher"""

    decrypted_message = ""
    upper_circle = upper
    lower_circle = "zxvtrpnljhfdbacegikmoqsuwy"

    for ch in message:
        if ch in upper_circle:
            if upper_circle.index(ch) < lower_circle.index(index):
                lower_circle = (lower_circle[lower_circle.index(index) -
                                upper_circle.index(ch):] +
                                lower_circle[:(lower_circle.index(index) - upper_circle.index(ch) + 26) % len(upper)])

            elif upper_circle.index(ch) > lower_circle.index(index):
                lower_circle = lower_circle[(lower_circle.index(index) + len(upper) - upper_circle.index(ch)) % len(
                    upper):] + lower_circle[
                               :(lower_circle.index(index) + len(upper) - upper_circle.index(ch)) % len(upper)]

        elif ch in lower_circle:
            decrypted_message += upper_circle[lower_circle.index(ch)].lower()
        else:
            decrypted_message += ch
    return decrypted_message
