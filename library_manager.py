import json
from typing import List, Optional

class Book:
    """
    Класс для представления книги.

    Атрибуты:
        book_id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализация объекта книги.

        Args:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str, optional): Статус книги (по умолчанию "в наличии").
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.

        Returns:
            dict: Словарь с данными книги.
        """
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    """
    Класс для управления библиотекой.

    Атрибуты:
        data_file (str): Путь к файлу для хранения данных библиотеки.
        books (List[Book]): Список объектов книг в библиотеке.
    """
    def __init__(self, data_file: str = "library.json"):
        """
        Инициализация объекта библиотеки.

        Args:
            data_file (str, optional): Путь к файлу данных библиотеки (по умолчанию "library.json").
        """
        self.data_file = data_file
        self.books: List[Book] = self.load_books()

    def load_books(self) -> List[Book]:
        """
        Загружает книги из файла.

        Returns:
            List[Book]: Список объектов книг, загруженных из файла.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        except FileNotFoundError:
            return []

    def save_books(self) -> None:
        """
        Сохраняет текущий список книг в файл.
        """
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        new_id = max((book.book_id for book in self.books), default=0) + 1
        new_book = Book(book_id=new_id, title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int) -> bool:
        """
        Удаляет книгу из библиотеки по её ID.

        Args:
            book_id (int): Уникальный идентификатор книги.

        Returns:
            bool: True, если книга успешно удалена, иначе False.
        """
        book = self.find_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_id(self, book_id: int) -> Optional[Book]:
        """
        Ищет книгу по её ID.

        Args:
            book_id (int): Уникальный идентификатор книги.

        Returns:
            Optional[Book]: Объект книги, если найден, иначе None.
        """
        return next((book for book in self.books if book.book_id == book_id), None)

    def search_books(self, query: str, field: str) -> List[Book]:
        """
        Ищет книги по заданному полю и запросу.

        :param query: Запрос для поиска.
        :param field: Поле для поиска (title, author, year).
        :return: Список найденных книг.
        """
        query_lower = query.lower()
        return [
            book for book in self.books
            if query_lower in str(getattr(book, field, "")).lower()
        ]

    def change_status(self, book_id: int, new_status: str) -> bool:
        """
        Изменяет статус книги.

        Args:
            book_id (int): Уникальный идентификатор книги.
            new_status (str): Новый статус книги ("в наличии" или "выдана").

        Returns:
            bool: True, если статус успешно изменён, иначе False.
        """
        book = self.find_by_id(book_id)
        if book and new_status in {"в наличии", "выдана"}:
            book.status = new_status
            self.save_books()
            return True
        return False

    def list_books(self) -> List[dict]:
        """
        Возвращает список всех книг в библиотеке.

        Returns:
            List[dict]: Список словарей с данными всех книг.
        """
        return [book.to_dict() for book in self.books]