#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 2

"""

import argparse
import sys

__version__ = '1.0'
__desc__ = "A simple script used to authenticate spies!"


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT0179G Assignment 2 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('credentials', metavar='credentials', type=str,
                        help="Username and password as string value")

    args = parser.parse_args()

    if not authenticate_user(args.credentials):
        print("Authentication failed. Program exits...")
        sys.exit()

    print("Authentication successful. User may now access the system!")


def authenticate_user(credentials: str) -> bool:
    """Procedure for validating user credentials"""
    username = 'Chevy_Chase'            # Expected username. MAY NOT BE MODIFIED!!
    password = 'i0J0u0j0u0J0Zys0r0{'    # Expected password. MAY NOT BE MODIFIED!!
    user_tmp = pass_tmp = str()

    ''' PSEUDO CODE
    PARSE string value of 'credentials' into its components: username and password.
    SEND username for FORMATTING by utilizing devoted function. Store return value in 'user_tmp'.
    SEND password for decryption by utilizing devoted function. Store return value in 'pass_tmp'.
    VALIDATE that both values corresponds to expected credentials.
    RETURN outcome of validation as BOOLEAN VALUE.
    '''
    c = credentials.split()
    user_tmp = f"{c[0]} {c[1]}"
    pass_tmp = c[2]
    return format_username(user_tmp) == username and decrypt_password(pass_tmp) == password


def format_username(username: str) -> str:
    """Procedure to format user provided username"""

    ''' PSEUDO CODE
    FORMAT first letter of given name to be UPPERCASE.
    FORMAT first letter of surname to be UPPERCASE.
    REPLACE empty space between given name and surname with UNDERSCORE '_'
    RETURN formatted username as string value.
    '''
    u = username.split()
    return f"{u[0].capitalize()}_{u[1].capitalize()}"


def decrypt_password(password: str) -> str:
    """Procedure used to decrypt user provided password"""
    rot7, rot9 = 7, 9       # Rotation values. MAY NOT BE MODIFIED!!
    vowels = 'AEIOUaeiou'   # MAY NOT BE MODIFIED!!
    decrypted = str()

    ''' PSEUDO CODE
    REPEAT {
        DETERMINE if char IS VOWEL.
        DETERMINE ROTATION KEY to use.
        DETERMINE decryption value
        ADD decrypted value to decrypted string
    }
    RETURN decrypted string value
    '''
    for i in range(len(password)):
        is_vowel = vowels.find(password[i])
        key = rot7 if i % 2 == 0 else rot9
        decrypted_value = chr(ord(password[i]) + key) if is_vowel == -1 else f"0{chr(ord(password[i]) + key)}0"
        decrypted += decrypted_value
    return decrypted


if __name__ == "__main__":
    main()
