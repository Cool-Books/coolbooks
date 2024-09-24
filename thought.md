### USER
- email - unique (if email exists, raise 403)
- password (enforce a pattern and hash)
pattern of password must be:
* at least 8 characters long
* must contain at least one uppercase
* must contain at least an integer
* must contain at least a symbol
- bio (string not more than 200 characters)
- first name
- last name
- other names (if any)
