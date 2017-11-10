import PyPDF2
from pathlib import Path


def get_filenames():
    """
    Get PDF files not yet reordered in the current directory
    :return: list of PDF file names
    """
    filenames = []
    for filename in Path(".").glob("*.pdf"):
        if "reordered" not in filename.stem:
            filenames.append(filename)

    return filenames


def write_pages(page_range, pdf_read, pdf_write):
    """
    Read pages within certain page range from the PDF read object and write those pages to the PDF write object
    :param page_range: iterable containing pages to be read and written
    :param pdf_read: PyPDF2.PdfFileReader object where pages are read from
    :param pdf_write: PyPDF2.PdfFileWriter object where pages are written to
    :return: None. pdf_write is modified in place.
    """
    for page_num in page_range:
        page = pdf_read.getPage(page_num)
        pdf_write.addPage(page)


def reorder(filename, insert_page, appendix_start, appendix_end, index_start, index_end):
    """
    Reorder the appendix and index of a PDF book to another location and store the new PDF under a new name
    :param filename: name of the PDF file to be reordered
    :param insert_page: page in the original PDF after which the appendix and index are to be inserted
    :param appendix_start: appendix start page in the original PDF
    :param appendix_end: appendix end page in the original PDF
    :param index_start: index start page in the original PDF
    :param index_end: index end page in the original PDF
    :return: a reordered PDF (ending with '_reordered.pdf') in the same directory as the original PDF
    """
    with filename.open('rb') as file_read, open(filename.stem + '_reordered.pdf', 'wb') as file_write:
        pdf_read = PyPDF2.PdfFileReader(file_read)
        pdf_write = PyPDF2.PdfFileWriter()
        pdf_length = pdf_read.numPages

        # Check for invalid page numbers
        if insert_page < 1 or insert_page >= appendix_start:
            raise ValueError('Invalid insert page')
        if appendix_start != index_start and appendix_start > appendix_end:
            raise ValueError('Invalid appendix start page')
        if appendix_start != index_start and appendix_end >= index_start:
            raise ValueError('Invalid appendix end page')
        if index_start > index_end:
            raise ValueError('Invalid index start page')
        if index_end > pdf_length:
            raise ValueError('Invalid index end page')

        # Prepare page ranges to be ordered
        pre_insert = range(insert_page)
        post_insert = range(insert_page, appendix_start-1)
        appendix = range(appendix_start-1, appendix_end)
        post_appendix = range(appendix_end, index_start-1)
        index = range(index_start-1, index_end)
        post_index = range(index_end, pdf_length)

        # Copy pages from original PDF object to new PDF object with the new ordered page ranges
        for page_range in [pre_insert, index, appendix, post_insert, post_appendix, post_index]:
            write_pages(page_range, pdf_read, pdf_write)

        # Write ordered PDF object to PDF file
        pdf_write.write(file_write)


def yes_or_no(prompt):
    """
    Prompt user to answer yes or no to a prompt, and keep asking if user did not input a correct yes/no input
    :param prompt: str prompting user to input their response
    :return: yes or no response once user has correctly input their response
    """
    response = input(prompt)
    while response not in ['y', 'n']:
        print('Invalid input')
        response = input(prompt)

    return response


def appendix_and_index_pages():
    """
    Prompt user to input appendix pages (if one exists) and index pages
    :return: start and end pages of the appendix and index
    """
    def index_pages():
        """
        Prompt user to input index pages
        :return: start and end pages of index
        """
        index_start = int(input('Enter the start page of your index: '))
        index_end = int(input('Enter the end page of your index: '))
        return index_start, index_end

    is_appendix = yes_or_no('Does your book have an appendix (y/n)? ')

    if is_appendix == 'y':
        appendix_start = int(input('Enter the start page of your appendix: '))
        appendix_end = int(input('Enter the end page of your appendix: '))
        index_start, index_end = index_pages()
    else:
        # When there is no appendix, set appendix start and end pages such as the page ranges of the
        # appendix and the post-appendix (pre-index) will be blank, and the page range of the post-insert
        # will be from the insert point to the start of the index. See def reorder for more details.
        index_start, index_end = index_pages()
        appendix_start = index_start
        appendix_end = index_start - 1

    return appendix_start, appendix_end, index_start, index_end


def main():
    while True:
        filenames = get_filenames()
        if filenames:
            print('------')
            print('Unordered PDF files in the current directory: ')
            for index, filename in enumerate(filenames):
                print('{}: {}'.format(index+1, filename))
            chosen_index = int(input('\nEnter the number of the file you want to reorder: '))
            insert_page = int(input('Enter the page you want your appendix and index to come after: '))
            appendix_start, appendix_end, index_start, index_end = appendix_and_index_pages()

            try:
                filename = filenames[int(chosen_index-1)]
                reorder(filename, insert_page, appendix_start, appendix_end, index_start, index_end)
                print('\n{} reordered.'.format(filename))
            except Exception as error:
                print(error)
                print('Restarting program\n')
                continue
        else:
            print('No unordered PDF found in current directory')

        # Ask user to reorder additional PDFs
        is_continue = yes_or_no('\nDo you want to reorder another PDF (y/n)? ')
        if is_continue == 'n':
            break


if __name__ == '__main__':
    main()