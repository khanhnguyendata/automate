from pathlib import Path
from pprint import pprint
import PyPDF2


def join_pdf(folder):
    write_pdf = PyPDF2.PdfFileWriter()

    for pdf_path in folder.glob('**/*.pdf'):
        print(pdf_path)
        read_object = open(pdf_path, 'rb')
        read_pdf = PyPDF2.PdfFileReader(read_object)

        for page in range(read_pdf.numPages):
            page_object = read_pdf.getPage(page)
            write_pdf.addPage(page_object)
        read_object.close()

    with open('joined.pdf', 'wb') as write_object:
        write_pdf.write(write_object)


def main():
    # folder = Path(r'C:\Projects\JHU\R-programming\notes\r-programming\01_week-1-background-getting-started-and-nuts-bolts')
    # join_pdf(folder)
    write_pdf = PyPDF2.PdfFileWriter()

    for path in [r'C:\Projects\JHU\R-programming\notes\r-programming\01_week-1-background-getting-started-and-nuts-bolts\01_background-material\01_welcome-to-r-programming_JHDSS_CourseDependencies.pdf',
                 r'C:\Projects\JHU\R-programming\notes\r-programming\01_week-1-background-getting-started-and-nuts-bolts\01_background-material\04_syllabus_JHSPH-StudentReferencing_handbook.pdf']:
        read_object = open(path, 'rb')
        read_pdf = PyPDF2.PdfFileReader(read_object)
        for page in range(read_pdf.numPages):
            page_object = read_pdf.getPage(page)
            write_pdf.addPage(page_object)
        read_object.close()

    write_object = open('joined.pdf', 'wb')
    write_pdf.write(write_object)

    write_object.close()


if __name__ == '__main__':
    main()