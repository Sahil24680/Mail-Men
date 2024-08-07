from django.shortcuts import render, get_object_or_404, redirect
from .models import Email, Inbox
from .serializers import Emailserializer,InboxSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from login.models import CustomUser
from rest_framework.decorators import api_view
from django.contrib.auth import logout
from django.utils.timesince import timesince
from django.http import HttpResponse
import plotly.graph_objects as go


@api_view(['GET'])
@login_required(login_url='login/')
def get_emails(request):
    user = request.user  # Get the currently logged-in user
    inbox, created = Inbox.objects.get_or_create(inbox_user=user)
    emails = Email.objects.filter(To=user, archived=False, starred=False).order_by('-timestamp')  # Order emails by timestamp (newest to oldest) # Filter emails where the recipient is the logged-in user
    serializer = Emailserializer(emails, many=True)
    inbox = get_object_or_404(Inbox, inbox_user=user)  # Get the inbox for the logged-in user
    inbox_serializer = InboxSerializer(inbox)
    return render(request, 'emails.html', {'emails': serializer.data, 'inbox': inbox_serializer.data})


def send_email(request):
    if request.method == 'POST':
        sender = request.user  # The currently logged-in user
        recipient_email = request.POST.get('recipient_email')
        recipient = get_object_or_404(CustomUser, email=recipient_email)
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        # Create the email
        email = Email.objects.create(sender=sender, To=recipient, subject=subject, body=body)

        # Get or create the recipient's inbox
        inbox, created = Inbox.objects.get_or_create(inbox_user=recipient)

        if not inbox.inbox.filter(id=email.id).exists():
            inbox.inbox.add(email)

        # Update the email count to the correct number
        if inbox.inbox.count() == 0:
             inbox.num_inbox = 0
        else:
            inbox.num_inbox = inbox.inbox.count()
        inbox.save()


        messages.success(request, 'Email sent successfully!')
        return redirect('all_emails')

    return render(request, 'emails.html')  # Render the email sending form


def delete_email(request,email_id):
    if request.method =='POST':
        email = get_object_or_404(Email, pk=email_id)
        user = request.user  
        email.delete()

        # Update the corresponding inbox count after deletion
        inbox = get_object_or_404(Inbox, inbox_user=user)
        inbox.num_inbox = inbox.inbox.count()
        inbox.save()


    return redirect('all_emails')



def search(request):   #used for serahing up emails
    emails_ = []  
    if request.method == 'POST':
        searched = request.POST.get('searched_user')
        user = request.user
        inboxes = Inbox.objects.filter(inbox_user=user)

        for i in inboxes:
            emails = i.inbox.filter(sender__email__icontains=searched) # this allows it so you can search up "sahil" and it will show u all the emaisl containing that
            emails_.extend(emails)  # Add emails to the list

    return render(request, 'search.html', {'emails': emails_})









def logout_(request):
    
    logout(request)
    return redirect('/')

def get_reply_thread(email):  #used to create a theard for all the replies to an email
    replies = email.replies.all().order_by('-timestamp')
    thread = []
    
    for reply in replies:
        thread.extend(get_reply_thread(reply))
    thread.append(email)
    
    return thread

def format_timestamp(email):
    formatted_date = email.timestamp.strftime("%b %d, %Y, %I:%M %p")  # used to fromal the email that was clicked so i didnt have to seralize it again
    time_ago = timesince(email.timestamp) + " ago"
    return f"{formatted_date} ({time_ago})"

def clicked_email(request, id):
    user = request.user
    email = get_object_or_404(Email, id=id)
    email.is_read = True
    email.save()

    
    email.timestamp_formatted = format_timestamp(email)

    
    reply= get_reply_thread(email)
    replies= Emailserializer(reply,many=True)


    return render(request, 'email_clicked.html', {'email': email, 'replies': replies.data, 'user': user})


