from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows

@login_required(login_url='login')
def feed(request):
    # Récupérer les utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    
    # Récupérer les tickets et critiques
    followed_tickets = Ticket.objects.filter(user__in=followed_users)
    followed_reviews = Review.objects.filter(user__in=followed_users)
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    response_reviews = Review.objects.filter(ticket__in=user_tickets)

    # Combiner et trier les posts
    all_posts = sorted(
        chain(followed_tickets, followed_reviews, user_tickets, user_reviews, response_reviews),
        key=lambda x: x.time_created,
        reverse=True
    )

    # Pagination
    paginator = Paginator(all_posts, 10)  # 10 posts par page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Ajouter le type de contenu pour chaque post
    for post in posts:
        if isinstance(post, Ticket):
            post.content_type = 'TICKET'
            post.can_review = post.can_be_reviewed_by(request.user)
        else:
            post.content_type = 'REVIEW'
    
    context = {
        'posts': posts,
        'page_obj': posts,  # Pour la pagination dans le template
    }
    return render(request, 'func/feed.html', context)


@login_required(login_url='login')
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = TicketForm()
    return render(request, 'func/ticket_create.html', {'form': form})

@login_required(login_url='login')
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('feed')
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'func/ticket_edit.html', {'form': form})

@login_required(login_url='login')
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('feed')
    if request.method == 'POST':
        ticket.delete()
        return redirect('feed')
    return render(request, 'func/ticket_delete.html', {'ticket': ticket})

@login_required(login_url='login')
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not ticket.can_be_reviewed_by(request.user):
        return redirect('feed')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    else:
        form = ReviewForm()
    return render(request, 'func/create_review.html', {'form': form, 'ticket': ticket})

@login_required(login_url='login')
def create_ticket_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'func/create_ticket_review.html', 
                 {'ticket_form': ticket_form, 'review_form': review_form})

@login_required(login_url='login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('feed')
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'func/edit_review.html', {'form': form})

@login_required(login_url='login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('feed')
    if request.method == 'POST':
        review.delete()
        return redirect('feed')
    return render(request, 'func/delete_review.html', {'review': review})