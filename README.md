# Build a Godot Project for iOS without a Mac!

Tools to develop apps for iOS without a Mac with Godot Engine!

Ever wanted to stop hopping between your Mac and Windows/Linux PCs when developing an iOS Project? This is the project for you!

Features:
- Editor to update the .ipa file of your game without rebuilding!
- Uploader that pushes your game to GitHub actions for building!


> [!NOTE]
> [My blog post](https://mak448a.github.io/blog/compile-ios-godot-without-mac) may have more up-to-date instructions!

> [!WARNING]
> I try my best to write code that works, but I may have accidentally included bugs. Please report any that you find and please be cautious!

## Requirements
- GitHub CLI (2.63.2 tested, other versions untested.)
- Git (2.50.1 tested)
- Python (3.12+)
- Godot Engine

## Installation and Configuration
1. First, download [Python](Python.org/downloads), Git, and [GitHub CLI](https://cli.github.com/). Make sure to check the box that says "Add to PATH" when installing Python if you're on Windows. Run this command if you want to install Python, Git, and GitHub CLI on Windows: `winget install Git.Git GitHub.cli Python.Python.3.13`, then log into GitHub with `gh auth login`.

2. Inside your project, go to `Project>Export...>Add..>iOS` and set team and bundle identification. Since this project builds an unsigned IPA, you can put anything for the team.
3. Press `Export Project` and save it to a new folder.
4. Open a Terminal/Command Prompt and download [build-ios](https://github.com/mak448a/build-ios) with the following command.
```shell
git clone https://github.com/mak448a/build-ios --depth=1
```
5. Change the current directory to build-ios with
```shell
cd build-ios
```
6. Install dependencies with the commands below. Choose the one for your operating system.

**Windows**
(Run in command prompt)

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux**
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
7. Visit https://www.dropbox.com/developers/apps to get your Dropbox token for use with the tool.
![Screenshot of "create new app"](tutorial/1.png)
You can name your app whatever you want, as long as it's unique.
![Screenshot of app naming](tutorial/2.png)
![Screenshot of generating access token](tutorial/3.png)
![Screenshot of going to permissions tab](tutorial/4.png)
![Screenshot of permissions](tutorial/5.png)
![Screenshot of submit button](tutorial/6.png)
8. Create the file `.env` and add `TOKEN=YOURKEYHERE` (replace the token with your token) to it.
9. Run the Python script!
```shell
python main.py
```
10. (Optional) If you want to skip writing in the questions every time you want to build, add the answers to the `.env` file. Make sure to check `example.env` for how to do this!
11. When you launch the CLI with `python main.py`, it'll prompt you to choose whether you want to build or edit an IPA. For the first time, choose build IPA.

## Usage
When you launch the CLI with `python main.py`, it'll prompt you to choose whether you want to build or edit an IPA. For the first time, choose build IPA.

If you want to save your answers, you can edit `.env` with your DropBox token, GitHub username, repository name, and output file.

When the program asks you for a path, you can drag in a file into the terminal window.

**Build IPA:**
- Follow the prompts.

**Edit IPA:**
- When exporting your Godot Project, choose "Export PCK/ZIP" and save it as `yourproject.pck`. Put it in the folder where you downloaded this program.

### But what's the difference?
- Build IPA is for the first time you run the CLI. It makes a fresh build of your project.
- Edit IPA is for after the first build. After exporting the PCK, use this option to replace the PCK in the IPA. If you changed any settings in `project.godot`, rebuild the IPA.


## Troubleshooting
### AuthError('expired_access_token', None)
Your token is probably expired. Get a new OAuth token from Dropbox.

If you still have problems, check [the other troubleshooting thread](https://github.com/mak448a/build-ios/issues/13) or open an issue in [this repository](https://github.com/mak448a/build-ios/issues)!
While you're waiting, try following the [original instructions](https://github.com/mak448a/build-ios/tree/main/original_repo).
### Invalid files
Did you add double quotes around the file path?

### Edit IPA not working
Did you place your pck file in the same directory as your ipa file?


## Privacy Policy
- I don't collect any data from this project.
- This project uses GitHub and Dropbox. See the privacy policies for these services for more information.


## Notes and credits
- Edit IPA function inspired by [this article by RandomMomentania](https://randommomentania.com/2022/01/godot-easy-ios-app-testing/)
- Started work on this project ~11/2024.
- Inspired by [u/_atreat](https://www.reddit.com/r/godot/comments/vlwrj0/comment/idxn5z8/) and [u/Host127001](https://www.reddit.com/r/godot/comments/s0pj02/comment/hs3rjl3/) who suggested building with GitHub Actions.