def send_reply(request, email_id):
    if request.method == 'POST':
        original_email = get_object_or_404(Email, id=email_id)
        sender = request.user  # The currently logged-in user
        subject = request.POST.get('subject')
        body = request.POST.get('body')

       
        reply_email = Email.objects.create(sender=sender, To=original_email.sender, subject=subject, body=body)

        inbox, created = Inbox.objects.get_or_create(inbox_user=original_email.sender)
        
        if not inbox.inbox.filter(id=reply_email.id).exists():
            inbox.inbox.add(reply_email)

       
        if inbox.inbox.count() == 0:
             inbox.num_inbox = 0
        else:
            inbox.num_inbox = inbox.inbox.count()
        inbox.save()

        # Add the reply email to the original email's reply_ids
        original_email.reply_ids.add(reply_email)
        original_email.save()

        messages.success(request, 'Reply sent successfully!')
        return redirect('all_emails')

    return render(request, 'email_clicked.html', {})




@login_required
def Profile(request):
    user = request.user
    if request.method == 'POST':
        new_user = request.POST.get('new_user')
        new_pass = request.POST.get('new_pass')
        new_email = request.POST.get('new_email')
        
        
        try:
            u = CustomUser.objects.get(username=user.username)
        except CustomUser.DoesNotExist:
            return HttpResponse("User profile not found.", status=404)
        
        
        u.username = new_user
        u.email = new_email
        if new_pass:
            u.set_password(new_pass)
        
        
        u.save()
        
        
        return redirect('login') 
    
   
    return render(request, 'update_profile.html', {})


def newpfp(request):
    if request.method == 'POST':
        newpfp = request.FILES.get('new_pfp')
        user = request.user
        user.pfp = newpfp
        user.save()
    return redirect('profile')


def archive(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    user = request.user
    inbox, created = Inbox.objects.get_or_create(inbox_user=user)

    if email.To == user:
        if email.archived:
            
            email.archived = False
            messages.success(request, 'Email un-archived successfully!')
        else:
            
            email.archived = True
            email.starred = False
            messages.success(request, 'Email archived successfully!')

        email.save()
        inbox.archived_inbox = Email.objects.filter(archived=True, To=user).count()  # Update archived_inbox count
        inbox.starred_inbox = Email.objects.filter(starred=True, To=user).count() 
        inbox.num_inbox = Email.objects.filter(archived=False, To=user,starred=False).count() 
        inbox.save()

    return redirect('all_emails')



def starred(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    user = request.user
    inbox, created = Inbox.objects.get_or_create(inbox_user=user)

    if email.To == user:
        if email.starred:
             
            email.starred = False
            messages.success(request, 'Email un-starred successfully!')
        else:
             # Decrement inbox count since email is being starred
            email.starred = True
            email.archived = False  # Ensure email is not archived if starred
            messages.success(request, 'Email starred successfully!')

        email.save()
        inbox.starred_inbox = Email.objects.filter(starred=True, To=user).count()  # Update starred_inbox count
        inbox.archived_inbox = Email.objects.filter(archived=True, To=user).count() 
        inbox.num_inbox = Email.objects.filter(archived=False, To=user,starred=False).count() 
        inbox.save()

    return redirect('all_emails')

def archived_emails(request):
    user = request.user
    emails = Email.objects.filter(To=user, archived=True, starred=False).order_by('-timestamp')
    serializer = Emailserializer(emails, many=True)
    inbox = get_object_or_404(Inbox, inbox_user=user)
    inbox_serializer = InboxSerializer(inbox)
    return render(request, 'archived.html', {'emails': serializer.data,'inbox': inbox_serializer.data})

def starred_emails(request):
    user = request.user
    emails = Email.objects.filter(To=user, archived=False, starred=True).order_by('-timestamp')
    serializer = Emailserializer(emails, many=True)
    inbox = get_object_or_404(Inbox, inbox_user=user)
    inbox_serializer = InboxSerializer(inbox)
    return render(request, 'starred.html', {'emails': serializer.data,'inbox': inbox_serializer.data})


def Graph_data(request):
    user =request.user
    sent = Email.objects.filter(sender=user).count()
    recieved= Email.objects.filter(To=user).count()
    seen =Email.objects.filter(is_read=True,To =user).count()
    starred = Email.objects.filter(starred=True,To =user).count()
    archived =Email.objects.filter(archived=True,To =user).count()
    labels = ['sent','recieved','seen','starred','archived']
    values = [sent,recieved,seen,starred,archived]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    label_colors = ['#1f77b4', 'lightgray', '#2ca02c', '#FFD700', '#808080']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=label_colors),  
        
    )])
    chart = fig.to_html()
    return render(request, 'graphs.html', {'chart':chart})