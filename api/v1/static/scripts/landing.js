function fetchBooksList() {
    const booksList = document.getElementById('books-list');
    fetch('http://localhost:5000/coolbooks/all_books')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then((data) => {
            booksList.innerHTML = '';
            if (data.length <= 5) {
                data.forEach((book) => {
                const bookItem = document.createElement('div');
                bookItem.classList.add('book-item');
                bookItem.innerHTML = `<img src="${book.cover}" alt="${book.title}" class="book-cover">`; // Use a default cover if none exists
                booksList.appendChild(bookItem);
            });
            }else {
                for (var i = 0; i < 5; i++) {
                    const bookItems = document.createElement('div');
                    bookItems.classList.add('book-item');
                    console.log(data[i])
                    bookItems.innerHTML = `<img src="${data[i].cover}" alt="${data[i].title}" class="book-cover"></img>`;
                    booksList.appendChild(bookItems);
                }
            }
        })
        .catch(err => {
            booksList.innerHTML = '';
            for (let i = 0; i < 5; i++) {
                const bookItem = document.createElement('div');
                bookItem.classList.add('book-item');
                bookItem.innerHTML = "<img src='../static/images/bookcover.png' alt='bookcover'></img>";
                booksList.appendChild(bookItem);
            }
        }); // Log errors
}

document.addEventListener('DOMContentLoaded', fetchBooksList); // Correct function name
setInterval(fetchBooksList, 5000); // Fetch books every 5 seconds
