import io
import fitz
from docx import Document
import pandas as pd
from bs4 import BeautifulSoup
from typing import Union
import os


class FileParser:

    """

    A file parsing class for extracting text content from various document formats.
    Supported file types include TXT, MD, JSON, CSV, PY, JS, PDF, DOCX, XLSX, HTML, and XML.

    
    Usage
    -----
    You must call the get_content_from_file method from the class instance.

    """

    def __init__(self) -> None:

        """

        Constructor of the FileParser class.

        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.

        """

        self.parsers = {
            ".txt": ("Text", self._extract_text_from_txt),
            ".md": ("Markdown", self._extract_text_from_txt),
            ".json": ("JSON", self._extract_text_from_txt),
            ".csv": ("CSV", self._extract_text_from_txt),
            ".py": ("Python Code", self._extract_text_from_txt),
            ".js": ("JavaScript Code", self._extract_text_from_txt),
            ".pdf": ("PDF", self._extract_text_from_pdf),
            ".docx": ("Word Document", self._extract_text_from_docx),
            ".xlsx": ("Excel Spreadsheet", self._extract_text_from_xlsx),
            ".html": ("HTML", self._extract_text_from_html),
            ".xml": ("XML", self._extract_text_from_html)
        }


    def _extract_text_from_txt(self, stream: io.BytesIO) -> str:

        """

        Extracts text from a plain text, markdown, JSON, or CSV file stream.

        
        Parameters
        ----------
        stream : io.BytesIO
            An in-memory binary stream of the file content.

            
        Returns
        -------
        content : str
            Extracted text content.

        """

        return stream.read().decode("utf-8")
    

    def _extract_text_from_pdf(self, stream: io.BytesIO) -> str:

        """

        Extracts text from a PDF document stream.

        
        Parameters
        ----------
        stream : io.BytesIO
            An in-memory binary stream of the PDF content.

            
        Returns
        -------
        content : str
            Extracted text content.

        """

        text = ""
        with fitz.open(stream=stream, filetype="pdf") as doc:
            for page_num, page in enumerate(doc, start=1):
                text += f"--- Page {page_num} ---\n"
                text += page.get_text() + "\n\n"


        return text


    def _extract_text_from_docx(self, stream: io.BytesIO) -> str:

        """

        Extracts text from a DOCX document stream.

        
        Parameters
        ----------
        stream : io.BytesIO
            An in-memory binary stream of the DOCX content.

            
        Returns
        -------
        content : str
            Extracted text content.
        """

        return "\n".join([p.text for p in Document(stream).paragraphs])
    

    def _extract_text_from_xlsx(self, stream: io.BytesIO) -> str:

        """

        Extracts data from an XLSX stream and formats it as Markdown tables.

        
        Parameters
        ----------
        stream : io.BytesIO
            An in-memory binary stream of the XLSX content.

            
        Returns
        -------
        content : str
            Extracted text content formatted as markdown.

        """

        xls = pd.ExcelFile(stream)
        full_text = ""
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name).fillna("")
            if not df.empty:
                full_text += f"--- Sheet: {sheet_name} ---\n"
                full_text += df.to_markdown(index=False)
                full_text += "\n\n"


        return full_text


    def _extract_text_from_html(self, stream: io.BytesIO) -> str:

        """

        Extracts clean text from an HTML stream.

        
        Parameters
        ----------
        stream : io.BytesIO
            An in-memory binary stream of the HTML content.

            
        Returns
        -------
        content : str
            Extracted text content.

        """

        soup = BeautifulSoup(stream.read().decode("utf-8"), "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()


        return soup.get_text(separator='\n', strip=True)


    def get_content_from_file(self, file_source: Union[str, bytes], filename: str) -> tuple[str, str]:

        """

        Dispatcher method to select the correct parser based on file extension.
        Accepts either a file path (str) or file content (bytes).
        Returns a tuple of (content, file_type).

        
        Parameters
        ----------
        file_source : str or bytes
            Path to the file or the file content as bytes.

        filename : str
            The original name of the file, used to determine the extension.

            
        Returns
        -------
        result : tuple
            A tuple containing the extracted content and the file type.

        """

        _, extension = os.path.splitext(filename.lower())

        if extension not in self.parsers:
            raise ValueError(f"Unsupported file format: {extension}. Supported formats are: {', '.join(self.parsers.keys())}.")


        file_type, parser_func = self.parsers[extension]

        if isinstance(file_source, str):
            if not os.path.isfile(file_source):
                raise ValueError(f"file_source must be a valid file path. Received: {file_source} with type: {type(file_source)}")
            with open(file_source, "rb") as f:
                stream = io.BytesIO(f.read())
        elif isinstance(file_source, bytes):
            stream = io.BytesIO(file_source)
        else:
            raise TypeError(f"Unsupported file_source type: {type(file_source)}. Must be str or bytes.")


        return parser_func(stream), file_type