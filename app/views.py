from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from django.utils.http import urlencode
from urllib.parse import urlparse, urlunparse


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

    url_schema = list(urlparse(reverse('bus_stations')))

    if page.has_next():
        # var.1
        # next_page_url = '?'.join((reverse('bus_stations'), urlencode({'page': page.next_page_number()})))
        # var.2
        url_schema[4] = urlencode({'page': page.next_page_number()})
        next_page_url = urlunparse(url_schema)

    if page.has_previous():
        # var.1
        # prev_page_url = '?'.join((reverse('bus_stations'), urlencode({'page': page.previous_page_number()})))
        # var.2
        url_schema[4] = urlencode({'page': page.previous_page_number()})
        prev_page_url = urlunparse(url_schema)

    return render(request, 'index.html', context={
        'bus_stations': paginator.page(current_page),
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
