from PyPDF2 import PdfReader, PdfWriter
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError


class Pdf:
    def merge_pdfs(self, pdfs: list, output: str):
        try:
            pdf_writer = PdfWriter()
            for pdf in pdfs:
                try:
                    reader = PdfReader(pdf)
                    for page in reader.pages:
                        pdf_writer.add_page(page)
                except FileNotFoundError:
                    print(f"File not found: '{pdf}'")
                except PdfReadError:
                    print(f"PDF is locked or corrupted: '{pdf}'")
                except Exception as e:
                    print(f"Error reading PDF '{pdf}': {e}")

            with open(output, "wb") as out:
                pdf_writer.write(out)
            print(f"Merged PDF saved as '{output}'")
        except Exception as e:
            print(f"Error merging PDFs: {e}")

    def split_pdf(self, pdf, select):
        try:
            reader = PdfReader(pdf)
            num_pages = len(reader.pages)

            if select == "odd":
                pages_to_split = range(
                    0, num_pages, 2
                )  # 0-based indexing for odd pages
            elif select == "even":
                pages_to_split = range(
                    1, num_pages, 2
                )  # 0-based indexing for even pages
            elif isinstance(select, list):
                pages_to_split = select  # Custom list of pages
            elif isinstance(select, int):
                pages_to_split = range(select)
            else:
                return f"need to select the pages use [page x , page y , page z,...] or 10 (for first 10 pages)\nEven and odd"

            writer = PdfWriter()
            for page_num in pages_to_split:
                if 0 <= page_num < num_pages:  # Ensure valid page numbers
                    writer.add_page(reader.pages[page_num])
                else:
                    continue

            if writer.pages:
                output_filename = f'{pdf.rsplit(".", 1)[0]}_selected_pages_{select}.pdf'
                with open(output_filename, "wb") as out:
                    writer.write(out)
                print(f"Selected pages saved as '{output_filename}'")
            else:
                print("No valid pages selected to save.")

        except FileNotFoundError:
            print(f"File not found: '{pdf}'")
        except PdfReadError:
            print(f"PDF is locked or corrupted: '{pdf}'")
        except Exception as e:
            print(f"Error splitting PDF: {e}")

    def extract_text_from_pdf(self, pdf, page_number=None):
        try:
            reader = PdfReader(pdf)
            if page_number is not None:
                if 0 <= page_number < len(reader.pages):
                    return reader.pages[page_number - 1].extract_text()
                else:
                    print(f"Invalid page number: {page_number}")
                    return ""
            else:
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except FileNotFoundError:
            return f"File not found: '{pdf}'"
        except PdfReadError:
            return f"PDF is locked or corrupted: '{pdf}'"
        except Exception as e:
            return f"Error extracting text from PDF: {e}"
