"""Simple document reader."""

from pathlib import Path

import PyPDF2


class DocumentReader:
    """Reads documents from files."""

    def read_file(self, file_path: str) -> str:
        """
        Read content from file.

        Args:
            file_path: Path to file

        Returns:
            str: File content
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() == '.pdf':
            return self._read_pdf(file_path)
        elif path.suffix.lower() == '.txt':
            return self._read_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

    def _read_pdf(self, file_path: str) -> str:
        """Read PDF file."""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
        return content.strip()

    def _read_text(self, file_path: str) -> str:
        """Read text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def split_text(self, text: str, chunk_size: int = 1000) -> list[str]:
        """Split text into chunks."""
        sentences = text.split('. ')
        chunks = []
        current = ""

        for sentence in sentences:
            if len(current + sentence) < chunk_size:
                current += sentence + ". "
            else:
                if current.strip():
                    chunks.append(current.strip())
                current = sentence + ". "

        if current.strip():
            chunks.append(current.strip())

        return [chunk for chunk in chunks if len(chunk) > 50]


# Global instance
document_reader = DocumentReader()
