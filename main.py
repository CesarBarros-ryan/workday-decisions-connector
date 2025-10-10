import os
import requests
import xmltodict
import json
import textwrap
import argparse

# Load environment variables from a .env file when python-dotenv is installed.
# This keeps credentials out of source control. If python-dotenv isn't
# available we'll fall back to the current process environment variables.
try:
    from dotenv import load_dotenv, find_dotenv
    # Prefer find_dotenv so we can report the resolved path and failures clearly.
    dotenv_path = find_dotenv()
    if dotenv_path:
        try:
            loaded = load_dotenv(dotenv_path)
            if not loaded:
                print(f"Warning: found .env at {dotenv_path} but load_dotenv returned False")
        except Exception as e:
            print(f"Error loading .env from {dotenv_path}: {e}")
    else:
        # No .env found by find_dotenv; still check for a local .env file and report
        if os.path.exists('.env'):
            try:
                loaded = load_dotenv('.env')
                if not loaded:
                    print("Warning: .env exists but load_dotenv returned False")
            except Exception as e:
                print(f"Error loading local .env: {e}")
        else:
            # No .env file present; that's okay if env vars are provided externally
            pass
except Exception:
    # dotenv isn't installed or failed to import; continue using os.environ
    # We'll not treat this as fatal, but surface a helpful hint below if credentials are missing.
    pass

# --- Workday SOAP API Setup ---
workday_url = os.getenv('WORKDAY_URL', 'https://WD2-IMPL-services1.workday.com/ccx/service/ryan7/Financial_Management/v44.1')
username = os.getenv('WORKDAY_USERNAME', '')
password = os.getenv('WORKDAY_PASSWORD', '')

if not username or not password:
    print("Warning: WORKDAY_USERNAME and/or WORKDAY_PASSWORD are not set.\n"
          "Please create a .env file (see .env.example) or set the environment variables before running the script.")
document_reference = []
worker_reference = []
comment = []
tax_calculation_error_message = []  # Example message
taxable_document_line_reference = []
tax_applicability = []
tax_code_reference = []
withholding_tax_code_reference = []
extended_amount = []
amount_inclusive_of_tax = []
tax_rate_reference = []  # Kept the latest ID
tax_rate_taxable_amount = []
tax_rate_tax_amount = []
tax_rate_percentage = []
tax_recoverability_reference = []  # Kept the latest ID
recoverable_tax_amount = []
non_recoverable_tax_amount = []
tax_recoverable_percentage = []
tax_type_reference = []
third_party_tax_code_identifier = []
jurisdiction = []
tax_rate_reference_id = []  # Kept the latest ID
subject_to_withholding_amount = []
third_party_tax_base_type_reference = []
company_reference = 'dde36542331f1000b66f45813fbd0000'  # Example company reference



def get_search_soap_body():
    """Return the SOAP body used to search for taxable documents."""
    body = textwrap.dedent(f'''<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:wd="urn:com.workday/bsvc"
                      xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
                      xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
                      xmlns:bsvc="urn:com.workday/bsvc">
        <soapenv:Header>
            <wsse:Security soapenv:mustUnderstand="1">
                <wsse:UsernameToken wsu:Id="UsernameToken-1">
                    <wsse:Username>{username}</wsse:Username>
                    <wsse:Password>{password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </soapenv:Header>
        <soapenv:Body>
            <bsvc:Get_Taxable_Document_for_Tax_Calculation_Request xmlns:bsvc="urn:com.workday/bsvc" bsvc:version="v44.1">
                <bsvc:Request_Criteria>
                    <bsvc:Company_Reference bsvc:Descriptor="string">
                        <bsvc:ID bsvc:type="wid">{company_reference}</bsvc:ID>
                    </bsvc:Company_Reference>
                </bsvc:Request_Criteria>
            </bsvc:Get_Taxable_Document_for_Tax_Calculation_Request>
        </soapenv:Body>
    </soapenv:Envelope>''')
    return body

# --- Call Workday API ---
def get_workday_data(soap_body_search_documents):
    """Send the search SOAP request and return the parsed XML as a dict."""
    soaprequest = requests.post(workday_url, data=soap_body_search_documents, headers={"Content-Type": "text/xml"})
    # Provide response body for debugging when non-200
    try:
        soaprequest.raise_for_status()
    except Exception as e:
        try:
            print("Workday search response status:", soaprequest.status_code)
            print("Workday search response body:\n", soaprequest.text)
        except Exception:
            pass
        raise
    request_dict = xmltodict.parse(soaprequest.content)
    print("Search response:", json.dumps(request_dict, indent=4))
    return request_dict


