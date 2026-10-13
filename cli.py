''' Import CLI to parse file'''
import sys

def command_line_interface():
  if len(sys.argv) != 2:
    print("Error: Please provide the correct number of arguments. [python your_parser.py program.uedge]")
    sys.exit(1)
  
  uedge_file = sys.argv[1]

  if not uedge_file.endswith(".uedge"):
    print("Error: Please provide a valid .uedge file.")
    sys.exit(1)

  try:
    with open(uedge_file, 'r', encoding = 'utf-8') as file:
      source_code = file.read()
  
  except OSError as e:
    print(f"Error: Could not read file '{uedge_file}': {e}")
    sys.exit(1)

  return source_code

'''
if __name__ == "__main__":
  source_code = command_line_interface()
  print(source_code)
'''
