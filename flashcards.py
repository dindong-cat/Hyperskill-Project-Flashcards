# Write your code here
import random
from io import StringIO
import argparse


memory_file = StringIO()


def add_flashcard(flashcard_dict):
    print_and_log("The card:")
    term = input()
    memory_file.write(f"{term}\n")
    while term in flashcard_dict:
        print_and_log(f'The term "{term}" already exists. Try again:')
        term = input()
        memory_file.write(f"{term}\n")
    print_and_log("The definition of the card:")
    definition = input()
    memory_file.write(f"{definition}\n")
    while definition in [flashcard_dict[i]["definition"] for i in flashcard_dict]:
        print_and_log(f'The definition "{definition}" already exists. Try again:')
        definition = input()
        memory_file.write(f"{definition}\n")
    flashcard_dict[term] = {"definition": definition, "mistake": 0}
    print_and_log(f'The pair ("{term}":"{definition}") has been added.')
    print_and_log()
    return flashcard_dict


def ask_flashcard(flashcard_dict):
    print_and_log("How many times to ask?")
    need_to_ask = int(input())
    memory_file.write(f"{need_to_ask}\n")
    if not flashcard_dict:
        print_and_log("No question in database!")
        print_and_log()
    else:
        for i in range(need_to_ask):
            question = random.choice(list(flashcard_dict))
            print_and_log(f'Print the definition of "{question}":')
            answer = input()
            memory_file.write(f"{answer}\n")
            if answer == flashcard_dict[question]["definition"]:
                print_and_log("Correct!")
            elif answer in [i["definition"] for i in flashcard_dict.values()]:
                for key, value in flashcard_dict.items():
                    if answer == value["definition"]:
                        break
                print_and_log(f'Wrong. The right answer is "{flashcard_dict[question]["definition"]}", but your definition is correct for "{key}".')
                flashcard_dict[question]["mistake"] += 1
            else:
                print_and_log(f'Wrong. The right answer is "{flashcard_dict[question]["definition"]}".')
                flashcard_dict[question]["mistake"] += 1
        print_and_log()
    return flashcard_dict


def remove_flashcard(flashcard_dict):
    print_and_log("Which card?")
    to_be_removed = input()
    memory_file.write(to_be_removed)
    if to_be_removed not in flashcard_dict:
        print_and_log(f'Can\'t remove "{to_be_removed}": there is no such card.')
        print_and_log()
    else:
        del flashcard_dict[to_be_removed]
        print_and_log("The card has been removed.")
        print_and_log()
    return flashcard_dict


def import_flashcard(flashcard_dict):
    print_and_log("File name:")
    file_name = input()
    memory_file.write(f"{file_name}\n")
    try:
        with open(file_name, "r") as f:
            file_content = [i.strip().split(" ") for i in f]
        temp_dict = {i[0]: {"definition": i[1], "mistake": int(i[-1])} for i in file_content}
        for i in temp_dict:
            flashcard_dict[i] = temp_dict[i]
        print_and_log(f"{len(file_content)} cards have been loaded.")
        print_and_log()
    except FileNotFoundError:
        print_and_log("File not found.")
        print_and_log()
    return flashcard_dict


def export_flashcard(flashcard_dict):
    print_and_log("File name:")
    file_name = input()
    memory_file.write(file_name)
    try:
        with open(file_name, "w") as f:
            for i, j in flashcard_dict.items():
                f.writelines(f"{i} {j['definition']} {j['mistake']}\n")
            print_and_log(f"{len([i for i in flashcard_dict])} cards have been saved.")
            print_and_log()
    except:
        print_and_log("Some errors happened")
        print_and_log()
    return flashcard_dict


def reset_flashcard(flashcard_dict):
    for i in flashcard_dict:
        flashcard_dict[i]["mistake"] = 0
    print_and_log("Card statistics have been reset.")
    return flashcard_dict


def hardest_flashcard(flashcard_dict):
    if flashcard_dict:
        hardest = max(i["mistake"] for i in flashcard_dict.values())
        hardest_items = [i for i in flashcard_dict if flashcard_dict[i]["mistake"] == hardest]
        hardest_items_string = ", ".join(['"' + i + '"' for i in flashcard_dict if flashcard_dict[i]["mistake"] == hardest])
        if hardest == 0:
            print_and_log("There are no cards with errors.")
        elif len(hardest_items) == 1:
            print_and_log(f'The hardest card is {hardest_items_string}. You have {hardest} errors answering it.')
        else:
            print_and_log(f'The hardest cards are {hardest_items_string}. You have {hardest} errors answering them.')
    else:
        print_and_log("There are no cards with errors.")
    return flashcard_dict


def log_flashcard(flashcard_dict):
    content = memory_file.getvalue()
    print_and_log("File name:")
    file_name = input()
    memory_file.write(f"{file_name}\n")
    with open(file_name, "w") as f:
        for i in content:
            f.write(i)
    print_and_log("The log has been saved.")
    return flashcard_dict


def print_and_log(string=""):
    print(string)
    if string:
        memory_file.write(string + "\n")
    else:
        memory_file.write("\n")


def action_menu(flashcard_dict):
    print_and_log("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    action = input()
    memory_file.write(f"{action}\n")
    if action == "add":
        flashcard_dict = add_flashcard(flashcard_dict)
    elif action == "ask":
        flashcard_dict = ask_flashcard(flashcard_dict)
    elif action == "remove":
        flashcard_dict = remove_flashcard(flashcard_dict)
    elif action == "import":
        flashcard_dict = import_flashcard(flashcard_dict)
    elif action == "export":
        flashcard_dict = export_flashcard(flashcard_dict)
    elif action == "exit":
        print("Bye bye!")
        return False
    elif action == "log":
        flashcard_dict = log_flashcard(flashcard_dict)
    elif action == "hardest card":
        flashcard_dict = hardest_flashcard(flashcard_dict)
    elif action == "reset stats":
        flashcard_dict = reset_flashcard(flashcard_dict)
    return action_menu(flashcard_dict)


def main():
    flashcard_dict = {}

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--import_from")
    parser.add_argument("-e", "--export_to")
    args = parser.parse_args()
    if args.import_from:
        try:
            with open(args.import_from, "r") as f:
                file_content = [i.strip().split(" ") for i in f]
            temp_dict = {i[0]: {"definition": i[1], "mistake": int(i[-1])} for i in file_content}
            for i in temp_dict:
                flashcard_dict[i] = temp_dict[i]
            print_and_log(f"{len(file_content)} cards have been loaded.")
            print_and_log()
        except FileNotFoundError:
            print_and_log("File not found.")
            print_and_log()

    action_menu(flashcard_dict)

    if args.export_to:
        try:
            with open(args.export_to, "w") as f:
                for i, j in flashcard_dict.items():
                    f.writelines(f"{i} {j['definition']} {j['mistake']}\n")
                print_and_log(f"{len([i for i in flashcard_dict])} cards have been saved.")
                print_and_log()
        except:
            print_and_log("Some errors happened")
            print_and_log()


if __name__ == "__main__":
    main()
