import sys

def open_file(name):
    with open (name, "r") as myfile:
        return myfile.read().rstrip()

def main(name):
    html = ""
    data = open_file(name)
    print(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] You did not supply enough arguments")
        print("[INFO] To execute type: 'py ./beau.py <FILENAME>'")
    elif len(sys.argv) > 2:
        print("[ERROR] You supplied too many arguments")
        print("[INFO] To execute type: 'py ./beau.py <FILENAME>'")
    else:
        main(sys.argv[1])