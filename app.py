from ytdown import create_app
from ytdown import db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
