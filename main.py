import requests
import xmltodict
import json

# --- Workday SOAP API Setup ---
workday_url = "https://WD2-IMPL-services1.workday.com/ccx/service/ryan7/Financial_Management/v44.1"
username = "RC08492@ryan7"
password = "Monday30!!"
document_reference = "dde36542331f1000b66f45813fbd0000"
worker_reference = "b3f8d5e4a3b21100b66"
comment = "Importing tax details"
tax_calculation_error_message = "No errors"  # Example message
taxable_document_line_reference = "line-ref-001"
tax_applicability = "applicability-ref-001"
tax_code_reference = "tax-code-ref-001"
withholding_tax_code_reference = "withholding-tax-code-ref-001"
extended_amount = "1000.00"
amount_inclusive_of_tax = "1100.00"
tax_rate_reference = "tax-rate-ref-002"  # Kept the latest ID
tax_rate_taxable_amount = "1000.00"
tax_rate_tax_amount = "100.00"
tax_rate_percentage = "10.00"
tax_recoverability_reference = "recoverability-ref-002"  # Kept the latest ID
recoverable_tax_amount = "80.00"
non_recoverable_tax_amount = "20.00"
tax_recoverable_percentage = "80.00"
tax_type_reference = "tax-type-ref-001"
third_party_tax_code_identifier = "TP123"
jurisdiction = "NY"
tax_rate_reference_id = "tax-rate-ref-002"  # Kept the latest ID
subject_to_withholding_amount = "500.00"
third_party_tax_base_type_reference = "base-type-ref-001"
company_reference = "dde36542331f1000b66f45813fbd0000"  # Example company reference



