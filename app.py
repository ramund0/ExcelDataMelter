import sys 
import getopt 
import pandas as pd

opts, args = getopt.getopt(sys.argv[1:], "i:o:s:")


def __get_data_from_xlsx_file(file_path: str, sheet_number=0) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_number)
    return df

def __data_from_3d_to_2d(df:pd.DataFrame, columns_to_keep:list, var_name:str) -> pd.DataFrame:
    df = pd.melt(df, id_vars=columns_to_keep, var_name=var_name)
    return df


def __get_interval_dates() -> tuple:
    starting_date = str(input("Enter starting date: "))
    ending_date = str(input("Enter the ending date:"))
    return (starting_date, ending_date)



def __get_dataframe_between_dates(df:pd.DataFrame, dates_interval: tuple):
    df = df[(df['Date'] > dates_interval[0]) & (df['date'] <= dates_interval[1])]
    return df

            


def __give_options_to_split_current_large_dataframe(df:pd.DataFrame):
    print(f"The sheet is too large! Your sheet has {len(df.index)} rows when Max size is 1048576")
    print("You can try and select one of the following options: ")
    print(f"""
            1. Divide dataframe in {len(df.index//1048576)} sheets
            2. Provide a date interval 
            3. Provide a row to start truncating the data from 
            4. Exit
            """
            )

    question_result = str(input("Enter option: "))
    if question_result == '1':
        print("Divide all the things")
    elif question_result == '2':
        print("What date would you like to start from (input as dd/mm/yyyy)")
    else: 
        sys.exit()

def __write_dataframe_to_output_file(df:pd.DataFrame, file_path: str):
    writer = pd.ExcelWriter(file_path)
    number_of_rows = len(df.index)

    if number_of_rows > 1048576: 
        __give_options_to_split_current_large_dataframe(df)
    else:
        df.to_excel(writer)
        writer.save()
        print(f"DataFrame is written successfully to Excel File {file_path}")


if __name__ =='__main__':
    for opt,arg in opts:
        if opt == '-i':
            input_file = arg
        if opt == '-o':
            output_file = arg
        if opt == '-s':
            sheet_number = int(arg)

    list_of_columns = []
    list_of_columns = [item for item in input("Enter the names of the columns that you wish to keep separated by a space: ").split()]
    var_name = input("Enter the name of the column that you wish to get the data from: ")
    df = __get_data_from_xlsx_file(input_file, sheet_number)
    df = __data_from_3d_to_2d(df, list_of_columns, var_name)
    try:
        __write_dataframe_to_output_file(df, output_file)
    except ValueError: 
        print (f"The sheet is too large! Your sheet has {len(df.index)} rows when Max size is 1048576")
        
    





