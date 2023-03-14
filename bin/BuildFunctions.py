import argparse
import subprocess


def CreateBranch():

    branch_name = str(
        input(
            "Type a name for this branch: "
        )
    ).replace(" ", "")

    subprocess.run(
        f"git checkout -b {branch_name}"\
              .split()
    )

    return 0


def EnumerateCommits():

    while True:
        subprocess.run("clear")
        subprocess.run("git add --patch".split())
        subprocess.run("git commit".split)

        while True:
            decision = input(
                "Commit added; would you like to add another? Y/n: "
            )[0].lower()

            if decision == "y": break
            elif decision == "n": exit()
            else: print("Error! Please only type either Yes or No.")

    subprocess.run("git push")

    return 0


def IncrementProjectVersion(file):

    version = ""
    update = ""
    patch = ""

    with open(file, "r") as project_file:
        pyproject = project_file.readlines()


    updated_lines = ""

    for line in pyproject:

        if line.split(" ")[0] == "version":

            version_octets = line.split(" ")[-1]\
                                 .strip()\
                                 .replace("\"", "")\
                                 .split(".")

            version = version_octets[0]
            update  = version_octets[1]
            patch   = version_octets[2]

            if int(patch) >= 9:
                update = str(int(update) + 1)
                patch = "0"
            
            if int(update) >= 9:
                version = str(int(version) + 1)
                update = "0"

            else: 
                patch = str(int(patch) + 1)

            build_number = ".".join([version, update, patch])

            line = f"version = \"{build_number}\"\n"

        updated_lines += line


    # Write the new lines to the pyproject.toml file.
    with open(file, "w") as project_file:
        project_file.write(updated_lines)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--branch", action="store_true")
    parser.add_argument("-e", "--enumerate", action="store_true")
    parser.add_argument("-i", "--increment", action="store_true")
    parser.add_argument("-f", "--file")

    arguments = parser.parse_args()

    if arguments.enumerate: EnumerateCommits()
    if arguments.branch: CreateBranch()
    if arguments.increment: IncrementProjectVersion(arguments.file)