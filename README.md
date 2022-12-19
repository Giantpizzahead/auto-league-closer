# Auto League Finder

Tired of procrastinating on homework all day while still being hardstuck Bronze? Suffering from a bad case of League withdrawal?

Well, I've got a solution for you! Install the **Auto League Finder™**!

This handy program blasts you with alerts whenever it sees the League of Legends client, so you can get back to binging YouTube videos - uh, I mean doing homework :)

(This is a mock application, made solely to practice following style guidelines, making a clean project structure, and distributing packages / end user applications.)

### Setup

First, setup a [virtual environment](https://kylefu.me/cheat_python/envanddeps.html). Then run:

```bash
$ pip install -r requirements.txt
```

If you want to help develop the project, also run:

```bash
$ pip install -r dev_requirements.txt
```

### Packaging into an EXE

First, create a Python file that calls your module's main function or does something else - the "entry point" of your application. Then, to bundle it up, do the following:

```bash
# Initial pyinstaller to generate .spec file
pyinstaller entry.py --name leaguecloser --clean --onefile --icon leagueicon.png
# Go into the .spec file, and add Tree('<relative path to data folder from cwd>', prefix='<relative path to data folder from cwd (for consistency)>') after a.binaries in the EXE section
# Then, run the below to regenerate the EXE
pyinstaller --clean leaguecloser.spec
# Or (these are equivalent, see the Makefile):
make build
```
