# import validators
# valid=validators.url('codespeedy.com')
# if valid==True:
#     print("Url is valid")
# else:
#     print("Invalid url")


from werkzeug.security import generate_password_hash
print(generate_password_hash('rando password sus', method='sha256'))