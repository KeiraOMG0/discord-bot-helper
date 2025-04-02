from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="discord-bot-helper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'discord.py>=2.3.0',
        'python-dotenv>=1.0.0'
    ],
    entry_points={
        'console_scripts': [
            'dbh-init=discord_bot_helper.__main__:main'
        ]
    },
    author="Keira",
    description="Discord Bot Setup Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeiraOMG0/discord-bot-helper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
