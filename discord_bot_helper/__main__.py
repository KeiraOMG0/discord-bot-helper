from .config_setup import setup_config

def main():
    """Entry point for CLI configuration"""
    try:
        import discord
        from dotenv import load_dotenv
    except ImportError:
        import sys
        import subprocess
        print("⚠️  Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py", "python-dotenv"])
    
    setup_config()

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 60c585b (Pushing changes!)
