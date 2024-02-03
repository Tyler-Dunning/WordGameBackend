from flask import Flask,request, jsonify
import csv

app = Flask(__name__)


# Specify the path to your CSV file and the column name containing the strings
csv_file_path = 'words_altered.csv'
string_column_name = 'aaargh'  # Replace with your actual column name

# Read the CSV file and create a set of strings
csv_strings_set = set()
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        string_from_csv = row[string_column_name]
        csv_strings_set.add(string_from_csv)

@app.route("/anagrams", methods=['GET'])
def anagrams():
    
    query = request.args.get('inputs')
    chars = [char for char in query]
    allWords = set()

    def recurseAnagram(curString, used, index):
        can = True
        tempUsed = used.split(";")
        for i in tempUsed:
            if(i == (str(index))):
                can = False
        if(0 <= index < 6 and can):
            used += str(index) + ";"
            curString += chars[index]
            if(len(curString) > 3):
                allWords.add(curString)
            for i in range(len(chars)):
                recurseAnagram(curString, used, i)

    for i in range(len(chars)):
        recurseAnagram("", "", i)

    result = [[],[],[],[]]
    for i in allWords:
        if(len(i) > 3 and i in csv_strings_set and i not in result[len(i) - 4]):
            result[len(i) - 4].append(i) 
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/wordhunt", methods=['GET'])
def wordhunt():
    
    query = request.args.get('inputs')
    letters = [char for char in query]
    allWords = set()

    grid = [['a', 'b', 'c', 'd'], 
            ['e', 'f', 'g', 'h'], 
            ['i', 'j', 'k', 'l'], 
            ['m', 'n', 'o', 'p']]

    for i in range(len(grid)):
        for k in range(len(grid[i])):
            grid[i][k] = letters[(i * 4) + k]

    allWords = []

    def recurse(indexes, curString, xVal, yVal):
        can = True
        tempUsed = indexes.split(";")
        for i in tempUsed:
            if(i == (str(xVal) + "" + str(yVal))):
                can = False
        
        if(0 <= xVal < 4 and 0 <= yVal < 4 and len(curString) < 7):
            can = True
            tempUsed = indexes.split(";")
            for i in tempUsed:
                if(i == (str(xVal) + "" + str(yVal))):
                    can = False
            if(can):
                indexes += str(xVal) + str(yVal) + ";"
                curString += grid[xVal][yVal]
                if(len(curString) > 3):
                    allWords.append(curString)
                
        
                recurse(indexes, curString, xVal + 1, yVal)
                recurse(indexes, curString, xVal - 1, yVal)
                recurse(indexes, curString, xVal, yVal + 1)
                recurse(indexes, curString, xVal, yVal - 1) 
                recurse(indexes, curString, xVal + 1, yVal + 1) 
                recurse(indexes, curString, xVal - 1, yVal + 1) 
                recurse(indexes, curString, xVal + 1, yVal - 1) 
                recurse(indexes, curString, xVal - 1, yVal - 1) 

    for i in range(4):
        for k in range(4):
            recurse("", "", i, k)

    result = [[],[],[],[]]
    for i in allWords:
        if(len(i) > 2 and i in csv_strings_set and i not in result[len(i) - 4]):
            result[len(i) - 4].append(i)
    return result
