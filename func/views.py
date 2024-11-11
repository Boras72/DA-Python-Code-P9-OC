from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from itertools import chain
from .forms import TicketForm, ReviewForm, UserSearchForm
from .models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError

User = get_user_model()

@login_required(login_url='login')
def feed(request):
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    
    followed_tickets = Ticket.objects.filter(user__in=followed_users)
    followed_reviews = Review.objects.filter(user__in=followed_users)
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    response_reviews = Review.objects.filter(ticket__in=user_tickets)

    all_posts = sorted(
        chain(followed_tickets, followed_reviews, user_tickets, user_reviews, response_reviews),
        key=lambda x: x.time_created,
        reverse=True
    )

    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    for post in posts:
        if isinstance(post, Ticket):
            post.content_type = 'TICKET'
            post.can_review = post.can_be_reviewed_by(request.user)
        else:
            post.content_type = 'REVIEW'

    context = {
        'posts': posts,
        'page_obj': posts,
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
            messages.success(request, "Votre demande de critique a été publiée.")
            return redirect('feed')
    else:
        form = TicketForm()
    return render(request, 'func/ticket_create.html', {'form': form})

@login_required(login_url='login')
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        messages.error(request, "Vous n'avez pas la permission de modifier ce ticket.")
        return redirect('feed')
    
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Le ticket a été modifié avec succès.")
            return redirect('posts')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'func/ticket_edit.html', {'form': form, 'ticket': ticket})

@login_required(login_url='login')
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce ticket.")
        return redirect('feed')
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
        return redirect('posts')
    return render(request, 'func/ticket_delete.html', {'ticket': ticket})

@login_required(login_url='login')
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Vérifier si l'utilisateur a déjà créé une critique pour ce ticket
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, "Vous avez déjà créé une critique pour ce ticket.")
        return redirect('feed')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            try:
                review.save()
                messages.success(request, "Votre critique a été créée avec succès.")
                return redirect('feed')
            except IntegrityError:
                messages.error(request, "Une erreur est survenue lors de la création de la critique.")
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'ticket': ticket
    }
    return render(request, 'func/create_review.html', context)

@login_required(login_url='login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette critique.")
        return redirect('feed')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "La critique a été modifiée avec succès.")
            return redirect('posts')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'func/edit_review.html', {'form': form, 'review': review})

@login_required(login_url='login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette critique.")
        return redirect('feed')
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "La critique a été supprimée avec succès.")
        return redirect('posts')
    return render(request, 'func/delete_review.html', {'review': review})

@login_required(login_url='login')
def create_ticket_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        
        if ticket_form.is_valid() and review_form.is_valid():
            try:
                with transaction.atomic():
                    ticket = ticket_form.save(commit=False)
                    ticket.user = request.user
                    ticket.save()
                    
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.ticket = ticket
                    review.save()
                
                messages.success(request, "Votre critique a été publiée avec succès.")
                return redirect('feed')
            except IntegrityError:
                messages.error(request, "Une erreur est survenue lors de la création de la critique.")
    
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request, 'func/create_ticket_review.html', context)

@login_required(login_url='login')
def posts(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    
    all_posts = sorted(
        chain(user_tickets, user_reviews),
        key=lambda x: x.time_created,
        reverse=True
    )
    
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    for post in posts:
        if isinstance(post, Ticket):
            post.content_type = 'TICKET'
        else:
            post.content_type = 'REVIEW'
    
    return render(request, 'func/posts.html', {'posts': posts})

@login_required(login_url='login')
def subscriptions(request):
    form = UserSearchForm(request.POST or None)
    search_results = []
    
    if request.method == 'POST' and form.is_valid():
        search_query = form.cleaned_data['username']
        search_results = User.objects.filter(
            Q(username__icontains=search_query) & 
            ~Q(id=request.user.id)
        )
        
        if not search_results:
            messages.error(request, f"Aucun utilisateur trouvé avec le nom '{search_query}'")
    
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    
    context = {
        'form': form,
        'search_results': search_results,
        'following': following,
        'followers': followers,
    }
    
    return render(request, 'func/subscriptions.html', context)

@login_required(login_url='login')
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if user_to_follow == request.user:
        messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
        return redirect('subscriptions')
    
    try:
        UserFollows.objects.create(
            user=request.user,
            followed_user=user_to_follow
        )
        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}")
    except IntegrityError:
        messages.error(request, f"Vous suivez déjà {user_to_follow.username}")
    
    return redirect('subscriptions')

@login_required(login_url='login')
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    follow = UserFollows.objects.filter(
        user=request.user,
        followed_user=user_to_unfollow
    ).first()
    
    if follow:
        follow.delete()
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}")
    else:
        messages.error(request, f"Vous ne suiviez pas {user_to_unfollow.username}")
    
    return redirect('subscriptions')