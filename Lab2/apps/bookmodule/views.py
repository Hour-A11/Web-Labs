from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import (
    Q,
    Count,
    Sum,
    Avg,
    Max,
    Min,
    F,
    Value,
    FloatField,
    ExpressionWrapper,
    OuterRef,
    Subquery,
)

from .models import Book, Address, Student, Publisher, Author


def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')


def list_books(request):
    return render(request, 'bookmodule/list_books.html')


def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')


# Lab5
def html5_links(request):
    return render(request, 'bookmodule/html5_links.html')


def html5_text_formatting(request):
    return render(request, 'bookmodule/html5_text_formatting.html')


def html5_listing(request):
    return render(request, 'bookmodule/html5_listing.html')


def html5_tables(request):
    return render(request, 'bookmodule/html5_tables.html')


# Lab6
def __getBooksList():
    book1 = {
        'id': 12344321,
        'title': 'Continuous Delivery',
        'author': 'J.Humble and D. Farley'
    }

    book2 = {
        'id': 56788765,
        'title': 'Reversing: Secrets of Reverse Engineering',
        'author': 'E. Eilam'
    }

    book3 = {
        'id': 43211234,
        'title': 'The Hundred-Page Machine Learning Book',
        'author': 'Andriy Burkov'
    }

    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(
            request,
            'bookmodule/bookList.html',
            {'books': newBooks}
        )

    return render(request, 'bookmodule/search.html')


# Lab7
def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')

    return render(
        request,
        'bookmodule/bookList.html',
        {'books': mybooks}
    )


def complex_query(request):
    mybooks = (
        Book.objects
        .filter(author__isnull=False)
        .filter(title__icontains='and')
        .filter(edition__gte=2)
        .exclude(price__lte=100)[:10]
    )

    if len(mybooks) >= 1:
        return render(
            request,
            'bookmodule/bookList.html',
            {'books': mybooks}
        )
    else:
        return render(request, 'bookmodule/index.html')


# Lab8 - Task1
def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))

    return render(
        request,
        'bookmodule/lab8_books.html',
        {
            'books': books,
            'page_title': 'Lab8 - Task1',
            'description': 'Books with price less than or equal to 80.'
        }
    )


# Lab8 - Task2
def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3)
        & (
            Q(title__icontains='co')
            | Q(author__icontains='co')
        )
    )

    return render(
        request,
        'bookmodule/lab8_books.html',
        {
            'books': books,
            'page_title': 'Lab8 - Task2',
            'description': (
                'Books with edition higher than 3 and '
                'either title or author containing "co".'
            )
        }
    )


# Lab8 - Task3
def lab8_task3(request):
    books = Book.objects.filter(
        ~(
            Q(edition__gt=3)
            & (
                Q(title__icontains='co')
                | Q(author__icontains='co')
            )
        )
    )

    return render(
        request,
        'bookmodule/lab8_books.html',
        {
            'books': books,
            'page_title': 'Lab8 - Task3',
            'description': 'Books that do not match the condition in Task2.'
        }
    )


# Lab8 - Task4
def lab8_task4(request):
    books = Book.objects.order_by('title')

    return render(
        request,
        'bookmodule/lab8_books.html',
        {
            'books': books,
            'page_title': 'Lab8 - Task4',
            'description': 'Books ordered by title.'
        }
    )


# Lab8 - Task5
def lab8_task5(request):
    statistics = Book.objects.aggregate(
        number_of_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        maximum_price=Max('price'),
        minimum_price=Min('price')
    )

    return render(
        request,
        'bookmodule/lab8_statistics.html',
        {'statistics': statistics}
    )


# Lab8 - Task7
def lab8_task7(request):
    cities = (
        Address.objects
        .values('city')
        .annotate(student_count=Count('student'))
        .order_by('city')
    )

    return render(
        request,
        'bookmodule/lab8_students.html',
        {'cities': cities}
    )


# Lab9 - Task1
def lab9_task1(request):
    total_quantity = (
        Book.objects.aggregate(total=Sum('quantity'))['total'] or 0
    )

    if total_quantity > 0:
        books = Book.objects.annotate(
            availability=ExpressionWrapper(
                F('quantity') * 100.0 / total_quantity,
                output_field=FloatField()
            )
        )
    else:
        books = Book.objects.annotate(
            availability=Value(0.0, output_field=FloatField())
        )

    return render(
        request,
        'bookmodule/lab9_books.html',
        {
            'books': books,
            'total_quantity': total_quantity
        }
    )


# Lab9 - Task2
def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_stock=Sum('book__quantity', default=0)
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_publishers.html',
        {
            'publishers': publishers,
            'task': 2
        }
    )


# Lab9 - Task3
def lab9_task3(request):
    oldest_book = (
        Book.objects
        .filter(publisher=OuterRef('pk'))
        .order_by('pubdate', 'pk')
    )

    publishers = Publisher.objects.annotate(
        oldest_title=Subquery(oldest_book.values('title')[:1]),
        oldest_date=Min('book__pubdate')
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_publishers.html',
        {
            'publishers': publishers,
            'task': 3
        }
    )


# Lab9 - Task4
def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        average_price=Avg('book__price'),
        minimum_price=Min('book__price'),
        maximum_price=Max('book__price')
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_publishers.html',
        {
            'publishers': publishers,
            'task': 4
        }
    )


# Lab9 - Task5
def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count(
            'book',
            filter=Q(book__rating__gte=4)
        ),
        highly_rated_quantity=Sum(
            'book__quantity',
            filter=Q(book__rating__gte=4),
            default=0
        )
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_publishers.html',
        {
            'publishers': publishers,
            'task': 5
        }
    )


# Lab9 - Task6
def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_book_count=Count(
            'book',
            filter=(
                Q(book__price__gt=50)
                & Q(book__quantity__lt=5)
                & Q(book__quantity__gte=1)
            )
        )
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_publishers.html',
        {
            'publishers': publishers,
            'task': 6
        }
    )