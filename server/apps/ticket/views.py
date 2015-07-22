# coding:utf8

from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
#from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import *
from models import Group, Ticket


def check_auth(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")


def send_mail_ticket(group, send_type):
    subject = u"pokus"
    body = u"Ahoj tohle je generovaný email"
    email_from = "info@varhoo.cz"
    emails = [it.email for it in group.users.all()]
    for email in emails:
        print "send email to %s" % email
        #send_mail(subject, body, email_from,[email,], fail_silently=True)


def show_all(request):
    ret = check_auth(request)
    if ret:
        return ret

    group = Group.objects.filter(users=request.user.id)
    tickets = Ticket.objects.filter(Q(author=request.user.id) | Q(
        group__in=group)).order_by("status", "-priority", "-pub_date")
    return render_to_response('tickets.html',
                              {'tickets': tickets},
                              context_instance=RequestContext(request))


def show_item(request, id):
    ret = check_auth(request)
    if ret:
        return ret

    ticket = Ticket.objects.get(id=id)

    if request.method == 'POST':
        if request.GET.has_key("new") and request.GET["new"] == "comment":
            form = CommentForm(request.POST, files=request.FILES)
            if form.is_valid():
                a = Comment()
                a.text = form.cleaned_data["text"]
                a.is_public = form.cleaned_data["is_public"]
                a.upload_file = form.cleaned_data["upload_file"]
                a.author_id = request.user.id
                a.ticket_id = ticket.id
                a.save()
                # send_mail_ticket(a.group,"new_comment")
                # TODO errot
                # print form.errors

        if request.GET.has_key("edit") and request.GET["edit"] == "ticket":
            form = TicketFormEdit(request.POST, files=request.FILES)
            if form.is_valid():
                ticket.status = form.cleaned_data["status"]
                ticket.priority = form.cleaned_data["priority"]
                ticket.save()
                send_mail_ticket(ticket.group, "edit_ticket")
            # TODO errot print form.errors

    form = {"ticket": TicketForm(instance=ticket),
            "comment": CommentForm()}

    comments = Comment.objects.filter(ticket=ticket.id)

    return render_to_response('ticket_item.html',
                              {'ticket': ticket, 'forms':
                               form, 'comments': comments},
                              context_instance=RequestContext(request))


def new_item(request):
    ret = check_auth(request)
    if ret:
        return ret

    if request.method == 'POST':
        print request.POST
        if request.GET["new"] == "ticket":
            form = TicketForm(request.POST)
            print "valid", form.errors
            if form.is_valid():
                a = Ticket()
                a.title = form.cleaned_data["title"]
                a.text = form.cleaned_data["text"]
                a.priority = form.cleaned_data["priority"]
                a.author = request.user
                a.save()
                send_mail_ticket(a.group, "new_ticket")
                return show_item(request, a.id)

    form = {"ticket": TicketForm(),
            "comment": CommentForm()}

    return render_to_response('ticket_new.html',
                              {'forms': form, },
                              context_instance=RequestContext(request))
