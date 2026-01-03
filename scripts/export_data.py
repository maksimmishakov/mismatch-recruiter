import json
import csv
from datetime import datetime

class DataExporter:
    @staticmethod
    def export_to_json(data: list, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Exported {len(data)} items to {filename}")
    
    @staticmethod
    def export_to_csv(data: list, filename: str) -> None:
        if not data:
            return
        
        keys = data[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Exported {len(data)} items to {filename}")
    
    @staticmethod
    def backup_database(db_path: str) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"db_backup_{timestamp}.sql"
        print(f"Database backup created: {backup_name}")
        return backup_name

if __name__ == '__main__':
    exporter = DataExporter()
    sample_data = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
    exporter.export_to_json(sample_data, 'test.json')
    exporter.export_to_csv(sample_data, 'test.csv')
