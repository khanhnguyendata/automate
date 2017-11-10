import os, PyPDF2


def get_filenames():
    """
    Get PDF files not yet reordered in the current directory
    :return: list of PDF file names
    """
    filenames = []
    for filename in os.listdir('.'):
        if filename.endswith('.pdf') and not filename.endswith('reordered.pdf'):
            filenames.append(filename)

    return filenames


def write_pages(page_range, pdf_read, pdf_write):
    """
    Read pages within certain page range from the PDF read object and write those pages to the PDF write object
    :param page_range: iterable containing pages to be read and written
    :param pdf_read: PyPDF2.PdfFileReader object where pages are read from
    :param pdf_write: PyPDF2.PdfFileWriter object where pages are written to
    :return:
    """
    for page_num in page_range:
        page = pdf_read.getPage(page_num)
        pdf_write.addPage(page)


def reorder_index(filename, insert_page, appendix_start, appendix_end, index_start, index_end):
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
    with open(filename, 'rb') as file_read, open(filename[:-4] + '_reordered.pdf', 'wb') as file_write:
        pdf_read = PyPDF2.PdfFileReader(file_read)
        pdf_write = PyPDF2.PdfFileWriter()
        pdf_length = pdf_read.numPages

        # Check for invalid page numbers
        if insert_page < 1 or insert_page >= appendix_start:
            raise ValueError('Invalid insert page')
        if appendix_start > appendix_end:
            raise ValueError('Invalid appendix start page')
        if appendix_end >= index_start:
            raise ValueError('Invalid appendix end page')
        if index_start > index_end:
            raise ValueError('Invalid index start page')
        if index_end > pdf_length:
            raise ValueError('Invalid index end page')

        # Prepare page ranges to be ordered
        pre_insert = range(insert_page)
        post_insert = range(insert_page, appendix_start - 1)
        appendix = range(appendix_start - 1, appendix_end)
        post_appendix = range(appendix_end, index_start - 1)
        index = range(index_start - 1, index_end)
        post_index = range(index_end, pdf_length)

        # Copy pages from original PDF object to new PDF object with the new ordered page ranges
        for page_range in [pre_insert, index, appendix, post_insert, post_appendix, post_index]:
            write_pages(page_range, pdf_read, pdf_write)

        # Write ordered PDF object to PDF file
        pdf_write.write(file_write)


def main():
    while True:
        filenames = get_filenames()
        if filenames:
            for index, filename in enumerate(filenames):
                print('{}: {}'.format(index+1, filename))
            chosen_index = int(input('\nEnter the number of the file you want to reorder: '))
            insert_page = int(input('Enter the page you want your appendix and index to come after: '))
            appendix_start = int(input('Enter the start page of your appendix: '))
            appendix_end = int(input('Enter the end page of your appendix: '))
            index_start = int(input('Enter the start page of your index: '))
            index_end = int(input('Enter the end page of your index: '))
            try:
                filename = filenames[int(chosen_index-1)]
                reorder_index(filename, insert_page, appendix_start, appendix_end, index_start, index_end)
                print('\n{} reordered.'.format(filename))
            except Exception as error:
                print(error)
                print('Restarting program\n')
                continue
        else:
            print('No unordered PDF found in current directory')

        is_continue = input('\nDo you want to order another PDF (y/n)? ')
        if is_continue == 'n':
            break
        while is_continue != 'y':
            print('Invalid input')
            is_continue = input("Do you want to order another PDF (y/n)? ")


if __name__ == '__main__':
    main()