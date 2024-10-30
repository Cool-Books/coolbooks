const searchInput = document.getElementById('searchInput');
const searchIcon = document.getElementById('searchIcon');
let isExpanded = false;

searchIcon.addEventListener('click', () => {
    if (isExpanded) {
        // Collapse the search input
        searchInput.style.padding = '0';
        searchInput.style.width = '0';
    } else {
        // Expand the search input with responsive width
        searchInput.style.padding = '0 10px';

        // Check screen width to adjust width for smaller screens
        if (window.innerWidth <= 768) {
            searchInput.style.width = '100px'; // Smaller width for mobile screens
            searchInput.style.transition = 'width 0.5s ease';
        } else {
            searchInput.style.width = '150px'; // Default width for larger screens
            searchInput.style.transition = 'width 0.5s ease';
        }
    }
    isExpanded = !isExpanded;
});

const grav = document.getElementById('grav')
const fallBack = document.getElementById('fallbackIcon')

document.addEventListener('DOMContentLoaded', gravatarLoader)

function gravatarLoader() {
    fetch('http://localhost:5000/coolbooks/users/03a978e3-9190-4243-9679-c3b4367f907d')
        .then((response) => {
            console.log(response)
            return response.json()
                .then((data) => {
                    if (response.status == 200) {
                        grav.src = data.gravatar;
                        grav.style.display = 'block';
                        fallBack.style.display = 'none';
                    } else {
                        throw new Error()
                    }
                })
        }).catch(err => {
            fallBack.style.display = 'block';
            grav.style.display = 'none';
        });
};

function fetchBooksList() {
    fetch('http://localhost:5000/coolbooks/all_books')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            trendingRow.innerHTML = '';
            data.slice(0, 20).forEach(book => {
                const bookCover = document.createElement('img')
                bookCover.classList.add('book-cover')
                bookCover.src = book.cover;
                bookCover.alt = book.title;
                trendingRow.appendChild(bookCover);
            })
        }).catch(err => {
            trendingRow.innerHTML = '';
            for (let i=0; i < 10; i++) {
                const bookCover = document.createElement('img')
                bookCover.classList.add('book-cover')
                bookCover.src = '../static/images/bookcover.png';
                bookCover.alt = 'bookcover';
                trendingRow.appendChild(bookCover);
            }
        })
}

document.getElementById('left-icon').addEventListener('click', () => {
    document.getElementById('trendingRow').scrollBy({ left: -300, behavior: 'smooth' });
});

document.getElementById('right-icon').addEventListener('click', () => {
    document.getElementById('trendingRow').scrollBy({ left: 300, behavior: 'smooth' });
});

document.addEventListener('DOMContentLoaded', fetchBooksList); // Correct function name
setInterval(fetchBooksList, 5000); // Fetch books every 5 seconds
setInterval(gravatarLoader, 10000);