from project import create_app
import platform
import subprocess

# Run create_app() and run the app on localhost (and all other ports)
if __name__ == '__main__':
  # Install playwright packages
  script_path = 'install_playwright.ps1'
  # Only run PowerShell install script on Windows

  if platform.system() == "Windows":
    try:
      subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)
    except subprocess.CalledProcessError as e:
      print(e.stderr)
  
  app = create_app()
  app.run(host = '0.0.0.0', port = 8000, debug = True)