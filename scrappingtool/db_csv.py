import csv
import os

import django
from django.conf import settings

from .models import Newsheadline  # Replace with your actual model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Replace 'myproject.settings' with your project's settings module
django.setup()

# Define the CSV file path

def export_to_csv(csv_file_path):

    # Query the database
    data = Newsheadline.objects.all()

    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
        
        # Write the headers (assuming your model has 'field1', 'field2', etc.)
        headers = ['news_title', 'news_source', 'news_upload_date']  # Replace with your actual field names
        csvwriter.writerow(headers)
        
        # Write the data
        for item in data:
            row = [item.field1, item.field2, item.field3]  # Replace with your actual fields
            csvwriter.writerow(row)

    print(f"Data exported to {csv_file_path}")
