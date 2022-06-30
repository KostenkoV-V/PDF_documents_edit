import os.path

import fitz
import img2pdf
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


# извлечение текста из PDF документа
def text_extract(path_doc):
    if not os.path.isfile(path_doc):
        print('[+] Файл не найден')
        return
    if not path_doc.endswith('.pdf'):
        print('[+] Неверное расширение файла')
        return

    doc = fitz.open(path_doc)
    print(f'\n[+] Количество страниц документа: {doc.page_count}')

    doc_name = os.path.split(path_doc)[-1].removesuffix('.pdf')

    text_dict = []
    for current_page in range(len(doc)):
        print(f'\r[+] Считываю страницу: {current_page + 1}', end='')
        if doc.load_page(100).get_text("text") != "":
            text_dict.append(doc.load_page(current_page).get_text("text"))
    if len(text_dict) > 0:
        if not os.path.exists(os.path.join(os.getcwd(), doc_name)):
            os.mkdir(os.path.join(os.getcwd(), doc_name))

        for text in text_dict:
            with open(os.path.join(os.getcwd(), doc_name, f"{doc_name}.txt"), 'a',
                      encoding='utf-8') as tex:
                tex.write(f'{text}\n')
    else:
        print('\n[+] Документ не имеет текстового слоя')
        main()
        return
    print(f'\n[+] Сохранение текста pdf-документа "{doc_name}" завершено.')
    main()
    return


# извлечение изображений из PDF документа
def image_extract(path_doc):
    if not os.path.isfile(path_doc):
        print('[+] Файл не найден')
        main()
        return
    if not path_doc.endswith('.pdf'):
        print('[+] Неверное расширение файла')
        main()
        return

    doc = fitz.open(path_doc)
    print(f'\n[+] Количество страниц документа: {doc.page_count}')

    doc_name = os.path.split(path_doc)[-1].removesuffix('.pdf')

    if not os.path.exists(os.path.join(os.getcwd(), doc_name)):
        os.mkdir(os.path.join(os.getcwd(), doc_name))
    if not os.path.exists(os.path.join(os.getcwd(), doc_name, 'images')):
        os.mkdir(os.path.join(os.getcwd(), doc_name, 'images'))

    page_count = 0
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            page_count += 1
            pix1.save(os.path.join(os.getcwd(), doc_name, 'images', f'image_0{page_count}.png'))
            print(f'\r[+] Изображение {page_count} сохранено', end='')
    print(f'\n[+] Сохранение изображений pdf-документа "{doc_name}" завершено.')
    main()
    return


# разбивка PDF-файлов на страницы
def pages_split(path_doc):
    if not os.path.isfile(path_doc):
        print('[+] Файл не найден')
        main()
        return
    if not path_doc.endswith('.pdf'):
        print('[+] Неверное расширение файла')
        main()
        return

    pdf = PdfFileReader(path_doc)
    print(f'\n[+] Количество страниц документа: {pdf.getNumPages()}\n')

    doc_name = os.path.split(path_doc)[-1].removesuffix('.pdf')

    if not os.path.exists(os.path.join(os.getcwd(), doc_name)):
        os.mkdir(os.path.join(os.getcwd(), doc_name))
    if not os.path.exists(os.path.join(os.getcwd(), doc_name, 'pages')):
        os.mkdir(os.path.join(os.getcwd(), doc_name, 'pages'))

    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        current_page = pdf.getPage(page)
        pdf_writer.addPage(current_page)
        with open(os.path.join(os.getcwd(), doc_name, 'pages', f'{doc_name}_{page + 1}.pdf'), "wb") as out:
            pdf_writer.write(out)
        print(f'\r[+] Страница {page + 1} сохранена', end='')
    print(f'\n[+] Сохранение страниц pdf-документа "{doc_name}" завершено.')
    main()
    return


# объединение документов PDF в один
def pages_merge(path_doc, name_file):
    if not os.path.isdir(path_doc):
        print('[+] Папка не найдена')
        main()
        return
    if len(os.listdir(path_doc)) <= 1:
        print('[+] В папке нет файлов для объединения')
        main()
        return

    merger = PdfFileMerger()

    count = 1
    for file in os.listdir(path_doc):
        if os.path.isfile(os.path.join(path_doc, file)):
            if file.endswith('.pdf'):
                print(f'\r[+] Объединяю файлы: {count} подождите...', end='')
                with open(os.path.join(path_doc, file), 'rb') as pdf_file:
                    source_file = PdfFileReader(pdf_file)
                    merger.append(source_file)
                count += 1
    merger.write(f'{name_file}.pdf')
    print(f'\n[+] Объединение страниц в pdf-документ "{name_file}.pdf" завершено.')
    main()
    return


# объединение картинок в pdf-документ
def merge_images(path_doc, title):
    if not os.path.isdir(path_doc):
        print('\n[+] Указанной папки не существует. Проверьте введенные данные')
        main()
        return

    if len(os.listdir(path_doc)) > 0:
        image_list = []
        count = 1
        for image in os.listdir(path_doc):
            if os.path.isfile(os.path.join(path_doc, image)):
                if image.split(".")[-1] in ['jpg', 'jpeg', 'bmp', 'png', 'tiff', 'gif']:
                    image_list.append(os.path.join(path_doc, image))
                    print(f'\r[+] Дабавлено {count}-е изображение', end='')
                    count += 1

        if len(image_list) > 0:
            print('\n[+] Обработка добавленных изображений...')
            with open(f'{title}.pdf', 'wb') as file:
                file.write(img2pdf.convert(image_list))
            print(f'\n[+] Объединение изображений в pdf-документ "{title}.pdf" завершено.')
            main()
            return
        else:
            print('\n[+] В папке нет файлов изображений. Проверьте правильность пути к изображениям')
            main()
            return


# выбор пользователем нужных действий
def main():
    user_input = input('\n[+] Выберите действие:\n   [1] Сохранить текст из PDF\n   [2] Сохранить картинки из PDF\n'
                       '   [3] Разделить документ PDF на страницы\n   [4] Объединить PDF-документ из страниц\n   '
                       '[5] Объединить картинки в PDF\n   [6] Выход\n   >>> ')

    if user_input == "1":
        text_extract(input('\n[+] Введите путь к файлу pdf >>> '))
    elif user_input == "2":
        image_extract(input('\n[+] Введите путь к файлу pdf >>> '))
    elif user_input == "3":
        pages_split(input('\n[+] Введите путь к файлу pdf >>> '))
    elif user_input == "4":
        pages_merge(input('\n[+] Введите путь к папке с файлами >>> '),
                    input('[+] Введите имя создаваемого pdf >>> '))
    elif user_input == "5":
        merge_images(input('\n[+] Введите путь к папке с картинками >>> '),
                     input('[+] Введите имя создаваемого pdf >>> '))
    elif user_input == "6":
        exit(0)
    else:
        print('\n[+] Неопознанный выбор. Попробуйте снова')
        main()
        return


if __name__ == "__main__":
    main()


    