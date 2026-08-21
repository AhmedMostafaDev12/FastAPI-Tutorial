from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Takes plaintext, generates a random salt, runs 4096 rounds of bcrypt, returns that $2b$12$... string. 
# Called once per user, at signup.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Internally: reads the salt out of hashed_password, hashes plain_password with that same salt, compares the results. Returns True or False. 
# Called once per login.
def verify(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

## what is hasing ans salting?
# Hashing is a one-way function that converts input data (like a password) into a
# fixed-length string of characters, which is typically a hash value. It is designed to be irreversible, meaning you cannot easily retrieve the original input from the hash. 
# Hashing is commonly used for securely storing passwords, as it allows you to verify a password without storing the actual password itself.
# Salting is the process of adding a unique random value (the salt) to the input data before hashing it. This helps protect against certain types of attacks, such as rainbow table attacks, where precomputed hash values are used to crack passwords. By adding a salt, even if two users have the same password, their hashed values will be different due to the unique salt applied to each password.