from pathlib import Path
import PyPDF2


def join_pdf(folder, destination):
    """
    Merge all PDFs in a folder (including all subfolders) and store merged PDF in specified path
    :param destination: path (str) where the merged PDF will be stored
    :param folder: pathlib.Path object
    :return: merged PDF in the folder
    """
    merge_pdf = PyPDF2.PdfFileMerger()

    for pdf_path in folder.glob('**/*.pdf'):
        with open(pdf_path, 'rb') as read_object:
            read_pdf = PyPDF2.PdfFileReader(read_object)
            merge_pdf.append(read_pdf)

    with open(destination + '/joined_{}.pdf'.format(folder.stem), 'wb') as merge_object:
        merge_pdf.write(merge_object)


def join_pdf_in_subfolders(folder):
    """
    For each subfolder in the folder, find all PDF recursively in that subfolder, merge them in a PDF,
    and store the merged PDFs in the root folder
    :param folder: root folder (str) where merged PDFs will be stored
    :return: merged PDFs from the subfolders will be stored in the root folder
    """
    path_object = Path(folder)
    subfolders = [subfolder for subfolder in path_object.iterdir() if subfolder.is_dir()]
    for subfolder in subfolders:
        join_pdf(subfolder, folder)


def main():
    join_pdf_in_subfolders(r'C:\Projects\JHU\R-programming\notes\r-programming')


if __name__ == '__main__':
    main()