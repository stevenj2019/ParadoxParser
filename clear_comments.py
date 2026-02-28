from ParadoxParser import ParadoxScriptParser as PDXParser
from ParadoxParser.ParadoxNodes import GenericBlock
#in this current version of the code this will work
paradox_file = PDXParser(path="/mnt/RAID/Projects/extremis-ultimis-dev/eu/events/EU_ARG_events.txt")
paradox_file._backup_file()
paradox_file._to_pdx_script_file()
#once i implement the code replace with something like this 
# paradox_file = PDXParser(path="")
# for node in paradox_file.nodes:
#     for child in node.children:
#         if (isinstance(child), GenericBlock):
#             #iterate
#             print()
#         else:
#             if (isinstance(child), GenericCommentBlock):
#                 #tag for removal
# paradox_file._backup_file()
# paradox_file._write_file()

