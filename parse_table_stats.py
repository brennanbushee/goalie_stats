# File: parse_table_with_name.py

from bs4 import BeautifulSoup
import csv

# Function to extract player name from nested table
def extract_name(th):
    # Locate the nested <td> containing the player's name
    name_cell = th.find('td', style="text-align:left;")
    return name_cell.text.strip() if name_cell else None

# Function to parse HTML table
def parse_html_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract headers
    headers = [th.text.strip() for th in soup.find("thead").find_all("th")]
    headers.remove('Name')
    # Identify column indices
    target_columns = [
        "xGAA",
        "GAA Better Than Expected",
        "Wins Above Replacement",
        "High Danger Unblocked Shot Attempt Save % Above Expected"
    ]
    target_columns.sort()
    col_indices = {col: headers.index(col) for col in target_columns}

    # Extract table rows
    data = {}
    rows = soup.find("tbody").find_all('tr')


    for row in rows:  # Skip header row
        name_th = row.find("th")
        name = extract_name(name_th) if name_th else "Unknown"
        cells = row.find_all_next('td')[3:]
        if cells:
            # Find the "Name" field in the corresponding <th> tag
            # Extract required columns
            # data.update({col: cells[idx].text.strip() for col, idx in col_indices.items()})
            data[name] = {col: cells[idx].text.strip() for col, idx in col_indices.items()}

    return data


# Function to save extracted data into a CSV file
def save_to_csv(data, filename='extracted_stats_with_names_12_13.csv'):
    target_columns = [
        "Name",
        "High Danger Unblocked Shot Attempt Save % Above Expected",
        "GAA Better Than Expected",
        "Wins Above Replacement",
        "xGAA"
    ]
    if data:
        flat_data  = flatten_dict(data)
        keys = flat_data[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(flat_data)

    # File: flatten_dict_to_list.py

def flatten_dict(input_dict):
    # Convert dict of dicts into a flat list of dicts
    return [{'Name': key, **value} for key, value in input_dict.items()]




# Example usage
if __name__ == "__main__":
    # Example input
    data = {
        'Tim Thomas': {
            'High Danger Unblocked Shot Attempt Save % Above Expected': '0.651',
            'GAA Better Than Expected': '2.70',
            'Wins Above Replacement': '0.71',
            'xGAA': '2.00'
        }
    }

    # Flatten the input
    flattened_data = flatten_dict(data)

    # Print result
    print(flattened_data)
    # Read HTML content from a file
    #seasons = ['2012_13', '2013_14', '2014_15', '2015_16', '2016_17', '2016_17', '2017_18', '2018_19', '2019_20', '2020_21', '2021_22', '2022_23', '2023_24']
    seasons = ['2022_23', '2021_22']
    for season in seasons:

        with open('data/team_xgf_table_' + season, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the table and extract data
        extracted_data = parse_html_table(html_content)

        # Save to CSV
        csv_name = 'extracted_stats_with_names_' + season + '.csv'
        save_to_csv(extracted_data, filename=csv_name)
        print(f"Data extraction complete. Check '{csv_name}'.")
