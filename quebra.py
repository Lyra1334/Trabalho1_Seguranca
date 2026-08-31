from collections import Counter
from string import ascii_uppercase

try:
    from .vigenere import Decodificar
except ImportError:
    from vigenere import Decodificar


def frequency_table(values):
    return dict(zip(ascii_uppercase, values))


ENGLISH_FREQUENCIES = frequency_table((
    .08167, .01492, .02782, .04253, .12702, .02228, .02015,
    .06094, .06966, .00153, .00772, .04025, .02406, .06749,
    .07507, .01929, .00095, .05987, .06327, .09056, .02758,
    .00978, .02360, .00150, .01974, .00074,
))

PT_BR_FREQUENCIES = frequency_table((
    .1463, .0104, .0388, .0499, .1257, .0102, .0130,
    .0128, .0618, .0040, .0002, .0278, .0474, .0505,
    .1073, .0252, .0120, .0653, .0781, .0434, .0463,
    .0167, .0001, .0021, .0001, .0047,
))


def normalize(text):
    return "".join(c.upper() for c in text if c.isascii() and c.isalpha())


def index_of_coincidence(text):
    counts = Counter(text)
    size = len(text)
    if size < 2:
        return 0
    return sum(n * (n - 1) for n in counts.values()) / (size * (size - 1))


def average_ic(text, key_length):
    return sum(
        index_of_coincidence(text[i::key_length])
        for i in range(key_length)
    ) / key_length


def chi_squared(text, frequencies):
    counts = Counter(text)
    size = len(text)
    return sum(
        (counts.get(letter, 0) - frequency * size) ** 2 / (frequency * size)
        for letter, frequency in frequencies.items()
    )


def guess_key(text, key_length, frequencies):
    key = ""
    for column in (text[i::key_length] for i in range(key_length)):
        scores = []
        for shift in range(26):
            decoded = "".join(
                chr((ord(c) - 65 - shift) % 26 + 65) for c in column
            )
            scores.append(chi_squared(decoded, frequencies))
        key += chr(65 + min(range(26), key=scores.__getitem__))
    return key


def rank_key_lengths(text, maximum=20):
    maximum = min(maximum, max(1, len(text) // 2))
    return sorted(
        ((length, average_ic(text, length)) for length in range(1, maximum + 1)),
        key=lambda item: (-item[1], item[0]),
    )


def choose_key_length(candidates):
    best_length, best_ic = candidates[0]
    return min(
        length for length, ic in candidates
        if best_length % length == 0 and ic >= best_ic - .0025
    )


def shortest_repeating_key(key):
    for length in range(1, len(key) + 1):
        if key == key[:length] * (len(key) // length):
            return key[:length]
    return key


def decode_file(filename, frequencies=ENGLISH_FREQUENCIES):
    with open(filename, encoding="utf-8") as file:
        original = file.read()

    text = normalize(original)
    if not text:
        raise ValueError("The input does not contain any ASCII letters.")

    key_length = choose_key_length(rank_key_lengths(text))
    key = shortest_repeating_key(guess_key(text, key_length, frequencies))
    print(f"Guessed key: {key}\n")
    return Decodificar(original, key)
