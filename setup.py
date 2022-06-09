import pwinput as pw

print("To run the scraper you will need a linkedIn account (You can create a fake account too for the purpose)")

username = input("Enter your LinkedIn username: ")
password = pw.pwinput("Enter your LinkedIn password: ")

with open(".env", "w") as f:
    f.write(f"USERNAME = '{username}'\n")
    f.write(f"PASSWORD = '{password}'\n")

    f.close();

