ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use

BASEURL = 'http://localhost:8000'
APIS = {
    'store': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'b00k_db',
        'USER': 'b00k',
        'PASSWORD':'b00k',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

