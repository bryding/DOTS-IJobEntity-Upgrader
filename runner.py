import argparse
import os

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dir', default="sandbox", help="The top level directory containing all of the .cs files that need to be updated.")
    parser.add_argument('--commit', default='false', choices=['true', 'false'], help="Set to false to merely print out potential results, no files will be changed. True will update the files")

    args = parser.parse_args()
    commit = args.commit == 'true'

    for subdir, dirs, files in os.walk(args.dir):
      for file in files:
        if file.lower().endswith('.cs'):
          filePath = os.path.join(subdir, file).replace("\\","/")
          if needsUpgrade(filePath):
            processFile(filePath)

def processFile(filePath):
  print(f'Processing file: {filePath}')
  
  # Read the file into a list of strings
  with open(filePath, 'r') as file:
    data = file.readlines()
  
  # Get the index of the line that contains the word, 'IJobEntity'
  index = next((i for i, line in enumerate(data) if ': IJobEntity' in line), None)

  # Given the index, get the name of the struct where the word, 'IJobEntity' was found and name comes after the word 'struct'
  structName = data[index].split('struct')[1].split(':')[0].strip()

  # Get the index of the line that contains the words 'new {structName}'
  index = next((i for i, line in enumerate(data) if f'new {structName}' in line), None)
  start, end = getBracketIndexes(data, structName)

  # If start and end are the same or start is greater than end, return
  if start == end or start > end or end - start == 1:
    print(f'No changes needed for file: {filePath}')
    return

  # for each line in the range of start to end, get the index of the first word after the tab
  for i in range(start, end):
    # Get the index of the first word after the spaces
    varIndex = data[i].find(data[i].strip())
    # add the word var to the first word after the tab
    data[i] = '      job.' + data[i][varIndex:]

    # Remove commas from the line
    data[i] = data[i].replace(',', '')
    data[i] = data[i].replace('\n', '')
    # add a semicolon to the end of the line
    data[i] = data[i] + ';\n'

  # Replace this line with the following "var job = new {structName}();"
  data[index] = f'      var job = new {structName}();\n'

  # Get the index of the line that contains the words '.Schedule'
  scheduleIndex = next((i for i, line in enumerate(data) if '.Schedule' in line), None)
  if (scheduleIndex == None):
      # Get the index of the line that contains the words '.Run'
      scheduleIndex = next((i for i, line in enumerate(data) if '.Run' in line), None)
  if (scheduleIndex != None):
    data[scheduleIndex] = data[scheduleIndex].replace('}.', 'job.')
  else:
    print(f'No schedule or run statement found for file: {filePath}')


  # Print the lines
  print(*data, sep='')
  return

# Given a list of strings that correspond to the lines of a c# file and an index where an object is being initialized, return the start and end index of the object's brackets
def getBracketIndexes(data, structName):
  # Get the index of the line that contains the word, 'new {structName}'
  index = next((i for i, line in enumerate(data) if f'new {structName}' in line), None)
  # Get the index of the first bracket starting at the index
  for i in range(index, len(data)):
    if '}' in data[i]:
      return -1, -1
    if '{' in data[i]:
      start = i
      break

  # If the start line contains the struct name, increment the startIndex by 1
  if structName in data[start]:
    start += 1

  # Get the index of the last bracket
  for i in range(start, len(data)):
    if '}' in data[i]:
      end = i
      break
  
  return start, end

def needsUpgrade(filePath):
  # Read the file into a string
  with open(filePath, 'r') as file:
    data = file.read()
  
  # Check if the file contains the word, 'IJobEntity'
  if 'IJobEntity' in data:
    return True
  return False

if __name__ == "__main__":
  main()