import json
import csv
import pandas as pd

class DataTransformer:
    @staticmethod
    def transform(response):
        """Transform the Workday API response into a structured format."""
        try:
            transformed_data = []
            #step 1 : load up the search_response
            if isinstance(response, str):
                    response = json.loads(response)
            #step 2 : loop through the response and get the taxable document Id and taxable document line Ids
          
            #step 3 : for each line check what the spend category or reveue category is

            #step 4 : check what the country of the client/vendor is

            #step 5 : loop through decisions_data and check if any of the conditions match
            # if match found, assign the tax code and tax rate
            # if no match found, assign default tax code and tax rate

            for item in transformed_data:
                item['tax_code'] = 'DEFAULT_CODE'
                item['tax_rate'] = 0.0  # Default values
            return {
                'status': 'success',
                'data': transformed_data
            }   
  
    
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'data': response
            }
  