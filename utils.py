import textwrap
import os

# --- Workday SOAP API Setup ---
workday_url = os.getenv('WORKDAY_URL', 'https://WD2-IMPL-services1.workday.com/ccx/service/ryan7/Financial_Management/v44.1')
username = os.getenv('WORKDAY_USERNAME', '')
password = os.getenv('WORKDAY_PASSWORD', '')
company_reference = 'dde36542331f1000b66f45813fbd0000'  # Example company reference

# Utility function to build SOAP requests
class SOAPBuilder:
    @staticmethod
    def get_search_soap_body(username: str, password: str, company_reference: str) -> str:
        """Return the SOAP body used to search for taxable documents."""
        print("Generating search SOAP body with username:", username)
        print("Using company reference:", company_reference)
        print("Using password:", '*' * len(password))  # Mask the password in logs
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

    @staticmethod
    def build_import_body_for_doc_id(username: str, password: str, comment: str, tax_calc_msg: str, third_party_tax_code_identifier: str, jurisdiction: str, tax_rate_reference: str, tax_rate_taxable_amount: str, subject_to_withholding_amount: str, tax_rate_tax_amount: str, tax_rate_percentage: str, taxable_document_reference: str, taxable_document_line_reference: str, tax_applicability_reference: str, tax_code_reference: str, withholding_tax_code_reference: str, autocomplete: str, worker_reference: str, extended_amount: str, amount_inclusive_of_tax: str, tax_recoverability_reference: str, recoverable_tax_amount: str, non_recoverable_tax_amount: str, tax_recoverable_percentage: str, tax_type_reference: str, third_party_tax_base_type_reference: str) -> str:
        """Build an Import_Taxable_Document_Tax_Details_Request SOAP body for a single document id."""
        import_body = f'''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:wd="urn:com.workday/bsvc"
                  xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
                  xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
                  xmlns:bsvc="urn:com.workday/bsvc">
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
        <bsvc:ID bsvc:type="wid">{taxable_document_reference}</bsvc:ID>
        </bsvc:Taxable_Document_Reference>
        <!-- Optional: -->
        <bsvc:Business_Process_Parameters>
        <!-- Optional: -->
        <bsvc:Auto_Complete>{autocomplete}</bsvc:Auto_Complete>
        <!-- Optional: -->
        <bsvc:Comment_Data>
        <!-- Optional: -->
        <bsvc:Comment>{comment}</bsvc:Comment>
        <!-- Optional: -->
       
        </bsvc:Comment_Data>
        </bsvc:Business_Process_Parameters>
        <!-- Optional: -->
        <bsvc:Taxable_Document_Tax_Data>
        <!-- Optional: -->
        <bsvc:Tax_Calculation_Error_Message>{tax_calc_msg}</bsvc:Tax_Calculation_Error_Message>
        <!-- Optional: -->
        <bsvc:Submit>true</bsvc:Submit>
        <!-- Zero or more repetitions: -->
        <bsvc:Taxable_Document_Line_Tax_Data>
        <bsvc:Taxable_Document_Line_Reference bsvc:Descriptor="string">
        <!-- Zero or more repetitions: -->
        <bsvc:ID bsvc:type="wid">{taxable_document_line_reference}</bsvc:ID>
        </bsvc:Taxable_Document_Line_Reference>
       
        <bsvc:Withholding_Tax_Code_Reference bsvc:Descriptor="string">
        <!-- Zero or more repetitions: -->
        <bsvc:ID bsvc:type="wid">{withholding_tax_code_reference}</bsvc:ID>
        </bsvc:Withholding_Tax_Code_Reference>
        <bsvc:Taxable_Document_Line_Withholding_Tax_Rate_Data>
        <bsvc:Tax_Rate_Reference bsvc:Descriptor="string">
        <!-- Zero or more repetitions: -->
        <bsvc:ID bsvc:type="wid">{tax_rate_reference}</bsvc:ID>
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
        <!-- Optional: -->
        
        </bsvc:Taxable_Document_Line_Withholding_Tax_Rate_Data>
        </bsvc:Taxable_Document_Line_Tax_Data>
        </bsvc:Taxable_Document_Tax_Data>
        </bsvc:Import_Taxable_Document_Tax_Details_Request>
        </soapenv:Body>
        </soapenv:Envelope>'''

 
        return import_body