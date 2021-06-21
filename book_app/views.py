from django.contrib import messages
from django.shortcuts import render, redirect
from book_app.models import *
# Create your views here.
def home (request):
# user's home page where they can add and see all books
    logged_user= User.objects.get(id=request.session['user'])
    context = {
        "all_books": Book.objects.all(),
        "users_info": User.objects.get(id=request.session['user'])
    }
    return render(request, 'book/index.html', context)

def logout (request):
# log the user out and return them to login and registration page
    request.session.flush()
    return redirect('/')

def create (request):
# creates a new book to add to database
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        logged_user = User.objects.get(id=request.session['user'])
        if len(errors) > 0:
            for value in errors.items():
                messages.error(request,value)
            return('/book/home')

        added_book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = logged_user,
        )
        added_book.users_who_like.add(logged_user)
    return redirect('/book/home')

def edit (request, book_id):
# where the user can edit their book's title and description if they are the ones who created it
    book_to_edit = Book.objects.get(id=book_id)
    users_info = User.objects.get(id=request.session['user'])
    context = {
        "users_info": User.objects.get(id=request.session['user']),
        "book": book_to_edit,
    }
    return render( request, 'book/edit.html',context)


def update (request, book_id):
# method to actually edit the book
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for value in errors.items():
                messages.error(request,value)
            return redirect(f'/book/edit/{book_id}')

        make_update = Book.objects.get(id=book_id)
        make_update.title = request.POST['title']
        make_update.description = request.POST['description']
        make_update.save()
    return redirect('/book/home')

def delete (request, book_id):
# deletes a book from the database if they are the one who create it
    if request.method == "POST":
        book_to_delete = Book.objects.get(id=book_id)
        if book_to_delete.uploaded_by.id == request.session['user']:
            book_to_delete.delete()
    return redirect('/book/home')

def show (request, book_id):
# shows a page of the books infomation
    logged_user = User.objects.get(id=request.session['user'])
    book_to_show = Book.objects.get(id=book_id)
    context = {
        "users_info": logged_user,
        "book_info": book_to_show,
    }
    return render(request, 'book/show.html', context)

def favorite (request, book_id):
# Adds the book to user's list of favorites
    logged_user = User.objects.get(id=request.session['user'])
    book = Book.objects.get(id=book_id)
    logged_user.liked_books.add(book)
    return redirect(f'/book/{book_id}')

def unfavorite (request, book_id):
# Removes the book from user's list of favorites
    logged_user = User.objects.get(id=request.session['user'])
    book= Book.objects.get(id=book_id)
    logged_user.liked_books.remove(book)
    return redirect(f'/book/{book_id}')