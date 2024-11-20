from library_manager import Library

def main() -> None:
    """
    Основная функция приложения для управления библиотекой.
    Позволяет пользователю взаимодействовать с библиотекой через консольный интерфейс.
    """
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

        choice: str = input("Введите номер действия: ").strip()

        if choice == "1":
            try:
                title: str = input("Введите название книги: ").strip()
                author: str = input("Введите автора: ").strip()
                year: int = int(input("Введите год издания: ").strip())
                library.add_book(title, author, year)
                print("Книга добавлена!")
            except ValueError:
                print("Ошибка: Год издания должен быть числом.")
        elif choice == "2":
            try:
                book_id: int = int(input("Введите ID книги: ").strip())
                if library.remove_book(book_id):
                    print("Книга удалена!")
                else:
                    print("Книга с таким ID не найдена.")
            except ValueError:
                print("Ошибка: ID книги должен быть числом.")
        elif choice == "3":
            field: str = input("Искать по (title, author, year): ").strip()
            query: str = input("Введите запрос: ").strip()
            if field not in {"title", "author", "year"}:
                print("Ошибка: Поле должно быть 'title', 'author' или 'year'.")
                continue
            results = library.search_books(query, field)
            if results:
                for book in results:
                    print(book.to_dict())
            else:
                print("Ничего не найдено.")
        elif choice == "4":
            books = library.list_books()
            if books:
                for book in books:
                    print(book)
            else:
                print("Библиотека пуста.")
        elif choice == "5":
            try:
                book_id: int = int(input("Введите ID книги: ").strip())
                new_status: str = input("Введите новый статус (в наличии/выдана): ").strip()
                if new_status not in {"в наличии", "выдана"}:
                    print("Ошибка: Статус должен быть 'в наличии' или 'выдана'.")
                    continue
                if library.change_status(book_id, new_status):
                    print("Статус обновлён!")
                else:
                    print("Ошибка обновления статуса.")
            except ValueError:
                print("Ошибка: ID книги должен быть числом.")
        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
