export FLASK_APP=app/
export FLASK_DEBUG=true
flask run

# If error ocurrs after creation table.
# -> CREATE EXTENSION IF NOT EXISTS "uuid-ossp";