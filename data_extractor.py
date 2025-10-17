import json

class DataExtractor:
    @staticmethod

    def extract_values(search_data):
        """Extract values from the Get_Taxable_Document_for_Tax_Calculation search response.

        For each returned document, append a value (or None) to the module-level lists.
        """
        # Step 1: Locate the list of documents robustly
        # Navigate through the SOAP response structure to find the list of documents.
        env = search_data.get('env:Envelope') or search_data.get('soapenv:Envelope') or search_data
        body = env.get('env:Body') or env.get('soapenv:Body') or env.get('Body') or {}
        resp = body.get('wd:Get_Taxable_Document_for_Tax_Calculation_Response') or body.get('Get_Taxable_Document_for_Tax_Calculation_Response') or {}
        resp_data = resp.get('wd:Response_Data') or resp.get('Response_Data') or {}
        items = resp_data.get('wd:Taxable_Document_for_Tax_Calculation') or resp_data.get('Taxable_Document_for_Tax_Calculation') or []

        # Step 2: Save the response to a JSON file for debugging
        try:
            with open('search_response.json', 'w', encoding='utf-8') as fh:
                json.dump(items, fh, indent=2)
            print('Wrote search_response.json for debugging')
        except Exception as e:
            print('Failed to write search_response.json:', e)

        # Step 3: Ensure the items are in list format
        if isinstance(items, dict):
            items = [items]

        # Step 4: Prepare output lists to store extracted values
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


        # Step 5: Define helper functions for extracting and collecting WIDs
        def pick_wid(id_node, target_list):
            """Extract a WID from a node and append it to the target list."""
            if isinstance(id_node, list):
                for e in id_node:
                    if isinstance(e, dict) and (e.get('@wd:type') == 'WID' or e.get('@type') == 'WID'):
                        target_list.append(e.get('#text'))
                        return e.get('#text')
                    for e in id_node:
                        if isinstance(e, dict) and '#text' in e:
                            target_list.append(e.get('#text'))
                            return e.get('#text')
                return None
            if isinstance(id_node, dict):
                target_list.append(id_node.get('#text'))
                return id_node.get('#text')
            if isinstance(id_node, str):
                target_list.append(id_node)
                return id_node
            return None

        def collect_wids(node, found=None, parent_tag=None, grandparent_tag=None):
            """Recursively collect all WID values from a node and save them in lists matching the grandparent tag name.
            Filters values based on specific attributes like '@wd:type'.
            """
            if found is None:
                found = {}
            if isinstance(node, dict):
                if ('@wd:type' in node and '#text' in node):
                    # Save values based on the grandparent tag
                    key = f"{grandparent_tag}_{node.get('@wd:type')}"
                    if key not in found:
                        found[key] = []
                    found[key].append(node.get('#text'))
                for k, v in node.items():
                    if k in ('@wd:type', '@type', '#text'):
                        continue
                    collect_wids(v, found, parent_tag=k, grandparent_tag=parent_tag)
            elif isinstance(node, list):
                for item in node:
                    collect_wids(item, found, parent_tag=parent_tag, grandparent_tag=grandparent_tag)
            return found

        # Step 6: Iterate over each document and extract values
        for item in items:
            # Extract document reference WID
            doc_ref_node = item.get('wd:Taxable_Document_for_Tax_Calculation_Reference', {}).get('wd:ID')
            print("Document Reference Node:", doc_ref_node)
            doc_wid = pick_wid(doc_ref_node, _Taxable_Document_for_Tax_Calculation_Reference)
            #doc_refs.append(doc_wid)
            print("Document WID:", doc_ref_node)
            collect_wids(doc_wid)

            # Collect all WIDs present in this document
            per_doc_wids = collect_wids(item)
            if 'document_wids_local' not in locals():
                document_wids_local = []
            document_wids_local.append(per_doc_wids)

            # Extract header and company information
            header = item.get('wd:Taxable_Document_for_Tax_Calculation_Data', {}).get('wd:Taxable_Document_Header_for_Tax_Calculation_Data', {})
            comp_node = header.get('wd:Company_Reference', {}).get('wd:ID')
            comp_wid = pick_wid(comp_node, _Company_Reference)
            collect_wids(comp_wid)
            #company_ids.append(comp_wid)

            # Extract document metadata
            document_numbers= header.get('wd:Document_Number')
            collect_wids(document_numbers)

            curr_node = header.get('wd:Currency_Reference', {}).get('wd:ID')
            currency = None
            if isinstance(curr_node, list):
                for e in curr_node:
                    if isinstance(e, dict) and (e.get('@wd:type') == 'Currency_ID' or e.get('@type') == 'Currency_ID'):
                        currency = e.get('#text'); break
                if not currency:
                    for e in curr_node:
                        if isinstance(e, dict) and '#text' in e:
                            currency = e.get('#text'); break
            elif isinstance(curr_node, dict):
                currency = curr_node.get('#text')
            #currency_codes.append(currency)
            collect_wids(currency)

            document_Date = header.get('wd:Document_Date')
            collect_wids(document_Date)
            #document_dates.append(header.get('wd:Document_Date'))

        # Step 7: Assign extracted values to module-level variables
        global document_reference, taxable_document_line_reference, company_reference, tax_rate_taxable_amount, tax_rate_tax_amount
        document_reference = doc_refs
        taxable_document_line_reference = line_refs
        company_reference = company_ids

        # Step 8: Flatten and deduplicate WIDs
        global document_wids, all_wids
        document_wids = document_wids_local if 'document_wids_local' in locals() else []
        seen = set()
    #    all_wids = []
        for lst in document_wids:
            for w in lst:
                if w and w not in seen:
                    seen.add(w)
    #                all_wids.append(w)

        # Step 9: Expose additional extracted fields
    #    global extracted_document_number, extracted_currency, extracted_document_date, extracted_supplier_invoice_number, extracted_entered_tax_amount, extracted_amount_inclusive_of_tax
    #    extracted_document_number = document_numbers
    #    extracted_currency = currency_codes
    #    extracted_document_date = document_dates
    #    extracted_supplier_invoice_number = supplier_invoice_numbers
    #    extracted_entered_tax_amount = entered_tax_amounts
    #    extracted_amount_inclusive_of_tax = amount_inclusive_of_taxes

        # Step 10: Print a quick summary of extracted values
        print("Extracted document_reference (WID) count:", len(document_reference))
        print("Extracted taxable_document_line_reference count:", len(taxable_document_line_reference))
        print("Extracted company_reference count:", len(company_reference))

        # Step 11: Return extracted data as a dictionary
        return {
    #        'document_reference': document_reference,
    #        'taxable_document_line_reference': taxable_document_line_reference,
    #        'company_reference': company_reference,
            'document_wids': document_wids,
    #        'all_wids': all_wids,
    #        'document_number': extracted_document_number,
    #        'currency': extracted_currency,
    #        'document_date': extracted_document_date,
    #        'supplier_invoice_number': extracted_supplier_invoice_number,
    #        'entered_tax_amount': extracted_entered_tax_amount,
    #        'amount_inclusive_of_tax': extracted_amount_inclusive_of_tax
        }