def build_import_body_for_doc_id(doc_id):
    """Build an Import_Taxable_Document_Tax_Details_Request SOAP body for a single document id."""
    def first_or_str(val):
            if isinstance(val, list):
                    return str(val[0]) if val else ''
            if val is None:
                    return ''
            return str(val)

    doc_id_s = first_or_str(doc_id)
    comment_s = first_or_str(comment)
    tax_calc_msg_s = first_or_str(tax_calculation_error_message)

    import_body = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bsvc="urn:com.workday/bsvc">
    <soapenv:Header>
    <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <wsse:UsernameToken>
            <wsse:Username>{username}</wsse:Username>
            <wsse:Password>{password}</wsse:Password>
        </wsse:UsernameToken>
    </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
    <bsvc:Import_Taxable_Document_Tax_Details_Request xmlns:bsvc="urn:com.workday/bsvc" bsvc:version="v44.1">
        <bsvc:Taxable_Document_Reference bsvc:Descriptor="string">
            <bsvc:ID bsvc:type="wid">{doc_id_s}</bsvc:ID>
        </bsvc:Taxable_Document_Reference>
        <bsvc:Business_Process_Parameters>
            <bsvc:Auto_Complete>false</bsvc:Auto_Complete>
            <bsvc:Comment_Data>
                <bsvc:Comment>{comment_s}</bsvc:Comment>
            </bsvc:Comment_Data>
        </bsvc:Business_Process_Parameters>
        <bsvc:Taxable_Document_Tax_Data>
            <bsvc:Tax_Calculation_Error_Message>{tax_calc_msg_s}</bsvc:Tax_Calculation_Error_Message>
            <bsvc:Submit>true</bsvc:Submit>
        </bsvc:Taxable_Document_Tax_Data>
    </bsvc:Import_Taxable_Document_Tax_Details_Request>
    </soapenv:Body>
    </soapenv:Envelope>'''

    return import_body


def post_with_retries(payload, max_retries=3, backoff_sec=2):
    """Post payload to Workday with simple retry/backoff and return parsed response or raise."""
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(workday_url, data=payload, headers={"Content-Type": "text/xml"})
            # If non-200, print status and body to help debugging
            if resp.status_code >= 400:
                try:
                    print(f"Workday import response status: {resp.status_code}")
                    print("Workday import response body:\n", resp.text)
                except Exception:
                    pass
                resp.raise_for_status()
            return xmltodict.parse(resp.content)
        except Exception as e:
            last_exc = e
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                import time
                time.sleep(backoff_sec * attempt)
    raise last_exc


def extract_values_from_search(search_data):
    """Extract values from the Get_Taxable_Document_for_Tax_Calculation search response.

    For each returned document, append a value (or None) to the module-level lists.
    """
    # Locate the list of documents robustly
    env = search_data.get('env:Envelope') or search_data.get('soapenv:Envelope') or search_data
    body = env.get('env:Body') or env.get('soapenv:Body') or env.get('Body') or {}
    resp = body.get('wd:Get_Taxable_Document_for_Tax_Calculation_Response') or body.get('Get_Taxable_Document_for_Tax_Calculation_Response') or {}
    resp_data = resp.get('wd:Response_Data') or resp.get('Response_Data') or {}
    items = resp_data.get('wd:Taxable_Document_for_Tax_Calculation') or resp_data.get('Taxable_Document_for_Tax_Calculation') or []
    
    #save resp to json for debugging
    try:
        with open('search_response.json', 'w', encoding='utf-8') as fh:
            json.dump(items, fh, indent=2)
        print('Wrote search_response.json for debugging')
    except Exception as e:
        print('Failed to write search_response.json:', e)
 
    
    if isinstance(items, dict):
        items = [items]

    # Prepare output lists
    doc_refs = []
    line_refs = []
    company_ids = []
    document_numbers = []
    currency_codes = []
    document_dates = []
    supplier_invoice_numbers = []
    entered_tax_amounts = []
    amount_inclusive_of_taxes = []

    _Taxable_Document_for_Tax_Calculation_Reference = []
    _Company_Reference = []
    _Document_Number = []
    _Currency_Reference = []
    _Document_Date = []

    _Bill_To_Customer_Reference = []
    _Sold_To_Customer_Reference = []
    _Worktags_Reference = []
    _Customer_Category_of_Bill_to_Customer_Reference = []
    _Taxable_Document_Line_for_Tax_Calculation_Data = []
    _Line_Reference_ID = []
    _Company_Reference = []
    _Item_Reference = []
    _Accounting_Category_Reference = []
    _Quantity = []
    _Unit_Cost = []
    _Extended_Amount = []
    _Customer_Invoice_Line_for_Tax_Calculation_Data = []
    _Supplier_Invoice_Line_for_Tax_Calculation_Data = []
    _Supplier_Bill_To_Address_Data = []
    _Address_Format_Type=[]
    _Formatted_Address=[]


    def pick_wid(id_node):
        if isinstance(id_node, list):
            # prefer an entry whose type indicates WID, otherwise first with #text
            for e in id_node:
                if isinstance(e, dict) and (e.get('@wd:type') == 'WID' or e.get('@type') == 'WID'):
                    return e.get('#text')
            for e in id_node:
                if isinstance(e, dict) and '#text' in e:
                    return e.get('#text')
            return None
        if isinstance(id_node, dict):
            return id_node.get('#text')
        if isinstance(id_node, str):
            return id_node
        return None

    # Helper: collect all WID values anywhere under a node
    def collect_wids(node, found=None):
        if found is None:
            found = []
        if isinstance(node, dict):
            # If this node looks like an ID with type attributes, check it
            # Many ID nodes are like {'@wd:type': 'WID', '#text': '...'}
            if ('@wd:type' in node and node.get('@wd:type') == 'WID' and '#text' in node):
                found.append(node.get('#text'))
            if ('@type' in node and node.get('@type') == 'WID' and '#text' in node):
                found.append(node.get('#text'))
            # Recurse into children
            for k, v in node.items():
                if k in ('@wd:type', '@type', '#text'):
                    continue
                collect_wids(v, found)
        elif isinstance(node, list):
            for item in node:
                collect_wids(item, found)
        return found

    for item in items:
        # Document reference WID
        doc_ref_node = item.get('wd:Taxable_Document_for_Tax_Calculation_Reference', {}).get('wd:ID')
        doc_wid = pick_wid(doc_ref_node)
        doc_refs.append(doc_wid)

        # Collect all WIDs present in this document item
        per_doc_wids = collect_wids(item)
        # store per-document WIDs
        # We'll add a list to hold all per-document wid lists later
        # (we'll build a combined list after the loop)
        # append to a temporary list
        if 'document_wids_local' not in locals():
            document_wids_local = []
        document_wids_local.append(per_doc_wids)

        # Header and company
        header = item.get('wd:Taxable_Document_for_Tax_Calculation_Data', {}).get('wd:Taxable_Document_Header_for_Tax_Calculation_Data', {})
        comp_node = header.get('wd:Company_Reference', {}).get('wd:ID')
        comp_wid = pick_wid(comp_node)
        company_ids.append(comp_wid)

        # Document number, currency, date
        document_numbers.append(header.get('wd:Document_Number'))
        # Currency: try to get Currency_ID or Currency code
        curr_node = header.get('wd:Currency_Reference', {}).get('wd:ID')
        currency = None
        if isinstance(curr_node, list):
            for e in curr_node:
                if isinstance(e, dict) and (e.get('@wd:type') == 'Currency_ID' or e.get('@type') == 'Currency_ID' or e.get('@wd:type') == 'Currency_ID'):
                    currency = e.get('#text'); break
            if not currency:
                for e in curr_node:
                    if isinstance(e, dict) and '#text' in e:
                        currency = e.get('#text'); break
        elif isinstance(curr_node, dict):
            currency = curr_node.get('#text')
        currency_codes.append(currency)

        document_dates.append(header.get('wd:Document_Date'))

        # Supplier invoice header
        supplier_hdr = header.get('wd:Supplier_Invoice_Header_for_Tax_Calculation_Data', {})
        supplier_invoice_numbers.append(supplier_hdr.get('wd:Supplier_Invoice_Number'))
        entered_tax_amounts.append(supplier_hdr.get('wd:Entered_Tax_Amount'))
        amount_inclusive_of_taxes.append(supplier_hdr.get('wd:Amount_Inclusive_of_Tax'))

        # Line reference
        line = item.get('wd:Taxable_Document_Line_for_Tax_Calculation_Data', {})
        line_refs.append(line.get('wd:Line_Reference_ID'))

    # Assign to module-level variables (preserve names used earlier)
    global document_reference, taxable_document_line_reference, company_reference, tax_rate_taxable_amount, tax_rate_tax_amount
    # Map extracted lists to variables available in the module
    document_reference = doc_refs
    taxable_document_line_reference = line_refs
    company_reference = company_ids
    # Document-level WIDs (list per document) and flattened all WIDs
    global document_wids, all_wids
    document_wids = document_wids_local if 'document_wids_local' in locals() else []
    # Flatten and dedupe while preserving order
    seen = set()
    all_wids = []
    for lst in document_wids:
        for w in lst:
            if w and w not in seen:
                seen.add(w)
                all_wids.append(w)
    # Additional useful lists (not originally top-level variables) - store under new names
    # Keep original tax fields as empty or None lists (unless present later)
    # Expose some extracted fields for convenience
    global extracted_document_number, extracted_currency, extracted_document_date, extracted_supplier_invoice_number, extracted_entered_tax_amount, extracted_amount_inclusive_of_tax
    extracted_document_number = document_numbers
    extracted_currency = currency_codes
    extracted_document_date = document_dates
    extracted_supplier_invoice_number = supplier_invoice_numbers
    extracted_entered_tax_amount = entered_tax_amounts
    extracted_amount_inclusive_of_tax = amount_inclusive_of_taxes

    # Print a quick summary
    print("Extracted document_reference (WID) count:", len(document_reference))
    print("Extracted taxable_document_line_reference count:", len(taxable_document_line_reference))
    print("Extracted company_reference count:", len(company_reference))
    return {
        'document_reference': document_reference,
        'taxable_document_line_reference': taxable_document_line_reference,
        'company_reference': company_reference,
        'document_wids': document_wids,
        'all_wids': all_wids,
        'document_number': extracted_document_number,
        'currency': extracted_currency,
        'document_date': extracted_document_date,
        'supplier_invoice_number': extracted_supplier_invoice_number,
        'entered_tax_amount': extracted_entered_tax_amount,
        'amount_inclusive_of_tax': extracted_amount_inclusive_of_tax
    }

# --- Transform Data ---
def transform_workday_data(data):
    # Handle the actual response structure we're getting
    try:
        # Check if we have an import process response
        if 'env:Envelope' in data and 'env:Body' in data['env:Envelope']:
            body = data['env:Envelope']['env:Body']
            if 'wd:Put_Import_Process_Response' in body:
                import_ref = body['wd:Put_Import_Process_Response']['wd:Import_Process_Reference']['wd:ID']['#text']
                return {
                    "status": "success",
                    "import_process_id": import_ref,
                    "message": "Tax details import initiated successfully"
                }

        # If it's a different response type, handle accordingly
        return {
            "status": "unknown_response",
            "data": data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": data
        }


def _parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', help='Print SOAP payloads and do not post to Workday')
    return p.parse_args()


def main():
    args = _parse_args()
    # 1) Call Workday to get documents
    try:
        # Use the search SOAP body to retrieve documents
        if args.dry_run:
            search_body = get_search_soap_body()
            print('--- DRY RUN: Search SOAP body ---')
            print(search_body)
            # We can't extract results without a real response, so stop here for dry-run
            print('Dry run complete: no network requests were made.')
            return
        else:
            search_response = get_workday_data(get_search_soap_body())
    except Exception as e:
        print("Failed to get workday data:", str(e))
        raise

    # 2) Transform search response into an import SOAP body
    # Extract fields/lists from the search response
    extracted = extract_values_from_search(search_response)
    # Persist extracted values for auditing/debugging
    try:
        with open('extracted_values.json', 'w', encoding='utf-8') as fh:
            json.dump(extracted, fh, indent=2)
        print('Wrote extracted_values.json')
    except Exception as e:
        print('Failed to persist extracted values:', e)
    # Now build and post an import per document id
    process_ids = []
    for doc_id in extracted['document_reference']:
        if not doc_id:
            print('Skipping empty document id')
            process_ids.append(None)
            continue
        payload = build_import_body_for_doc_id(doc_id)
        print("Built import payload (truncated):", payload[:500])
        try:
            resp = post_with_retries(payload)
            # Use the reusable transformer to interpret the response
            transformed = transform_workday_data(resp)
            pid = transformed.get('import_process_id') if transformed.get('status') == 'success' else None
            process_ids.append(pid)
            print(f"Import posted for {doc_id}, transform status: {transformed.get('status')}, process id: {pid}")
        except Exception as e:
            print(f"Import failed for {doc_id}: {e}")

    print("All import process ids:", process_ids)


if __name__ == '__main__':
    main()

# --- Send to Decisions API ---
'''decisions_url = "https://your-decisions-instance.com/api/flow/trigger"
decisions_headers = {
    "Authorization": "Bearer YOUR_DECISIONS_API_TOKEN",
    "Content-Type": "application/json"
}

decisions_response = requests.post(decisions_url, json=transformed_data, headers=decisions_headers)
decisions_response.raise_for_status()

print("Data sent to Decisions successfully:", decisions_response.json())'''
