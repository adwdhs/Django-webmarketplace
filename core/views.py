from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item, Conversation, ConversationMessage
from .forms import SighupForm, newItemForm, editItemForm, ConversationMessageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.contrib import auth

@login_required(login_url='login')
def newConversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.user == request.user:
        return redirect('index')

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.user)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.users = request.user
            conversation_message.save()

            return redirect('details', pk=item_pk)
    else:
        form = ConversationMessageForm()
    return render(request, 'core/new.html', {'form': form})







def browse(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)


    if category_id:
        items = items.filter(categoty_id=category_id)


    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(categoty__name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {'items': items, 'query': query, 'categories': categories, 'category_id': int(category_id)}
    return render(request, 'core/items.html', context)



def contacts(request):
    return render(request, 'core/contacts.html')

def detail(requsest, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(categoty=item.categoty, is_sold=False).exclude(pk=pk)[0:3]

    context = {'item': item, 'related_items': related_items}
    return render(requsest, 'core/detail.html', context)


class LogoutView(View):
    def post(self, request):
        auth.logout(request)

        return redirect('/')



def sighup(request):

    if request.method == "POST":
        form = SighupForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/login/')
    else:
        form = SighupForm()

    context = {'form': form}
    return render(request, 'core/sighup.html', context)
@login_required(login_url='login')
def newItem(request):
    if request.method == 'POST':
        form = newItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

            return redirect('details', pk=item.id)

    else:
        form = newItemForm()

    return render(request, 'core/form.html', {'form': form, 'title': 'Add New Item'})


@login_required(login_url='login')
def dashboard(request):
    items = Item.objects.filter(user=request.user)

    context = {
        'items': items
    }

    return render(request,'core/dashboard.html',context)

@login_required(login_url='login')
def deleteItem(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    item.delete()

    return redirect('dashboard')

@login_required(login_url='login')
def editItem(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)

    if request.method == 'POST':
        form = editItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()

            return redirect('details', pk=item.id)

    else:
        form = editItemForm(instance=item)

    return render(request, 'core/form.html', {'form': form, 'title': 'Edit Item'})

@login_required(login_url='login')
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'core/inbox.html', {'conversations': conversations})

@login_required(login_url='login')
def message(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    form = ConversationMessageForm()

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.users = request.user
            conversation_message.save()
            form = ConversationMessageForm()



    context = {'conversation': conversation, 'form': form}
    return render(request, 'core/messages.html', context)



