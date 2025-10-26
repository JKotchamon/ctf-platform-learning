import base64

payload = b'IiIudGkgZ25pbm51ciBvZiBkYWV0c25pIGVkb2Mgc2lodCB0bmlycCB0c3VKICMKIiBuMDF0cHlyY24zX3Qwbl9zMV80Nl8zczRiJ1ZVQyIgPSBnYWxmCi5lcmVoIHRoZ2lyIHNpIGdhbGYgZWhUICMKIHJlZW5pZ25lIGVzcmV2ZXIgLGVub2QgbGxlVyAjIiIi'

def unleash(data):
    try:
        decoded = base64.b64decode(data)
        unscrambled = decoded.decode('utf-8')[::-1]
        exec(unscrambled)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Running the secret task... done.")
    unleash(payload)