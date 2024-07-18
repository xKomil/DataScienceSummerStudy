# Data cleaning
So today i was learning how to clean dataset from this tutorial: https://www.youtube.com/watch?v=bDhvCp3_lYw
I think its a great creator because understanding this tutorial was very easy, messages were presented clearly and i enjoyed it. 

1. erasing the dupplicates but before look up why there are duplicates
2. drop useless columns
3. using .strip() 
4. if we want to change only in one column we need to call it like that df['Last_Name'] = df['Last_Name'].str.lstrip('...')
5. filling None value with df.fillna('')
6. dropping rows with specific column with none value: df = df.dropna(subset='Phone_Number', inplace=True)