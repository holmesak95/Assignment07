#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes, functions, and structured error handling
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AHolmes, 2022-Mar-05, Updated code
# AHolmes, 2022-Mar-11, Separated error handling into a different class
# AHolmes, 2022-Mar-13, tested, fine-tuned code
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object

YES_NO_LIST = ['y','n']
MENU_LIST = ['l', 'a', 'i', 'd', 's', 'x']

# -- PROCESSING -- #
class ErrorProcessor:
    def valid_int():
        """
        Returns
        -------
        intID : TYPE = INTEGER
            DESCRIPTION = returns a valid integer

        """
        while True:
            try:
                intID = int(input('Enter ID: ').strip())
                return intID
            except:
                print('Please only enter numbers.')
                
    def valid_str(strQuestion, answers = []):
        """
        Parameters
        ----------
        strQuestion : TYPE = string
            DESCRIPTION = displays the question that the user will respond to
        answers : TYPE, optional = list
            DESCRIPTION. The default is []. displays the possible answers

        Raises
        ------
        Exception
            DESCRIPTION = if user enters without typing anything

        Returns
        -------
        strAnswer : TYPE = string
            DESCRIPTION = the user's response to strQuestion

        """
        while True:
            try:
                if len(answers) > 0:
                    strAnswer = str(input(strQuestion).strip().lower())
                    if (strAnswer not in answers):
                        raise Exception('Please enter a valid choice: ' + print(answers))
                else:
                    strAnswer = str(input(strQuestion).strip())
                if not strAnswer:
                    raise Exception('Empty string. Please enter value.')
                return strAnswer
            except:
                print('Please enter a string.')
                
    def valid_file(strFileName, openType):
        """
        Parameters
        ----------
        strFileName : TYPE = string
            DESCRIPTION = the name of the file
        openType : TYPE = string
            DESCRIPTION = whether to append, read, or write to the file

        Returns
        -------
        objFile : TYPE = file
            DESCRIPTION = what file to perform the action to
        newFileInd : TYPE = boolean
            DESCRIPTION = determines whether the file was newly created or not

        """
        try:
            objFile = open(strFileName, openType)
            newFileInd = False
            return objFile, newFileInd
        except FileNotFoundError:
            strAnswer = ErrorProcessor.valid_str('File was not found. Do you want to create a new file? ', YES_NO_LIST)
            if (strAnswer == 'y'):
                objFile = open(strFileName, 'ab')
                newFileInd = True
                return objFile, newFileInd
            else:
                newFileInd = False
                return None, newFileInd
            

class DataProcessor:
    def file_to_list(line, table):
        """
        Parameters
        ----------
        line : TYPE = string
            DESCRIPTION = contains 1 line from reading the file
        table : TYPE = list
            DESCRIPTION = list of dictionaries containing the CD Inventory

        Returns
        -------
        None.
        """
        
        #data = line.strip().split(',')
        #dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
        dicRow = line
        table.append(dicRow)
    
    def add_to_table(intID, strTitle, strArtist):
        """
        Parameters
        ----------
        intID : TYPE = int
            DESCRIPTION = the ID number for the CD (inputted from user)
        strTitle : TYPE = string
            DESCRIPTION = the title of the CD (inputted from user)
        strArtist : TYPE = string
            DESCRIPTION = the artist for the CD (inputted from user)

        Returns
        -------
        None.

        """
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)
    
    def add_inventory():
        """
        Returns
        -------
        resultID : TYPE = int
            DESCRIPTION = the ID number for the CD (inputted from user)
        strTitle : TYPE = string
            DESCRIPTION = the title of the CD (inputted from user)
        strArtist : TYPE = string
            DESCRIPTION = the artist for the CD (inputted from user)

        """
        intID = ErrorProcessor.valid_int()
        strTitle = ErrorProcessor.valid_str('What is the CD\'s title? ')
        strArtist = ErrorProcessor.valid_str('What is the Artist\'s name? ')
        
        return intID, strTitle, strArtist


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts). Pne line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile, newFileInd = ErrorProcessor.valid_file(file_name, 'rb')
        if objFile is None:
            print('There is no available file.')
            return False
        elif newFileInd is True:
            objFile.close()
            return False
        try:
            while True:
                try:
                    DataProcessor.file_to_list(pickle.load(objFile), table)
                except EOFError:
                    objFile.close()
                    return False
        except:
            print('File is probably empty. Can\'t load data.')
            return True

    @staticmethod
    def write_file(file_name, table):
        """
        Parameters
        ----------
        file_name : TYPE = string
            DESCRIPTION = contains the file name with which to write the CDs to
        table : TYPE = list (of dictionaries)
            DESCRIPTION = contains the list of CDs for writing to file

        Returns
        -------
        None.

        """
        objFile, newFileInd = ErrorProcessor.valid_file(file_name, 'wb')
        if objFile is None:
            print('There is no available file.')
            return True
        else:
            if len(table) == 0:
                return True
            for row in table:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                pickle.dump(row, objFile)
                #objFile.write(','.join(lstValues) + '\n')
            objFile.close()
            print('Data has been saved to the file.')
            return False

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection
        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in MENU_LIST:
            choice = ErrorProcessor.valid_str('Which operation would you like to perform? [l, a, i, d, s or x]: ', MENU_LIST)
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')
        
    def delete_CD(intIDDel):
        """
        Parameters
        ----------
        intIDDel : TYPE = int
        DESCRIPTION = the ID number of the CD user wants to delete

        Returns
        -------
        None.

        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
            

# 1. When program starts, read in the currently saved Inventory
fileEmptyInd = FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        if (fileEmptyInd is True):
            print('It\'s not possible to load data from the file right now.')
            continue
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strAnswer = ErrorProcessor.valid_str('type \'y\' to continue and reload from file. otherwise reload will be canceled', YES_NO_LIST)
        if (strAnswer == 'y'):
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        intID, strTitle, strArtist = DataProcessor.add_inventory()

        # 3.3.2 Add item to the table
        DataProcessor.add_to_table(intID, strTitle, strArtist)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = ErrorProcessor.valid_int()
        # 3.5.2 search thru table and delete CD
        IO.delete_CD(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strAnswer = ErrorProcessor.valid_str('Save this inventory to file? [y/n] ', YES_NO_LIST)
        # 3.6.2 Process choice
        if strAnswer == 'y':
            # 3.6.2.1 save data
            fileEmptyInd = FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




