# Multilingual Online Translator
# Author: Jason Tolbert (https://github.com/jasonalantolbert)
# Python Version: 3.8


# BEGINNING OF PROGRAM


import re

import requests
from bs4 import BeautifulSoup

supported_languages = {  # dictionary of languages supported by the translator
    0: "all",
    1: "arabic",
    2: "dutch",
    3: "english",
    4: "french",
    5: "german",
    6: "hebrew",
    7: "japanese",
    8: "polish",
    9: "portuguese",
    10: "romanian",
    11: "russian",
    12: "spanish",
    13: "turkish"
}

session = requests.Session()  # opens a new requests session


def select_language():  # gets two languages and a word from the user via the command line

    # command line argument parsing
    source = input("Source language: ")
    target = input("Target language: ")
    word = input("Word to translate: ")

    print(f"\nTranslating '{word}' from {source.capitalize()} to "
          f"{target.capitalize() if target != 'all' else 'all languages'}...\n")
    return source.lower(), target.lower(), word.lower()


def validate(source, target, word):
    # language choice validation
    if source not in supported_languages.values() or target not in supported_languages.values():
        print(f"Sorry, this translator doesn't support "
              f"{source.capitalize() if source not in supported_languages.values() else target.capitalize()}"
              f". Please try again with a supported language.")
        return False
    elif source == target:
        print("You need to pick two different languages. Please try again.")
        return False

    # internet conecction validation
    try:
        site = request("english", "spanish", word)
    except requests.ConnectTimeout:
        # triggers if the translation service fails to respond
        print("There's something wrong with the translation service. Please try again later.")
        return False
    except requests.ConnectionError:
        # triggers if the program is unable to connect to the internet
        print("There's something wrong with your internet connection. "
              "Please fix the problem and try again.")
        return False

    # word validation
    if site.status_code == 404:
        print(f"Unable to find a translation for {word}. Please try again.")
        return False

    # if all validations passed
    return True


def request(o_lang, d_lang, word):  # requests data from the translation service
    return session.get(f"https://context.reverso.net/translation/{o_lang}-{d_lang}/{word}",
                       headers={"User-Agent": "Mozilla/5.0"})


def check_site_connection(site):  # checks that the translation service returns status code 200
    return True if site.status_code == 200 else False


def present(soup, lang):  # presents the translation information in a human-readable format
    translations = soup.find_all(class_=re.compile("^translation"))
    print(f"\n{lang.capitalize()} Translations:")
    if len(translations) >= 3:
        for index, element in enumerate(translations):
            if index in range(2, 7):
                print(re.sub("^\s*|\n", '', element.get_text()))
            elif index > 6:
                break
    else:
        print("None")

    print(f"\n{lang.capitalize()} Examples:")
    for index, element in enumerate(soup.find_all(class_="example")):
        if index in range(0, 6):
            src, trg = [re.compile("^src"), re.compile("^trg")]
            for mode in [src, trg]:
                print(re.sub("^\s*|\n", '', element.find(class_=mode).get_text())
                      + (":" if mode == src else '\n'))
        elif index > 5:
            break


def main():  # acts as master control for the rest of the program
    orig_language, dest_language, word = select_language()  # gets languages and word from select_language()

    if validate(orig_language, dest_language, word):  # validates the user input with validate()
        if dest_language != "all":  # runs if the user did not request translation to all languages
            site = request(orig_language, dest_language, word)
            if check_site_connection(site):
                present(BeautifulSoup(site.content, "lxml"), dest_language)
            else:
                print("Something went wrong. Please try again.")
                session.close()
                exit()
        else:
            # runs if the user requested translation for all languages. it's basically the same process as a single
            # language translation except a for loop runs it once for each supported language that's not the
            # origin language.
            for key in range(1, max(supported_languages.keys()) + 1):
                if supported_languages[key] != orig_language:
                    site = request(orig_language, supported_languages[key], word)
                    if check_site_connection(site):
                        present(BeautifulSoup(site.content, "lxml"), supported_languages[key])
                    else:
                        print("Something went wrong. Please try again.")
                        session.close()
                        exit()
    else:
        exit()

    session.close()


main()  # runs main()

# END OF PROGRAM
