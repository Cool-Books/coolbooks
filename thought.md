### USER
- email - unique (if email exists, raise 403)

- password (enforce a pattern and hash)
pattern of password must be:
* at least 8 characters long
* must contain at least one uppercase
* must contain at least an integer
* must contain at least a symbol

- bio (string not more than 250 characters)

- first name (validation)
* must not be empty
* must not contain any number or symbol
* must not be more than 50 characters

- last name (validation)
* same as first name

- other names (if any)

- is author (yes/no)


### BOOKS
- title of books - enforced
- Authors of the book - enforced
- short description - optional
- year of publication - optional
- edition - optional
- ISBN (uuid.uuid4) - optional
- Content - enforced
- Genre - optional
    



