# Library Project
## General Description
The project has an interface where it will be possible to manage the status of member books, and receive a status report on borrowing and returning books, updating book details, adding new books, deleting books, and general data about library users, for example, a report on books available for loan by category or number of books currently on loan, in addition to a general report on how many times each book has been borrowed.

## Project structure
```
library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db_connection.py  
│   │   ├── book_db.py  
│   │   └── member_db.py  
│   ├── routes/  
│   │   ├── book_routes.py  
│   │   ├── member_routes.py  
│   │   └── report_routes.py  
│   └── app.log 
│         
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
| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `title` | כותרת הספר, עמודה לא ריקה, מקסימום 50 תווים |
| `author` | שם המחבר, עמודה לא ריקה, מקסימום 50 תווים |
| `genre` | **ערכי `genre` מותרים:**  Fiction | Non-Fiction | Science | History | Other — מומש כעמודת ENUM במסד הנתונים, כל ערך אחר מחזיר שגיאה, עמודה לא ריקה |
| `is_available` | האם הספר זמין להשאלה — FALSE מסמן הושאל עמודה לא ריקה |
| `borrowed_by_member_id` | מזהה החבר שמחזיק את הספר — NULL אם זמין |

### Members table
| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `name` | שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email` | כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active` | האם החבר פעיל — FALSE לא יכול להשאיל עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה עמודה לא ריקה |

## System rules
| חוק | נושא | הכלל |
| ----: | ----: | ----: |
| 1 | יצירת ספר | המשתמש שולח title/author/genre — המערכת מוסיפה `is_available=True`, `borrowed_by=NULL` |
| 2 | genre | חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה יש לוודא הן בהוספה (POST) והן בעדכון (PATCH) |
| 3 | יצירת חבר | המשתמש שולח name/email — המערכת מוסיפה `is_active=True`, `total_borrows=0` |
| 4 | email | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם `is_active=False` — אי אפשר להשאיל ספר |
| 6 | ספר לא זמין | אי אפשר להשאיל ספר שכבר מושאל (`is_available=False`) |
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

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

- 1.**python -m venv venv --without-pip**
- 2.**.\venv\Scripts\Activate.ps1**
- 3.**pip install -r requierments.txt**
- 4.**cd app**
- 5.**python main.py**



