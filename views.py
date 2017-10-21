from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
# Create your views here.
from .models import Post
from urllib import quote_plus
from django.utils import timezone
from django.db.models import Q

#from .forms import PostForm

def post_create(request):
    return HttpResponse("<h1>create</h1>")

'''def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()

    if request.method == "POST":
        print request.POST.get("title")
        print request.POST.get("content")

        context = {
        "form": form,
    }
        return render(request, "post_forms.html", context)'''


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "post_details.html", context)

def post_list(request):
    today = timezone.now().date()
    quearyset_list = Post.objects.active()    # filter(draft=False).filter(publish__lte=timezone.now())  #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        quearyset_list = Post.objects.all()

    queary = request.GET.get("q")
    if queary:
        quearyset_list = quearyset_list.filter(
            Q(title__icontains=queary)|
            Q(content__icontains=queary)|
            Q(user__first_name__icontains=queary)|
            Q(user__last_name__icontains=queary)
            ).distinct()
    paginator = Paginator(quearyset_list, 5)  # Show 25 contacts per page
    #page_request_var = "page"
    page = request.GET.get('page')
    try:
        quearyset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quearyset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        quearyset = paginator.page(paginator.num_pages)

    template = 'post.html'
    context = {
        "object_list": quearyset,
        "title": "List",
        #"page_request_var": page_request_var
        "today": today,
    }

    return render(request, template, context)

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")