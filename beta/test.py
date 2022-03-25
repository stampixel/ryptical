# import validators
# valid=validators.url('codespeedy.com')
# if valid==True:
#     print("Url is valid")
# else:
#     print("Invalid url")


from werkzeug.security import generate_password_hash
print(generate_password_hash('1LaSeR545', method='sha256'))