soap_body = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bsvc="urn:com.workday/bsvc">
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
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{document_reference}</bsvc:ID>
</bsvc:Taxable_Document_Reference>
<!-- Optional: -->
<bsvc:Business_Process_Parameters>
<!-- Optional: -->
<bsvc:Auto_Complete>false</bsvc:Auto_Complete>
<!-- Optional: -->
<bsvc:Comment_Data>
<!-- Optional: -->
<bsvc:Comment>{comment}</bsvc:Comment>
<!-- Optional: -->
<bsvc:Worker_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{worker_reference}</bsvc:ID>
</bsvc:Worker_Reference>
</bsvc:Comment_Data>
</bsvc:Business_Process_Parameters>
<!-- Optional: -->
<bsvc:Taxable_Document_Tax_Data>
<!-- Optional: -->
<bsvc:Tax_Calculation_Error_Message>{tax_calculation_error_message}</bsvc:Tax_Calculation_Error_Message>
<!-- Optional: -->
<bsvc:Submit>true</bsvc:Submit>
<!-- Zero or more repetitions: -->
<bsvc:Taxable_Document_Line_Tax_Data>
<bsvc:Taxable_Document_Line_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{taxable_document_line_reference}</bsvc:ID>
</bsvc:Taxable_Document_Line_Reference>
<!-- Optional: -->
<bsvc:Tax_Applicability_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{tax_applicability}</bsvc:ID>
</bsvc:Tax_Applicability_Reference>
<!-- Optional: -->
<bsvc:Tax_Code_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{tax_code_reference}</bsvc:ID>
</bsvc:Tax_Code_Reference>
<!-- Optional: -->
<bsvc:Withholding_Tax_Code_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{withholding_tax_code_reference}</bsvc:ID>
</bsvc:Withholding_Tax_Code_Reference>
<!-- Optional: -->
<bsvc:Extended_Amount>{extended_amount}</bsvc:Extended_Amount>
<!-- Optional: -->
<bsvc:Amount_Inclusive_of_Tax>{amount_inclusive_of_tax}</bsvc:Amount_Inclusive_of_Tax>
<!-- Zero or more repetitions: -->
<bsvc:Taxable_Document_Line_Tax_Rate_Data>
<bsvc:Tax_Rate_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{tax_rate_reference}</bsvc:ID>
</bsvc:Tax_Rate_Reference>
<!-- Optional: -->
<bsvc:Tax_Rate_Taxable_Amount>{tax_rate_taxable_amount}</bsvc:Tax_Rate_Taxable_Amount>
<!-- Optional: -->
<bsvc:Tax_Rate_Tax_Amount>{tax_rate_tax_amount}</bsvc:Tax_Rate_Tax_Amount>
<!-- Optional: -->
<bsvc:Tax_Rate_Percentage>{tax_rate_percentage}</bsvc:Tax_Rate_Percentage>
<!-- Optional: -->
<bsvc:Tax_Recoverability_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{tax_recoverability_reference}</bsvc:ID>
</bsvc:Tax_Recoverability_Reference>
<!-- Optional: -->
<bsvc:Recoverable_Tax_Amount>{recoverable_tax_amount}</bsvc:Recoverable_Tax_Amount>
<!-- Optional: -->
<bsvc:Non_Recoverable_Tax_Amount>{non_recoverable_tax_amount}</bsvc:Non_Recoverable_Tax_Amount>
<!-- Optional: -->
<bsvc:Tax_Recoverable_Percentage>{tax_recoverable_percentage}</bsvc:Tax_Recoverable_Percentage>
<!-- Optional: -->
<bsvc:Tax_Type_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{tax_type_reference}</bsvc:ID>
</bsvc:Tax_Type_Reference>
<!-- Optional: -->
<bsvc:Third_Party_Tax_Code_Identifier>{third_party_tax_code_identifier}</bsvc:Third_Party_Tax_Code_Identifier>
<!-- Optional: -->
<bsvc:Jurisdiction>{jurisdiction}</bsvc:Jurisdiction>
</bsvc:Taxable_Document_Line_Tax_Rate_Data>
<!-- Zero or more repetitions: -->
<bsvc:Taxable_Document_Line_Withholding_Tax_Rate_Data>
<bsvc:Tax_Rate_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{tax_rate_reference_id}</bsvc:ID>
</bsvc:Tax_Rate_Reference>
<!-- Optional: -->
<bsvc:Tax_Rate_Taxable_Amount>{tax_rate_taxable_amount}</bsvc:Tax_Rate_Taxable_Amount>
<!-- Optional: -->
<bsvc:Subject_To_Withholding_Amount>{subject_to_withholding_amount}</bsvc:Subject_To_Withholding_Amount>
<!-- Optional: -->
<bsvc:Tax_Rate_Tax_Amount>{tax_rate_tax_amount}</bsvc:Tax_Rate_Tax_Amount>
<!-- Optional: -->
<bsvc:Tax_Rate_Percentage>{tax_rate_percentage}</bsvc:Tax_Rate_Percentage>
<!-- Optional: -->
<bsvc:Third_Party_Tax_Code_Identifier>{third_party_tax_code_identifier}</bsvc:Third_Party_Tax_Code_Identifier>
<!-- Optional: -->
<bsvc:Jurisdiction>{jurisdiction}</bsvc:Jurisdiction>
+
<!-- Optional: -->
<bsvc:Third_Party_Tax_Base_Type_Reference bsvc:Descriptor="string">
<!-- Zero or more repetitions: -->
<bsvc:ID bsvc:type="wid">{third_party_tax_base_type_reference}</bsvc:ID>
</bsvc:Third_Party_Tax_Base_Type_Reference>
</bsvc:Taxable_Document_Line_Withholding_Tax_Rate_Data>
</bsvc:Taxable_Document_Line_Tax_Data>
</bsvc:Taxable_Document_Tax_Data>
</bsvc:Import_Taxable_Document_Tax_Details_Request>
  </soapenv:Body>
