from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    next_page_url = None
    prev_page_url = None
    current_page = request.GET.get('page')

    with open('data-398-2018-08-30.csv') as f:
        data = [
            item
            for item in csv.DictReader(f)
        ]

    paginator = Paginator(data, 20)

    try:
        page = paginator.page(current_page)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)
        current_page = 1

    if page.has_next():
        next_page_url = "%s?page=%s" % (reverse('bus_stations'), page.next_page_number())

    if page.has_previous():
        prev_page_url = "%s?page=%s" % (reverse('bus_stations'), page.previous_page_number())

    return render(request, 'index.html', context={
        'bus_stations': paginator.page(current_page),
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
