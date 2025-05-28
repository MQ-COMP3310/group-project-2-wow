from project import create_app

# Run create_app() and run the app on localhost (and all other ports)
if __name__ == '__main__':
  app = create_app()
  app.run(host = '0.0.0.0', port = 8000, debug = True)