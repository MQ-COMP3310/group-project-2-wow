from project import create_app
import platform
import subprocess
import os

# Run create_app() and run the app on localhost (and all other ports)
if __name__ == '__main__':
  # Part 2 Task 7: Implementation of Authentication
  # Part 3 Task 9: Implementation of Additional Features
  # Install playwright packages
  script_path = 'install_playwright.ps1'
  
  # Only run PowerShell install script on Windows
  if platform.system() == "Windows":
    script_path = os.path.join(os.getcwd(), "install_playwright.ps1")
    if os.path.exists(script_path):
        try:
            print("Running Playwright setup script...")
            subprocess.run([
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-File", script_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            print("Error during Playwright setup:")
            print(e)
  
  app = create_app()
  app.run(host = '0.0.0.0', port = 8000, debug = True)