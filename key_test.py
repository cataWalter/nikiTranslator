from operator import itemgetter
import csv

import keyboard
from googletrans import Translator
from tabulate import tabulate

my_languages = ["es", "fr", "tr", "nl", "de", "pt"]


def load_words():
    with open('words.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def add_new_words(word_dict, used_words, translator, dictionary):
    translation = translator.translate(used_words, "en").text.lower()
    print("translation: " + str(translation))
    for translated_word in translation.split(" "):
        if translated_word in dictionary:
            found = False
            for word_from_dict in word_dict:
                if word_from_dict[1] == translated_word:
                    word_from_dict[0] += 1
                    found = True
                    break
            if not found:
                new_word_list = [1, translated_word]
                for x in my_languages:
                    try:
                        y = translator.translate(translated_word, x).text.lower()
                    except:
                        y = ""
                    new_word_list.append(y)
                word_dict.append(new_word_list)
        else:
            print(translated_word + " not found in the dictionary")
    word_dict = sorted(word_dict, key=itemgetter(0), reverse=True)
    return word_dict


def print_current_dictionary(used_words_counter):
    print(tabulate(used_words_counter, headers=["Occurrences", "en"] + my_languages, tablefmt='orgtbl'))


def save(used_words_counter):
    print("saving")
    with open("out.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerows(used_words_counter)


def read():
    print("reading")
    with open("out.csv", "r", encoding="utf-8") as f:
        used_words_counter = list(csv.reader(f, delimiter=","))
    used_words_counter = [[int(word[0])] + word[1:] for word in used_words_counter]
    return used_words_counter


def init_translator():
    translator = Translator()
    dictionary = load_words()
    used_words_counter = read()
    to_skip = ["maiusc", "tab", "backspace", "?", "!", "ctrl", "enter", "freccia destra", "freccia sinistra", "alt gr"]
    while True:
        recorded = keyboard.record(until='enter')
        print("recorded: " + str(recorded))
        result = ""
        for x in recorded:
            if x.event_type == "up":
                if x.name == "space":
                    result += " "
                elif x.name == "del":
                    result = result[:1]
                elif x.name not in to_skip:
                    result += x.name
        if result.__contains__("#s"):
            save(used_words_counter)
        if result.__contains__("#q"):
            save(used_words_counter)
            return
        if len(result) > 0:
            print("result: " + result)
            used_words_counter = add_new_words(used_words_counter, result, translator, dictionary)
        print_current_dictionary(used_words_counter)


if __name__ == '__main__':
    init_translator()
