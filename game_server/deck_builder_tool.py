import re

unit_card = open("./unit_card_template.py", "r")
txt: str = ""


def create_card() -> None:
    global txt
    for line in unit_card.readlines():
        regula = "%[A-z]+%"
        var = re.findall(regula, line)
        for element in var:
            line = re.sub(element, input(element + ": "), line)
        txt += line


def save_card() -> None:
    global txt
    new_card = open(input("name file:"), "w")
    new_card.write(txt)
    txt = ""


def main() -> None:
    global txt
    while (i := input("<<Wiating for command>>: ")) != "q":
        match i:
            case "h":
                print("(q)uit, (c)reate card")
            case "c":
                create_card()
            case "p":
                print(txt)
            case "s":
                save_card()


if __name__ == "__main__":
    main()
