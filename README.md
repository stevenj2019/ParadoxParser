# ParadoxParser
A complex Paradox Parser, utilising tokenisation and structural clues to build a paradox file as a series of nested python objects, in order to preserve code structure, i found other parsers were either baked into software, or incomplete/destructive handling, (e.g. successful got meradata, but destroyed trigger/effect code,

NOTICE: the parser itself, is very "vibe coded", there were a lot of possibilities to consider, so i spent 2 days whipping an ai to consider every condition, in any file regardless of formatting, 
e.g. 
limit = { check_variable = { var = x } 
and 
limit = 
{
    check_variable = {
      var = x 
    }
}

are treated as identical by the parser! 
and as such, i wont guaruntee it, on its own, this is unhelpful to those who dont know python, please check your objects and your work before commiting any changes using ParadoxWriter (a seperate module) which can be found [here](https://github.com/stevenj2019/ParadoxWriter)
