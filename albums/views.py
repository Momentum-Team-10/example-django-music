from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
from .models import Album, Genre
from .forms import AlbumForm, GenreForm
from .view_helpers import admin_user_check, is_ajax
from django.db import IntegrityError
from django.db.models import Q


def homepage(request):
    # show a homepage
    if request.user.is_authenticated:
        return redirect("list_albums")
    return render(request, "albums/homepage.html")


def list_albums(request):
    albums = Album.objects.all().order_by("title")
    return render(request, "albums/list_albums.html", {"albums": albums})


@login_required
@user_passes_test(
    admin_user_check
)  # https://docs.djangoproject.com/en/3.2/topics/auth/default/#django.contrib.auth.decorators.user_passes_test
def add_album(request):
    if request.method == "POST":
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.save()

            return redirect("show_album", pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, "albums/add_album.html", {"form": form})


@user_passes_test(admin_user_check)
def add_genre(request):
    context = {}
    if request.method == "POST":
        form = GenreForm(data=request.POST)
        if form.is_valid():
            try:
                genre = form.save()
                return redirect("show_genre", slug=genre.slug)
            except IntegrityError:
                context["warning"] = "Genre already exists"
                context["form"] = GenreForm()
    else:
        context["form"] = GenreForm()

    return render(request, "albums/add_genre.html", context)


def show_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    albums = genre.albums.all()

    return render(request, "albums/show_genre.html", {"genre": genre, "albums": albums})

@login_required
def show_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    favorited_by_user = request.user.favorite_albums.filter(pk=album.pk).exists()
    return render(
        request,
        "albums/show_album.html",
        {"album": album, "genres": album.genres.all(), "favorited": favorited_by_user },
    )


@user_passes_test(admin_user_check)
@login_required
def edit_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == "GET":
        form = AlbumForm(instance=album)
    else:
        form = AlbumForm(data=request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect("list_albums")

    return render(request, "albums/edit_album.html", {"form": form, "album": album})


@user_passes_test(admin_user_check)
@login_required
def delete_album(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        album.delete()
        messages.success(request, "Album deleted.")
        return redirect("list_albums")

    return render(request, "albums/delete_album.html", {"album": album})


@login_required
def favorite_album(request, pk):
    # get the user
    user = request.user
    # get the album
    album = get_object_or_404(Album, pk=pk)

    if request.method == "DELETE":
        album.favorited_by.remove(user)
        favorited = False
    elif request.method == 'POST':
        album.favorited_by.add(user)
        favorited = True

    if is_ajax(request):
        return JsonResponse({"favorited": favorited })

    return redirect("show_album", pk=pk)



def search_by_title(request):
    # get the search term from the query params
    query = request.GET.get("q")
    # use that search term to make a db query, save it to a variable
    results = Album.objects.filter(title__icontains=query)
    # send back a response that includes the data from the query

    return render(request, "albums/list_albums.html", {"albums": results})


def search_by_title_and_artist(request):
    """Return results for a search on title AND artist."""
    # get the search term from query params like ?artist=Beyonce&title=lemonade
    # note that we don't currently have a template with a search form that allows this
    title_query = request.GET.get("title")
    artist_query = request.GET.get("artist")
    # results must match BOTH lookups
    results = Album.objects.filter(
        title__icontains=title_query, artist__name=artist_query
    )

    return render(request, "albums/list_albums.html", {"albums": results})


def search_by_artist_or_title(request):
    # this search could work with the existing search form
    query = request.GET.get("q")
    # search using a logical OR operator, the `|` character, and Django's `Q` objects
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
    results = Album.objects.filter(
        Q(title__icontains=query) | Q(artist__name__icontains=query)
    )

    return render(request, "albums/list_albums.html", {"albums": results})
