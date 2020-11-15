# Vowels shift right by 1. Y will not be considered
# All F's are now ph
# Y and Q Swap

def encrypter(msg):
    enc_msg = ""
    for char in msg:
        if char in "Aa":
            enc_msg = enc_msg + "e"
        elif char in "Ee":
            enc_msg = enc_msg + "i"
        elif char in "Ii":
            enc_msg = enc_msg + "o"
        elif char in "Oo":
            enc_msg = enc_msg + "u"
        elif char in "Uu":
            enc_msg = enc_msg + "a"
        elif char in "Ff":
            enc_msg = enc_msg + "ph"
        elif char in "Yy":
            enc_msg = enc_msg + "q"
        elif char in "Qq":
            enc_msg = enc_msg + "y"
        else:
            enc_msg = enc_msg + char
    return enc_msg


message = input("Enter Your Message:")
new_message = encrypter(message)
print(new_message)