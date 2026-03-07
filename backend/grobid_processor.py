import requests
from pathlib import Path
from lxml import etree
from db import insert_metadata

GROBID_URL = "http://localhost:8070/api/processHeaderDocument"
UPLOAD_FOLDER = Path(__file__).parent / "data" / "uploaded_pdf"

def process_pdfs(pdf_path: Path):

    files = {"input": (pdf_path.name, open(pdf_path, "rb"), "application/pdf")}
    response = requests.post(GROBID_URL, files=files, timeout=60)

        # Check GROBID response
    if response.status_code != 200:
        raise Exception(f"GROBID processing failed: {response.text}")

    try:
        root = etree.fromstring(response.content)
        
        # Define namespace
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        
        # Extract metadata using namespace
        title_elem = root.find(".//tei:title", namespaces=ns)
        title = title_elem.text if title_elem is not None else ""
        
        # Extract authors
        author_elems = root.findall(".//tei:author//tei:persName", namespaces=ns)
        authors_list = []
        for author in author_elems:
            surname = author.findtext(".//tei:surname", namespaces=ns)
            forename = author.findtext(".//tei:forename", namespaces=ns)
            if surname and forename:
                authors_list.append(f"{forename} {surname}")
            elif surname:
                authors_list.append(surname)
        authors = ", ".join(authors_list)
        
        # Extract journal
        journal_elem = root.find(".//tei:title[@level='j']", namespaces=ns)
        journal = journal_elem.text if journal_elem is not None else ""
        
        # Extract year (this might need adjustment based on actual XML structure)
        date_elem = root.find(".//tei:date", namespaces=ns)
        year = date_elem.text if date_elem is not None else ""
        
        # Extract abstract
        abstract_elem = root.find(".//tei:abstract", namespaces=ns)
        abstract = abstract_elem.text if abstract_elem is not None else ""
        
    except Exception as e:
        raise Exception(f"XML parsing failed for {pdf_path.name}: {e}")






    # # Parse XML safely
    # try:
    #     root = etree.fromstring(response.content)
    #     title = root.findtext(".//title") or ""
    #     authors = ", ".join([a.text for a in root.findall(".//author//persName") if a.text]) or ""
    #     journal = root.findtext(".//periodical//title") or ""
    #     year = root.findtext(".//date") or ""
    #     abstract = root.findtext(".//abstract") or ""
    # except Exception as e:
    #     raise Exception(f"XML parsing failed for {pdf_path.name}: {e}")
    
    insert_metadata({
        "filename": pdf_path.name,
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "abstract": abstract
    })
        
    return {
        "filename": pdf_path.name,
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "abstract": abstract
    }

# def process_pdfs():

#     # Check upload folder
#     if not UPLOAD_FOLDER.exists():
#         print("ERROR: Upload folder does not exist:", UPLOAD_FOLDER.resolve())
#         return

#     pdf_files = list(UPLOAD_FOLDER.glob("*.pdf"))

#     if not pdf_files:
#         print("No PDF files found in:", UPLOAD_FOLDER.resolve())
#         return

#     print("Found", len(pdf_files), "PDF(s)")

#     for pdf_file in pdf_files:

#         print("\nProcessing:", pdf_file.name)

#         try:
#             with open(pdf_file, "rb") as f:

#                 files = {
#                     "input": (pdf_file.name, f, "application/pdf")
#                 }

#                 response = requests.post(
#                     GROBID_URL,
#                     files=files,
#                     timeout=60
#                 )
#             print("it worked")

#         except Exception as e:
#             print("ERROR sending request to GROBID:", e)
#             continue

#         # Check GROBID response
#         if response.status_code != 200:
#             print("\n--- GROBID RESPONSE PREVIEW ---")
#             print("GROBID failed for", pdf_file.name)
#             print("Status code:", response.status_code)
#             print("Response preview:", response.text[:500])
#             print("--- END PREVIEW ---\n")
#             continue

#         # Parse XML safely
#         try:
#             parser = etree.XMLParser(recover=True)
#             root = etree.fromstring(response.content)

#         except Exception as e:
#             print("XML parsing failed for", pdf_file.name)
#             print("Error:", e)
#             print("Response preview:", response.text[:500])
#             continue

#         ns = {"tei": "http://www.tei-c.org/ns/1.0"}

#         # Extract metadata
#         try:
#             title = root.findtext(".//tei:title", namespaces=ns)
#             print("Title extracted")
            
#             abstract = root.findtext(".//tei:abstract", namespaces=ns)
#             print("abstract extracted")
#             year = root.findtext(".//tei:date", namespaces=ns)
#             print("year extracted")
#             journal = root.findtext(".//tei:title[@level='j']", namespaces=ns)
#             print("Journal extracted")
#             authors_list = root.findall(".//tei:author", namespaces=ns)
#             print("author nodes found" , len(authors_list))
#             authors = []

#             for a in authors_list:
#                 name = a.findtext(".//tei:surname", namespaces=ns)
#                 if name:
#                     authors.append(name)

#             authors = ", ".join(authors)

#         except Exception as e:
#             print("Metadata extraction failed:", e)
#             continue

#         # Basic validation
#         if not title:
#             print("WARNING: Title missing for", pdf_file.name)

#         metadata = {
#             "filename": pdf_file.name,
#             "title": title if title else "Unknown",
#             "authors": authors if authors else "Unknown",
#             "journal": journal if journal else "Unknown",
#             "year": year if year else "Unknown",
#             "abstract": abstract if abstract else "None"
#         }

#         # Insert into database
#         try:
#             insert_metadata(metadata)
#             print("Stored:", pdf_file.name)

#         except Exception as e:
#             print("Database insert failed for", pdf_file.name)
#             print("Error:", e)

















