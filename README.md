### Completed
**Base Model** in ```models/base.py```:
- *to_json*
- *__eq__*
- *save*
- *save_to_file*
- *load_from_file*
- *search*
- *get*

**test_base** in ```test/test_base.py```:
- *test for init*
- *test for eq*
- *test for save*
- *test for save_to_file*
- *test for load_from_file*
- *test for search*
- *test for get*

**User** in ```models/user.py
- *email setter and getter*
- *first name and last name setter and getter*
- *bio setter and getter*
- *is author*

**test_user** in ```test/test_user.py```
- *test for email*
- *test for first name and last name*
- *test for bio*

**Books** in ```models/books.py```
- *title setter and getter*
- *author setter and getter*
- *content setter and getter*
- *description setter and getter*
- *isbn getter and setter*
- *edition getter and setter*
- *year of publish getter and setter*
- *delete a book*

**test_book** in ```test/test_book.py```

**endpoints**
- */all_books* in ```api/v1/views/index.py```
- */all_books/<isbn>: GET* in ```api/v1/views/books.py```
- */post_book: POST* in ```api/v1/views/books.py```
- */all_books/<isbn>: DELETE* in ```api/v1/views/books.py```
- */all_books/<isbn>: PATCH* in ```api/v1/views/books.py```
