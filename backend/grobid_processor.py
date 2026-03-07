from pathlib import Path
from lxml import etree
import requests
import shutil
from typing import List, Dict, Any
from db import insert_metadata_in_db

GROBID_URL = "http://localhost:8070/api/processHeaderDocument"
UPLOAD_FOLDER = Path(__file__).parent / "data" / "uploaded_pdf"
PROCESSED_FOLDER= Path(__file__).parent / "data" / "processed_pdf"

def extract_metadata_from_xml(xml_content: str, filename: str) -> Dict[str, Any]:
    try:
        root = etree.fromstring(xml_content.encode())

        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        print(f"Extracting metadata from {filename}")
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
        print("extracting metadata successfull.")
        
        metadata= {
                "filename": filename,
                "title": title,
                "authors": authors,
                "journal": journal,
                "year": year,
                "abstract": abstract            }
        return metadata
    except etree.XMLSyntaxError as e:
        print(f"XML parsing failed for {filename}: {e}")
        return None
    except Exception as e:
        print(f"Error extracting metadata from {filename}: {e}")
        return None
    
def process_single_pdf(pdf_path: Path) -> Dict[str, Any] | None:
    try:
        print(f"Processing {pdf_path.name}")
        with open(pdf_path, "rb") as f:
            files = {"input": (pdf_path.name, f, "application/pdf")}
            response = requests.post(GROBID_URL, files=files, timeout=200)
        if response.status_code != 200:
            print(f"GROBID failed for {pdf_path.name} (Status: {response.status_code})")
            print(f"Response: {response.text[:200]}")
            return None
        print(f"GROBID connected successfully for {pdf_path.name}")
        # Extract metadata
        metadata = extract_metadata_from_xml(response.text, pdf_path.name)
        if metadata:
            # Move file to processed folder
            destination = PROCESSED_FOLDER / pdf_path.name
            shutil.move(str(pdf_path), destination)
            print(f"Moved {pdf_path.name} to processed folder")
            
        return metadata
    except requests.exceptions.ConnectionError:
        print(f"GROBID connection failed - is GROBID running at {GROBID_URL}?")
        return None
    except Exception as e:
        print(f"Unexpected error processing {pdf_path.name}: {e}")
        return None
    
def process_pdfs() -> List[Dict[str, Any]]:
    pdf_files = list(UPLOAD_FOLDER.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF(s) to process")
    results = []
    for pdf_path in pdf_files:
        metadata = process_single_pdf(pdf_path)
        if metadata:
            results.append(metadata)
            inserted_in_db= insert_metadata_in_db(pdf_path.name, metadata)
            if inserted_in_db:
                print("successfully inserted metadata in sqlite")
            else:
                print("metadata insertion in sqlite not successfull.")
    print(f"\nProcessing complete. Successfully processed {len(results)} out of {len(pdf_files)} files")
    return results         

# if __name__ == "__main__":
#     # Test the function

#     results = process_pdfs()
#     for metadata in results:
#         print(f"\n--- {metadata['filename']} ---")
#         print(f"Title: {metadata['title']}")
#         print(f"Authors: {metadata['authors']}")
#         print(f"Journal: {metadata['journal']}")
#         print(f"Year: {metadata['year']}")