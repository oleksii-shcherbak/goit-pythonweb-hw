import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Book:
    def __init__(self, title: str, author: str, year: str) -> None:
        self.title = title
        self.author = author
        self.year = year


class LibraryInterface(ABC):
    @abstractmethod
    def add_book(self, book: "Book") -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        pass

    @abstractmethod
    def show_books(self) -> None:
        pass


class Library(LibraryInterface):
    def __init__(self) -> None:
        self.books: list[Book] = []

    def add_book(self, book: "Book") -> None:
        self.books.append(book)

    def remove_book(self, title: str) -> None:
        self.books = [b for b in self.books if b.title != title]

    def show_books(self) -> None:
        for book in self.books:
            logger.info(
                f"Title: {book.title}, Author: {book.author}, Year: {book.year}"
            )


class LibraryManager:
    def __init__(self, library: LibraryInterface) -> None:
        self.library: LibraryInterface = library

    def add_book(self, title: str, author: str, year: str) -> None:
        book: Book = Book(title, author, year)
        self.library.add_book(book)

    def remove_book(self, title: str) -> None:
        self.library.remove_book(title)

    def show_books(self) -> None:
        self.library.show_books()


def main() -> None:
    library: Library = Library()
    manager: LibraryManager = LibraryManager(library)

    while True:
        command: str = (
            input("Enter command (add, remove, show, exit): ").strip().lower()
        )

        match command:
            case "add":
                title: str = input("Enter book title: ").strip()
                author: str = input("Enter book author: ").strip()
                year: str = input("Enter book year: ").strip()
                manager.add_book(title, author, year)
            case "remove":
                title: str = input("Enter book title to remove: ").strip()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                break
            case _:
                print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
