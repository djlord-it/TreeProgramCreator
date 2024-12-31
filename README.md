# Directory Creator

Ever seen a cool directory tree on GitHub or had an LLM describe one and thought, "I wish I could create that structure easily"? Now you can! **Directory Creator** transforms tree-like structures into real directories and files, hassle-free.

## Features
- **Easy GUI**: Copy, paste, and click.
- **Safety First**: Protects against rogue paths and unsafe filenames.
- **Smart Cleanup**: Cleans up failed attempts.
- **Logging**: See what happens behind the scenes.

## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/djlord-it/TreeProgramCreator.git
   cd TreeProgramCreator
   ```
2. Install dependencies:
   ```bash
   pip install tkinter
   ```

## Usage
1. Run the app:
   ```bash
   python main.py
   ```
2. Paste a tree structure like this:
   ```
   Project/
   ├── src/
   │   ├── main.py
   │   └── tests/
   └── README.md
   ```
3. Select a destination and click "Create Structure."

## Why Use This?
Stop wasting time manually creating directories. Perfect for:
- Setting up project skeletons.
- Recreating directory structures from GitHub or AI output.
- Quickly prototyping ideas.

