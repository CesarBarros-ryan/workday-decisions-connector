import os
import requests
import xmltodict
import json
import argparse
from utils import SOAPBuilder
from workday_api import WorkdayAPI
from data_extractor import DataExtractor
from data_transformer import DataTransformer
from dotenv import load_dotenv

load_dotenv()

workday_url = os.getenv('WORKDAY_URL')
username = os.getenv('WORKDAY_USERNAME')
password = os.getenv('WORKDAY_PASSWORD')
company_reference = 'dde36542331f1000b66f45813fbd0000'  # Example company reference

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Print SOAP payloads and do not post to Workday')
    return parser.parse_args()


def process_documents(workday_api, document_ids):
    process_ids = []
    for doc_id in document_ids:
        if not doc_id:
            print('Skipping empty document ID')
            process_ids.append(None)
            continue

        try:
            payload = SOAPBuilder.build_import_body_for_doc_id(workday_api.username, workday_api.password, doc_id)
            try: 
                response = workday_api.post_with_retries( payload, max_retries=3, backoff_sec=2)
            except Exception as e:
                print(f'Failed to post document {doc_id}: {e}')
                process_ids.append(None)
                continue
            process_ids.append(response.get('import_process_id'))
        except Exception as e:
            print(f'Error processing document {doc_id}: {e}')
            process_ids.append(None)

    return process_ids


def main():

    workday_api = WorkdayAPI(username=username, password=password, url=workday_url)

    args = _parse_args()

    if args.dry_run:
        search_body = SOAPBuilder.get_search_soap_body(username, password, company_reference)
        print('--- DRY RUN: Search SOAP body ---')
        print(search_body)
        print('Dry run complete: no network requests were made.')
        return

    try:
        search_response = workday_api.get_search_data()
        extracted_data = DataExtractor.extract_values(search_response)

        with open('extracted_values.json', 'w', encoding='utf-8') as fh:
            json.dump(extracted_data, fh, indent=2)
        print('Wrote extracted_values.json')

        process_ids = []
        counter = 0
        for doc_id in extracted_data['document_wids']:
            print("Processing document WID:", counter)
            counter += 1
            third_party_tax_code_identifier = 0 #extracted_data['third_party_tax_code_identifier'][counter - 1] or ''
            jurisdiction = 0 #extracted_data['jurisdictions'][counter - 1] or ''
            tax_rate_reference = '42259d037f4e1001632cc3b194160000' #extracted_data['tax_rate_references'][counter - 1] or ''
            tax_rate_taxable_amount = 9600 #extracted_data['tax_rate_taxable_amounts'][counter - 1] or '0.00'
            subject_to_withholding_amount = 9600 #extracted_data['subject_to_withholding_amounts'][counter - 1] or '0.00'
            tax_rate_tax_amount = 960 #extracted_data['tax_rate_tax_amounts'][counter - 1] or '0.00'
            tax_rate_percentage = 10 #extracted_data['tax_rate_percentages'][counter - 1] or '0.00'
            taxable_document_reference = '684f19edf0eb90011d68b6cc78330000' #extracted_data['taxable_document_references'][counter - 1] or ''
            taxable_document_line_reference = '39d8593a214590011d4c0b63c94a0000' #extracted_data['taxable_document_line_references'][counter -  1] or ''
            tax_applicability_reference = 0 #extracted_data['tax_applicability_references'][counter - 1] or ''
            tax_code_reference = 0 #extracted_data['tax_code_references'][counter - 1] or ''
            withholding_tax_code_reference = '796aa1abab5810016319baa917f40000' #extracted_data['withholding_tax_code_references'][counter - 1] or ''
            autocomplete = 'false'  # or 'true' based on your requirement
            third_party_tax_base_type_reference = 0 #extracted_data['third_party_tax_base_type_references'][counter - 1] or ''
            worker_reference = 0 #extracted_data['worker_references'][counter - 1] or ''
            extended_amount = 0 #extracted_data['extended_amounts'][counter - 1] or '0.00'
            amount_inclusive_of_tax =  0 #extracted_data['amount_inclusive_of_taxes'][counter - 1] or '0.00'
            tax_recoverability_reference = 0 #extracted_data['tax_recoverability_references'][counter - 1] or ''
            recoverable_tax_amount = 0 #extracted_data['recoverable_tax_amounts'][counter - 1] or '0.00'
            non_recoverable_tax_amount = 0 #extracted_data['non_recoverable_tax_amounts'][ counter - 1] or '0.00'
            tax_recoverable_percentage = 0 #extracted_data['tax_recoverable_percentages'][counter - 1] or '0.00'
            tax_type_reference = 0 #extracted_data['tax_type_references'][counter - 1] or ''

            if not doc_id:
                print('Skipping empty document id')
                process_ids.append(None)
                continue
            payload = SOAPBuilder.build_import_body_for_doc_id(
                username,
                password,
                
                "Processed via script",  # comment
                "No issues",  # tax_calc_msg
                
                third_party_tax_code_identifier,
                jurisdiction,
                tax_rate_reference,
                tax_rate_taxable_amount,
                subject_to_withholding_amount,
                tax_rate_tax_amount,
                tax_rate_percentage,
                taxable_document_reference,
                taxable_document_line_reference,
                tax_applicability_reference,
                tax_code_reference,
                withholding_tax_code_reference,
                autocomplete,
                worker_reference,
                extended_amount,
                amount_inclusive_of_tax,
                tax_recoverability_reference,
                recoverable_tax_amount,
                non_recoverable_tax_amount,
                tax_recoverable_percentage,
                tax_type_reference,
                third_party_tax_base_type_reference
            )
            #print("Built import payload (truncated):", payload[:50000])
            try:
                resp = workday_api.post_with_retries(payload)
                # Use the reusable transformer to interpret the response
                print("Response (truncated):", resp[:5000])

                # Extract WID from the response
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(resp)
                    namespaces = {
                        'env': 'http://schemas.xmlsoap.org/soap/envelope/',
                        'wd': 'urn:com.workday/bsvc'
                    }
                    wid_element = root.find('.//wd:ID[@wd:type="WID"]', namespaces)
                    wid = wid_element.text if wid_element is not None else None
                    print("Extracted WID:", wid)
                except ET.ParseError as e:
                    print(f"Error parsing XML response: {e}")
                    wid = None

                transformed = DataTransformer.transform(resp)
                pid = transformed.get('import_process_id') if transformed.get('status') == 'success' else None
                process_ids.append(wid if wid else pid)
            # print(f"Import posted for {doc_id}, transform status: {transformed.get('status')}, process id: {pid}")
            except Exception as e:
                print(f"Import failed for {doc_id}: {e}")

        print("All import process ids:", process_ids)


    except Exception as e:
        print(f'Error during processing: {e}')


if __name__ == '__main__':
    main()
