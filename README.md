# Drone-Vision-Spring-2021-Sample-Solution Development

Sample Solution Development README can be found [here](sol_v1/README.md).

## Submission Instruction
_Notice: The names of files or folders are sensitive._

Each team should submit only one file: `solution.pyz`: the zipped package of `solution/`. You should use __[zipapp](https://docs.python.org/3/library/zipapp.html)__ to create the `.pyz` file from your solution folder.
```
└── solution/
    ├── requirements.txt
    ├── __main__.py
    ├── main.py
    └── other modules and resources
```
* `requirements.txt`: Include all your dependencies. Make sure their versions are compatible on the Raspberry Pi .
* `__main__.py`: Used to run `solution/`. DO NOT modify.
* `main.py`: The script that we will use to execute your solution. Details are listed in the comments inside.
* `other modules and resources` (optional): Any other modules that `main.py` needs to import and any other files that you use in your solution.

### Creating `.pyz` files
We recommend zipping your solution using the following command. It adds a shebang line that we are able to use to identify what version of Python you are using.
```
python3 -m zipapp solution -p='/usr/bin/env python3.8'
```
The valid version of Python for the challenge is the latest patch version of CPython 3.8 for the AArch64 architecture. The command above specifies the shebang of your solution.
If you intend on using a different version of Python, please contact the organizers as soon as possible via Slack.

### Output
Your solution is expected to generate an `answer.txt` under the current directory when run. 
```
├── solution.pyz
└── answers.txt
```   
We will run your code using the follow command:
```
  $ unzip solution.pyz -d solution/
  $ cd solution/
  $ pip3 install -r requirements.txt
  $ cd ../
  $ python3 solution/ video.mp4 questions.txt
```

