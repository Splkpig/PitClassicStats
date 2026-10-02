import time

# Read a certain line in a file
def read_specific_line(file_path, line_number):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            index = line_number
            if 0 <= index < len(lines):
                return lines[index].strip()
            else:
                return None
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Create a session in the session storage file
def startSession(player, userID, xp, gold, kills, deaths, playtime):
    timeUNIX = int(time.time())
    stats_string = f"{player}:{userID}:{xp}:{gold}:{kills}:{deaths}:{playtime}:{timeUNIX}"

    with open("../PitStats/storage/sessions.txt", "a") as file:
        file.write(stats_string + '\n')


# Get the info about a session from the session storage file
def viewSession(userID):
    with open("../PitStats/storage/sessions.txt", "r") as file:
        for line in file:
            fromFileID = line.split(":", 2)[1]
            if str(userID) == fromFileID:
                return line
    return None


# Delete a session from the session storage file
def endSession(userID):
    with open("../PitStats/storage/sessions.txt", "r") as file:
        lines = file.readlines()

    updated_lines = [line for line in lines if not line.split(":")[1] == str(userID)]
    with open("../PitStats/storage/sessions.txt", "w") as file:
        file.writelines(updated_lines)


# Check if a user already has a session in the session storage file
def hasSession(userID):
    with open("../PitStats/storage/sessions.txt", "r") as file:
        for line in file:
            fromFileID = line.split(":", 2)[1]
            if str(userID) == fromFileID:
                return True
    return False


# Check the currently stored sessions and delete any older than 24 hours
def checkSessions():
    with open("../PitStats/storage/sessions.txt", "r") as file:
        for line in file:
            fromFileTime = int(line.split(":")[7])
            if fromFileTime + 86400 <= int(time.time()):
                # print(f"Ended session for: {line.split(':')[0]}")
                endSession(line.split(":")[1])