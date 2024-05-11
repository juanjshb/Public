from query import runqry
from datetime import datetime

# Example query
query = """
SELECT * FROM your_table;
"""

cdate = datetime.now().strftime("%Y%m%d")
custom_file_name = "B2B_123456_FILE"
result = runqry(query)

if result:
    file_name = f"{custom_file_name}_{cdate}.txt"
    with open(file_name, "w") as f:
        for row in result:
            f.write('|'.join(map(str, row)) + '\n')
    print(f"Query results exported to {file_name}")
else:
    print("Error executing query.")