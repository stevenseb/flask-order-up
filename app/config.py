# !!START
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'you-will-never-guess'
    # define any other secret environment variables here

# !!END
