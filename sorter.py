target_username_length = 4 

with open("hits.txt", "r") as infile:
    usernamelist = infile.read().splitlines()

with open(f"{target_username_length}c.txt", "a") as outfile:
    for username in usernamelist:
        if len(username) == target_username_length and username.strip():
            print(username)
            outfile.write(username + "\n")