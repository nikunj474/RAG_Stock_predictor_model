import os
import subprocess
import sys

def check_and_install_pgvector():
    try:
        # Step 1: Check if PostgreSQL is installed
        postgres_check = subprocess.run(["psql", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if postgres_check.returncode != 0:
            print("PostgreSQL is not installed. Please install PostgreSQL first.")
            sys.exit(1)
        else:
            print("PostgreSQL is installed.")

        # Step 2: Check if pgvector is already installed
        print("Checking if pgvector extension is installed...")
        create_extension_query = "CREATE EXTENSION IF NOT EXISTS vector;"
        install_check = subprocess.run(
            ["psql", "-c", create_extension_query],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if "ERROR" in install_check.stderr:
            print("pgvector is not installed. Attempting to install pgvector...")

            # Step 3: Install pgvector (Linux/macOS installation using GitHub)
            subprocess.run(["git", "clone", "https://github.com/pgvector/pgvector.git"], check=True)
            os.chdir("pgvector")
            subprocess.run(["make"], check=True)
            subprocess.run(["make", "install"], check=True)
            os.chdir("..")
            print("pgvector installed successfully. Now enabling it in PostgreSQL.")

            # Step 4: Enable pgvector extension
            enable_vector = subprocess.run(
                ["psql", "-c", create_extension_query],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if enable_vector.returncode == 0:
                print("pgvector extension enabled successfully.")
            else:
                print("Failed to enable pgvector extension:", enable_vector.stderr)
                sys.exit(1)
        else:
            print("pgvector extension is already installed and enabled.")

    except Exception as e:
        print(f"An error occurred while checking or installing dependencies: {e}")
        sys.exit(1)

def check_python_dependencies():
    # Step 5: Check and install Python dependencies
    required_packages = ["psycopg2", "pandas"]
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed. Installing now...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"{package} installed successfully.")

if __name__ == "__main__":
    print("Checking system dependencies for PostgreSQL and pgvector...")
    check_and_install_pgvector()
    print("Checking Python dependencies for PostgreSQL interaction...")
    check_python_dependencies()
    print("All dependencies are installed and ready.")
