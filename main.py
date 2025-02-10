import argparse
from processor import process_csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="Path to the campaign CSV file")
    args = parser.parse_args()
    
    process_csv(args.csv_file)

if __name__ == "__main__":
    main()
