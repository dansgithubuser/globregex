#-----imports-----#
import argparse, os, re

try: input=raw_input
except NameError: pass

#-----args-----#
parser=argparse.ArgumentParser(description='regex operations on files')
parser.add_argument('path', help='path to look for files in')
parser.add_argument('text_pattern', help='pattern to search in text')
parser.add_argument('-tr', '--text_replace', help='expression to replace pattern with')
parser.add_argument('-fp', '--file_pattern', help='pattern to filter files with')
parser.add_argument('-c', '--cautious', action='store_true', help='ask for confirmation for file modifications')
parser.add_argument('-da', '--dotall', action='store_true', help='make . match newlines')
parser.add_argument('-ml', '--multiline', action='store_true', help='make ^ and $ work on newlines')
args=parser.parse_args()

#process files
filenames=[]
for path, dirs, files in os.walk(args.path):
	for file in files:
		if not args.file_pattern or re.match(args.file_pattern, file):
			filenames.append(os.path.join(path, file))

#process flags
flags=0
if args.dotall   : flags|=re.DOTALL
if args.multiline: flags|=re.MULTILINE

#-----helpers-----#
def separator(): print('='*72)

def section(s):
	width=10
	print('\n'+'-'*10+s+'-'*10)

def context(text, start, end):
	line_number=1
	column=1
	start_of_line=0
	for i in range(start):
		column+=1
		if text[i]=='\n':
			line_number+=1
			column=1
			start_of_line=i+1
	line=''
	i=start_of_line
	while i<len(text) and (i<end or text[i]!='\n'):
		line+=text[i]
		i+=1
	line=line.strip()
	return (line_number, column, line)

#-----info-----#
separator()
section('text_pattern')
print(args.text_pattern)
if args.text_replace:
	section('text_replace')
	print(args.text_replace)
if args.file_pattern:
	section('file_pattern')
	print(args.file_pattern)

#-----process-----#
for filename in filenames:
	#match
	with open(filename) as file: text=file.read()
	matches=re.finditer(args.text_pattern, text, flags=flags)
	#print
	empty=True
	for match in matches:
		empty=False
		line_number, column, line=context(text, match.start(), match.end())
		separator()
		section('match')
		print(filename)
		print('line {0}, column {1}'.format(line_number, column))
		print(line)
		if args.text_replace:
			section('replacement')
			print(re.sub(args.text_pattern, args.text_replace, match.group(), flags))
	#replace
	if args.text_replace and not empty:
		replace=True
		if args.cautious:
			print('replace these matches (y/n)?')
			replace=input()=='y'
		if replace:
			text=re.sub(args.text_pattern, args.text_replace, text, flags=flags)
			with open(filename, 'w') as file: file.write(text)
