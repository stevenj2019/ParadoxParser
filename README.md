# ParadoxParser
A complex Paradox Parser, utilising tokenisation and structural clues to build a paradox file as a series of nested python objects, in order to preserve code structure, i found other parsers were either baked into software, or incomplete/destructive handling, (e.g. successful got meradata, but destroyed trigger/effect code) 

This is just python code, you WILL require python coding knowledge, to make use of it, 
[examples gist](https://gist.github.com/stevenj2019/04b322de5374b9f0cec8dadfd2eb7c6d)

it handles all paradox differences as well as developer preference
e.g. 
```
limit = { check_variable = { var = x } }
```
<br> and <br>
```
limit = 
{ 
    check_variable = { 
      var = x 
    } 
}
```
will be treat identically, (because they are)

## Installation 
``` pip install git+https://github.com/stevenj2019/ParadoxParser.git```
## Removal 
``` pip uninstall ParadoxParser ```
## Update 
remove + install it 
## Local Build 
1. download the repo as a zip 
2. unzip it somewhere 
3. go to it in your preferred terminal 
```
  pip install -r requirements.txt
  python -m build 
  pip install dist/ParadoxParser-1.3py3-none-any.whl
```

## Known Limitation (will address)
* preserve comments, as a custom object, so it can be easily removed in script (done)

## Known Limitation (will never address)
* the Writer Part of this module will follow formatting best practices (as commonly agreed by community and wiki), if you care, sorry, i format weirdly too, ill let this fix it for me :D

## AI Notice

The "ParadoxParser" was created almost entirely by an AI language model and human checked for correctness.
This software is intended solely for personal, hobbyist, or educational use. Corporate appropriation — even for free usage — and any monetization are strictly prohibited.  
No human should claim ownership of AI works. This tool is designed to be freely used and must remain free for its intended purposes.

**License:** This software is released under the [PolyForm Noncommercial License](#LICENSE) (to be included in this repository), which legally enforces these usage restrictions.

## Changelog
### 1.0 initial release - MVP
- basic Parser, produced minimal structure to not break a file, 
### 1.1 Comments, and fixes
- provides minor fixes to the parser in cases of event_ids "<str>.<int>"
- support GenericComment Node, to store comments and preserve their whitespace/newline 
### 1.2 advanced variable usage fix
- proves support for token:var and var:var structures, to preserve their structure
- added ParadoxLocParser, read-only testing completed
### 1.3 name hotfix
- fixes string support when operator or punctuation in string ":, =, <, >, ."

This is mainly being modified as i find issues in ParadoxEdit (a currently hidden github project, if you notice a bug i have not yet, feel free to raise it)

## by 2.0 i intent to have a bugfree parser toolset