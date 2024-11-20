import unittest
import os
from library_manager import Library, Book

class TestLibrary(unittest.TestCase):
    """
    Набор тестов для проверки функциональности класса Library.
    """

    def setUp(self) -> None:
        """
        Подготовка тестового окружения.
        Создаем тестовый экземпляр библиотеки с временным файлом.
        """
        self.test_file = "test_library.json"
        self.library = Library(data_file=self.test_file)
        self.library.books = []  # Очищаем библиотеку перед каждым тестом
        self.library.save_books()

    def tearDown(self) -> None:
        """
        Очистка после тестов.
        Удаляем временный файл.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self) -> None:
        """
        Проверяет добавление книги в библиотеку.
        """
        self.library.add_book("Test Title", "Test Author", 2023)
        books = self.library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Test Title")
        self.assertEqual(books[0]["author"], "Test Author")
        self.assertEqual(books[0]["year"], 2023)
        self.assertEqual(books[0]["status"], "в наличии")

    def test_remove_book(self) -> None:
        """
        Проверяет удаление книги из библиотеки.
        """
        self.library.add_book("To Remove", "Author", 2022)
        book_id = self.library.books[0].book_id
        result = self.library.remove_book(book_id)
        self.assertTrue(result)
        self.assertEqual(len(self.library.list_books()), 0)

    def test_remove_nonexistent_book(self) -> None:
        """
        Проверяет удаление несуществующей книги.
        """
        result = self.library.remove_book(999)  # Несуществующий ID
        self.assertFalse(result)

    def test_search_books(self) -> None:
        """
        Проверяет поиск книг по различным полям.
        """
        self.library.add_book("Search Title", "Search Author", 2021)
        results_title = self.library.search_books("Search", "title")
        self.assertEqual(len(results_title), 1)
        self.assertEqual(results_title[0].title, "Search Title")

        results_author = self.library.search_books("Author", "author")
        self.assertEqual(len(results_author), 1)
        self.assertEqual(results_author[0].author, "Search Author")

        results_year = self.library.search_books("2021", "year")
        self.assertEqual(len(results_year), 1)
        self.assertEqual(results_year[0].year, 2021)

    def test_change_status(self) -> None:
        """
        Проверяет изменение статуса книги.
        """
        self.library.add_book("Status Test", "Author", 2020)
        book_id = self.library.books[0].book_id

        result = self.library.change_status(book_id, "выдана")
        self.assertTrue(result)
        self.assertEqual(self.library.books[0].status, "выдана")

        result_invalid = self.library.change_status(book_id, "недоступно")  # Некорректный статус
        self.assertFalse(result_invalid)

    def test_list_books(self) -> None:
        """
        Проверяет корректность вывода списка всех книг.
        """
        self.library.add_book("Book 1", "Author 1", 2001)
        self.library.add_book("Book 2", "Author 2", 2002)
        books = self.library.list_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Book 1")
        self.assertEqual(books[1]["title"], "Book 2")

if __name__ == "__main__":
    unittest.main()