</soapenv:Envelope>
"""

soap_body_search_documents = f'''<?xml version="1.0" encoding="UTF-8"?>
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
                <!-- Zero or more repetitions: -->
                <bsvc:Company_Reference bsvc:Descriptor="string">
                    <!-- Zero or more repetitions: -->
                    <bsvc:ID bsvc:type="wid">{company_reference}</bsvc:ID>
                </bsvc:Company_Reference>
            </bsvc:Request_Criteria>
        </bsvc:Get_Taxable_Document_for_Tax_Calculation_Request>
    </soapenv:Body>
</soapenv:Envelope>
'''

# --- Call Workday API ---
def get_workday_data(soap_body_search_documents):
    """Send the search SOAP request and return the parsed XML as a dict."""
    soaprequest = requests.post(workday_url, data=soap_body_search_documents, headers={"Content-Type": "text/xml"})
    soaprequest.raise_for_status()
    request_dict = xmltodict.parse(soaprequest.content)
    print("Search response:", json.dumps(request_dict, indent=4))
    return request_dict


def post_to_workday(soap_body):
    """Post an import SOAP payload to Workday and return the parsed response dict."""
    response = requests.post(workday_url, data=soap_body, headers={"Content-Type": "text/xml"})
    response.raise_for_status()
    data_dict = xmltodict.parse(response.content)
    print("Import response:", json.dumps(data_dict, indent=4))
    return data_dict


def build_import_soap_body_from_search(search_data):
    """Create a compact Import_Taxable_Document_Tax_Details_Request SOAP body from search results.

    This finds a document ID in the search response and builds an import payload that references it.
    If none found, falls back to `document_reference`.
    """
    def find_first_id(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.endswith(':ID') or k == 'ID' or k.endswith(':Id'):
                    if isinstance(v, dict):
                        if '#text' in v:
                            return v['#text']
                        for vv in v.values():
                            if isinstance(vv, str):
                                return vv
                    elif isinstance(v, str):
                        return v
                res = find_first_id(v)
                if res:
                    return res
        elif isinstance(obj, list):
            for item in obj:
                res = find_first_id(item)
                if res:
                    return res
        return None

    doc_id = find_first_id(search_data) or document_reference

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
        <bsvc:ID bsvc:type="wid">{doc_id}</bsvc:ID>
      </bsvc:Taxable_Document_Reference>
      <bsvc:Business_Process_Parameters>
        <bsvc:Auto_Complete>false</bsvc:Auto_Complete>
        <bsvc:Comment_Data>
          <bsvc:Comment>{comment}</bsvc:Comment>
        </bsvc:Comment_Data>
      </bsvc:Business_Process_Parameters>
      <bsvc:Taxable_Document_Tax_Data>
        <bsvc:Tax_Calculation_Error_Message>{tax_calculation_error_message}</bsvc:Tax_Calculation_Error_Message>
        <bsvc:Submit>true</bsvc:Submit>
      </bsvc:Taxable_Document_Tax_Data>
    </bsvc:Import_Taxable_Document_Tax_Details_Request>
  </soapenv:Body>
</soapenv:Envelope>'''

    return import_body


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


if __name__ == '__main__':
    # 1) Call Workday to get documents
    try:
        search_response = get_workday_data(soap_body_search_documents)
    except Exception as e:
        print("Failed to get workday data:", str(e))
        raise

    # 2) Transform search response into an import SOAP body
    import_payload = build_import_soap_body_from_search(search_response)
    print("Built import payload (truncated):", import_payload[:1000])

    # 3) Post import payload to Workday
    try:
        import_response = post_to_workday(import_payload)
    except Exception as e:
        print("Failed to post import payload:", str(e))
        raise

    # 4) Interpret the import response
    result = transform_workday_data(import_response)
    print("Final result:", json.dumps(result, indent=2))

# --- Send to Decisions API ---
'''decisions_url = "https://your-decisions-instance.com/api/flow/trigger"
decisions_headers = {
    "Authorization": "Bearer YOUR_DECISIONS_API_TOKEN",
    "Content-Type": "application/json"
}

decisions_response = requests.post(decisions_url, json=transformed_data, headers=decisions_headers)
decisions_response.raise_for_status()

print("Data sent to Decisions successfully:", decisions_response.json())'''
