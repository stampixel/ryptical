from website import create_app # __init__ makes a folder a python package, so we can directly import functions

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)