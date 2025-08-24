import random
from django.db import transaction
from django.db.models import Count, Sum, F
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import QuoteForm
from .models import Quote, Vote, ViewEvent

def _get_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def random_quote(request):
    qs = Quote.objects.filter(is_active=True)
    if not qs.exists():
        return render(request, 'quotes/random.html', {'quote': None})

    pairs = list(qs.values_list('id', 'weight'))
    ids, weights = zip(*pairs)
    chosen_id = random.choices(population=ids, weights=weights, k=1)[0]

    session_key = _get_session_key(request)
    with transaction.atomic():
        Quote.objects.filter(pk=chosen_id).update(views=F('views') + 1)
        ViewEvent.objects.create(quote_id=chosen_id, session_key=session_key)

    quote = Quote.objects.get(pk=chosen_id)
    return render(request, 'quotes/random.html', {'quote': quote})

def like_quote(request, pk):
    if request.method != 'POST':
        raise Http404()
    quote = get_object_or_404(Quote, pk=pk, is_active=True)
    session_key = _get_session_key(request)
    with transaction.atomic():
        vote, created = Vote.objects.get_or_create(quote=quote, session_key=session_key, defaults={'value': Vote.LIKE})
        if created:
            Quote.objects.filter(pk=quote.pk).update(likes=F('likes') + 1)
        else:
            if vote.value == Vote.DISLIKE:
                Quote.objects.filter(pk=quote.pk).update(likes=F('likes') + 1, dislikes=F('dislikes') - 1)
                vote.value = Vote.LIKE
                vote.save()
        quote.refresh_from_db(fields=['likes','dislikes'])
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def dislike_quote(request, pk):
    if request.method != 'POST':
        raise Http404()
    quote = get_object_or_404(Quote, pk=pk, is_active=True)
    session_key = _get_session_key(request)
    with transaction.atomic():
        vote, created = Vote.objects.get_or_create(quote=quote, session_key=session_key, defaults={'value': Vote.DISLIKE})
        if created:
            Quote.objects.filter(pk=quote.pk).update(dislikes=F('dislikes') + 1)
        else:
            if vote.value == Vote.LIKE:
                Quote.objects.filter(pk=quote.pk).update(dislikes=F('dislikes') + 1, likes=F('likes') - 1)
                vote.value = Vote.DISLIKE
                vote.save()
        quote.refresh_from_db(fields=['likes','dislikes'])
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('quotes:random'))
    else:
        form = QuoteForm()
    return render(request, 'quotes/add.html', {'form': form})

def top_quotes(request):
    qs = Quote.objects.filter(is_active=True).order_by('-likes', 'dislikes', '-weight', '-views')[:10]
    return render(request, 'quotes/top.html', {'quotes': qs})

def dashboard(request):
    total_quotes = Quote.objects.count()
    active_quotes = Quote.objects.filter(is_active=True).count()
    top_sources = (Quote.objects.filter(is_active=True)
                   .values('source__name')
                   .annotate(cnt=Count('id'), likes=Sum('likes'), views=Sum('views'))
                   .order_by('-likes')[:10])
    return render(request, 'quotes/dashboard.html', {
        'total_quotes': total_quotes,
        'active_quotes': active_quotes,
        'top_sources': top_sources,
    })
