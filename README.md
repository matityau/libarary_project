# Library Project
## General Description
The project has an interface where it will be possible to manage the status of member books, and receive a status report on borrowing and returning books, updating book details, adding new books, deleting books, and general data about library users, for example, a report on books available for loan by category or number of books currently on loan, in addition to a general report on how many times each book has been borrowed.

## Project structure
```
library-api/
│
├──app
|   |
|  main.py
|
├── database/
│ ├── db_connection.py
│ ├── book_db.py
│ └── member_db.py
├── routes/
│ ├── book_routes.py
│ ├── member_routes.py
│ └── report_routes.py
├── logs/
│ └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
```
## Database container
Here is the command to run the library database container.
```
docker run --name libarary_db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=libarary -p 3306:3306 -d mysql:8
```

## Tables structure
### Book table
Each book will have a unique ID, a title, an author's name, a genre that is one of the following: Fiction | Non-Fiction | Science | History | Other. 

The book will be listed as to whether it is available for loan or not, and if a friend has lent the book, the name of the borrower will be listed.

### Members table
Each member will have a unique ID, a name up to 50 characters long, no blank column allowed.
Unique email, no blank column allowed.
A column showing whether the member is active and can borrow a book.
And a counter that counts the number of questions given to that member.

## System rules
1. Create a book - the user sends a title, author name and gener, the system adds
is_available=True, borrowed_by=NULL.
2.genre - must be one of Fiction / Non-Fiction / Science / History / Other, any other value returns an error. Validation must be performed on addition and update.
3. create member - the user sends email/name - the system adds, True=active_is
total_borrows=0.
4. email - must be unique - if it already exists, an error is returned/
5. Inactive member - if False=active_is - a book cannot be borrowed.
6. Book unavailable - a book that has already been borrowed cannot be borrowed (False=available_is)
7. Maximum books - a member cannot have more than 3 books at a time.

8. Return a book - a book can only be returned if it is borrowed by the same member who is returning it.    

### Endpoints list
### BOOKS
- 1.Create a book ------ **post /books**
- 2.All books ---------- **GET / books**
- 3.book by id -------- **GET /books/{id}**
- 4.update book -------- **PATCH /books/{id}**
- 5.loan book to memeber **PATCH /{id}/borrow/{member_id}**
- 6.return books member **PATCH /books/{id}/return/{member_id}**
### MEMBERS
- 1.create member ----- **POST /members**
- 2.all member --------- **GET /members**
- 3.get member by id --- **GET /members/{id}**
- 4.update member ----- **PATCH /members/{id}**
- 5.deactive member ---** PATCH /members/{id}/deactivate **
- 6.active member ---- **PATCH /members/{id}/activate**

### REPORTS
- 1.General report ---- **GET /reports/summary**
- 2.Books by genre --- ** GET /reports/books-by-genre**
- 3.The most active member -- **GET /reports/top-member**
 
## System flow
http request -> fastapi -> endpoints -> query -> database

## Running instructions
python main.app



