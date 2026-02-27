# ParadoxParser
A complex Paradox Parser, utilising tokenisation and structural clues to build a paradox file as a series of nested python objects, in order to preserve code structure, i found other parsers were either baked into software, or incomplete/destructive handling, (e.g. successful got meradata, but destroyed trigger/effect code) 

This is just python code, you WILL require python coding knowledge, to make use of it, 
[examples gist](https://gist.github.com/stevenj2019/04b322de5374b9f0cec8dadfd2eb7c6d)

it handles all paradox differences as well as developer preference
e.g. 
limit = { check_variable = { var = x } 
and 
limit = 
{
    check_variable = {
      var = x 
    }
}

(note, the writer doesnt care for your preference, its "correct" wether you like it or not) 
(like the second example)

NOTE: currently, this will nuke your comments, i am working on it, but (see AI usage) i dont want to do anymore of that than i have to, and it isnt a priority, if it has comments in it, its likely a complex script file, and i see no value in why youd want to make changes this way.  

#AI usage notice
The parser itself, is entirely "vibe coded", it was a boring process of ensuring every possible case, in paradox changes, or just ibndividual formatting difference, were all included, and properly nested. it has however been extensively human-checked, and i will absolutely keep an eye on bugs, or discord contact regarding any issues that are found, 
i have intentionally ran this on complicated effect files to ensure there is no issues (i format weirdly to make sure my effects arent hundreds of lines long) and verified its accuracy. but i always welcome feedback, with a ._print_tree() statement and the file attached. 
The writer is entirely human made by myself.
