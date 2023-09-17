from django.contrib.auth.hashers import PBKDF2PasswordHasher


class HistoryHasher(PBKDF2PasswordHasher):
    """
    We need to keep the old password so that when you update django 
    (or configuration change) hashes have not changed. 
    Therefore, special hasher.

    """
    # Experimental value of the of iterations so that the calculation on the
    # average server configuration lasted around one second.
    iterations = 20000 * 10


class HistoryVeryStrongHasher(PBKDF2PasswordHasher):
    """
    We need to keep the old password so that when you update django 
    (or configuration change) hashes have not changed. 
    Therefore, special hasher.

    """
    # Experimental value of the of iterations so that the calculation on the
    # average server configuration lasted around 10 second.
    iterations = 20000 * 101