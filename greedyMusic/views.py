
from models import Track,Genre
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.views.generic import ListView,DetailView
from .forms import FormForGenre,TrackRequestForm
import re
from django.db.models import Q
import logging
logger = logging.getLogger('django')

REQUEST_POST="POST"

class TrackListView(ListView):

    trackAll = Track.objects.all()
    model = trackAll
    paginate_by = 4
    template_name = 'track.html'


def viewTrack(request):
#This function is used to display tracks in list view
    tracksDict = Track.objects.all()
    return render_to_response('track.html', tracksDict,context_instance=RequestContext(request))

class trackDetailView(DetailView):
    context_object_name = 'trackDetail'
    template_name = "trackDetail.html"
    allow_empty = True
    model = Track
    slug_field = 'pk' # 'name' is field of Customer Model

def viewTrackDetail(request, slug):
#This function is used to display tracks in detail view
    if request.method == "GET":
        if slug:
            return trackDetailView.as_view()(request, slug=slug)

def editTracks(request):
#This function edits a perticular track
    trackObj = get_object_or_404(Track, pk=request.GET['pk'])
    form = TrackRequestForm(request.POST or None, instance=trackObj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('track_list')


    return render_to_response('editTrack.html',{'form': form,},context_instance=RequestContext(request))

def editGenre(request):
#This function is used to edit a perticular genre
    genreObj = get_object_or_404(Genre, pk=request.GET['pk'])
    form = FormForGenre(request.POST or None, instance=genreObj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('viewGenre')


    return render_to_response('editGenre.html',{'form': form,},context_instance=RequestContext(request))




class genereDetailView(DetailView):
    context_object_name = 'genreDetail'
    template_name = "genreDetail.html"
    allow_empty = True
    model = Genre
    slug_field = 'pk' # 'name' is field of Customer Model

def viewGenreDetail(request, slug):
    #This function displays Genres in Detail form
    if request.method == "GET":
        if slug:
            return genereDetailView.as_view()(request, slug=slug)


def viewGenre1(request):
    #This function displays the genres in list form
    genreList=Genre.objects.all()
    genreDict = {}
    genreDict['genreList'] = genreList
    return render_to_response('genre.html', genreDict,context_instance=RequestContext(request))

def insertTracks(request):
#This function inserts the a new track in Track Table
    if request.method == "POST":
        form = TrackRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('track_list')
    else:
        form = TrackRequestForm()
    return render_to_response('addNewTrack.html',{'form': form},context_instance=RequestContext(request))

def insertGenre(request):
#This function inserts the a new genre in Genre Table
    if request.method == "POST":
        form = FormForGenre(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = request.POST['Name']
            post.save()
            return redirect('viewGenre')
    else:
        form = FormForGenre()
    return render_to_response('addNewGenre.html',{'form': form},context_instance=RequestContext(request))



def normalizeQuery(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term
    terms = normalizeQuery(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    key = 0
    if ('search_text' in request.GET) and request.GET['search_text'].strip():
        query_string = request.GET['search_text']

        entry_query = get_query(query_string, ['Title'])
        found_entries = Track.objects.filter(entry_query)
        key = 1

        if not found_entries:
            entry_query = get_query(query_string, ['Name'])
            found_entries = Genre.objects.filter(entry_query)
            key = 2

    return render_to_response('searchResults.html',
                          { 'query_string': query_string, 'found_entries': found_entries,'key':key },
                          context_instance=RequestContext(request))