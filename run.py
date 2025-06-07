from project import create_app
import subprocess

# Run create_app() and run the app on localhost (and all other ports)
if __name__ == '__main__':
  # Install playwright packages
  script_path = 'install_playwright.ps1'
  subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)
  
  app = create_app()
  app.run(host = '0.0.0.0', port = 8000, debug = True)