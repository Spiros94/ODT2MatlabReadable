import sys
import os
import Tkinter, tkFileDialog, tkMessageBox

targetOutDir = './output/'

def ExitProgram():
    print "[+] End"
    END = raw_input('..Press Enter key to exit..')
    raise SystemExit
    
def CheckOutputPathExistance():
    ''' Check if 'output' folder exists. If not create one '''
    if not os.path.exists(targetOutDir):
        os.makedirs(targetOutDir)

def CheckOutputFileExistance(OutputFileName,Extension):
    ''' Checks if the output file already exists. If so it creates another name for the file and returns it '''
    CheckExist = targetOutDir + OutputFileName + Extension
    i = 1 # Just an iterator
    while os.path.isfile(CheckExist): # If output file exists add a number at then end of the filename and try again
        OutputFileName += str(i)
        CheckExist = targetOutDir + OutputFileName + Extension
        i += 1
    return OutputFileName
        
def CheckInputFile(ODTfile):
    if not os.path.isfile(ODTfile):
        print "[!] No file named " + ODTfile + " found. Exit"
        ExitProgram()

def ColumnsRow(ColsRow):
    # Split and concat the fourth row of the file
    ColsNew = list() # List for the splitted row
    ColsRow = ColsRow.replace(ColsRow[:12],'') # Remove the first 12 characters
    ColsRow = ColsRow.split(' ')
    ColsRow = filter(lambda name: name.strip(), ColsRow) # Remove spaces from list
    colbuffer = ''
    for column in ColsRow:
        if column[0] != '{' and colbuffer == '':
            ColsNew.append(column)
        else:
            if '}' in column:
                colbuffer = colbuffer + column
                ColsNew.append(colbuffer)
                colbuffer = ''
            else:
                colbuffer = colbuffer + column + '_'
    return ColsNew        

def UnitsRow(UnitsRow):
    ''' Returns a list with the units for the columns  '''
    UnitsRow = UnitsRow.replace(UnitsRow[:8],'') # Remove the first 8 characters
    UnitsRow = UnitsRow.split(' ')
    UnitsRow = filter(lambda name: name.strip(), UnitsRow) # Remove spaces from list
    return UnitsRow

def CheckLine(line):
    ''' If the line contains the Units row returns "unit" '''
    ''' Else if line contains the Columns row returns "cols" '''
    ''' Else if line contains the a comment row returns "com" '''
    ''' Else returns "num" '''
    if line.startswith("#"):
        if line.startswith("# Units:"):
            return "uni"
        elif line.startswith("# Columns:"):
            return "cols"
        else:
            return "com"
    else:
        return "num"

def CountFileLines(File):
    ''' Counts file lines '''
    return sum(1 for line in open(File))

def MatlabScript(FHandler,ODTFile,Cols):
    FHandler.write("format long\n")
    FHandler.write("graphVals = importdata('" + ODTFile + "');\n")
    for m in range(0, len(Cols)):
        FHandler.write("a" + str(m+1) + " = graphVals(:," + str(m+1) + ");\n")
        
def HelperFile(FHandler,ODTFile,Cols,Units):
    FHandler.write("\t\t\t~~~ Data for " + ODTFile + "~~~\n")
    for c in range(0, len(Cols)):
        FHandler.write("a" + str(c+1) + " == " + Cols[c].replace("\n","") + " || " + Units[c] + "\n")
    
    
def main():
    UNITS = []
    COLUMNS = []
    FindUnitsRow = True # Flag for Units row in source file
    FindColsRow = True  # Flag for Columns row in source file
    k = 0 # Iterator for while loop
    
    root = Tkinter.Tk()
    root.withdraw()
    ODTfile = tkFileDialog.askopenfilename()
    print '[+] Open File'
    print "[+] Input File: " + ODTfile
    
    CheckInputFile(ODTfile)
    CheckOutputPathExistance()
    
    OutputFileName = targetOutDir + CheckOutputFileExistance(os.path.split(ODTfile)[1][:-4],".odt") + ".odt"
    print "[+] Output filename is: " + OutputFileName
    OutputHandler = open(OutputFileName, 'w')
    print "[+] Output file created"
    
    Infile = open(ODTfile,'r')
    print '[+] File is open. Trying to count lines'
    num_lines = CountFileLines(ODTfile) # Count how many lines are in the file
    print '[+] ' + str(num_lines) + ' lines found in source file'

    while(k < num_lines):
        line = Infile.readline()
        if CheckLine(line) == "num":
            OutputHandler.write(line)
        elif FindUnitsRow == True and CheckLine(line) == "uni":
            FindUnitsRow = False
            UNITS = UnitsRow(line)
        elif FindColsRow == True and CheckLine(line) == "cols":
            FindColsRow = False
            COLUMNS = ColumnsRow(line)
        elif CheckLine(line) == "com":
            continue
        else:
            print " [!] Exiting unexpectedly while reading lines in file"
            ExitProgram()
        k += 1

    OutputHandler.close()
    print "[+] " + str(CountFileLines(OutputFileName)) + " lines written in output file"
    Infile.close()


    if tkMessageBox.askyesno("Matlab Script","Do you want to create a matlab script too?"):
        MatlabScriptFileName = os.path.split(OutputFileName)[1][:-4]
        
        CheckOutputFileExistance(MatlabScriptFileName,".m")
        MatlabFileHandler = open(os.path.join(targetOutDir,MatlabScriptFileName)+".m",'w')
        MatlabScript(MatlabFileHandler,os.path.split(OutputFileName)[1],COLUMNS)
        MatlabFileHandler.close()
        
        HelperFileName = MatlabScriptFileName
        CheckOutputFileExistance(HelperFileName,".help")
        HelperFileHandler = open(os.path.join(targetOutDir,HelperFileName)+".help",'w')
        HelperFile(HelperFileHandler,os.path.split(OutputFileName)[1],COLUMNS,UNITS)
        HelperFileHandler.close()        
    
    ExitProgram()
    
if __name__ == "__main__":
    main()
