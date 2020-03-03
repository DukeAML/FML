import re
import sys
import os

from flask.cli import main

if __name__ == '__main__':
    # export FLASK_DEBUG=1
    # export FLASK_APP=app.py
    os.environ['FLASK_DEBUG'] = "1"
    os.environ['FLASK_APP'] = 'app.py'
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())