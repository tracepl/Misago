from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.threads.mixins import TypeMixin

class NewThreadView(NewThreadBaseView, TypeMixin):
    def set_forum_context(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')

    def response(self):
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("New thread has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(EditThreadBaseView, TypeMixin):
    def response(self):
        self.request.messages.set_flash(Message(_("Your thread has been edited.")), 'success', 'threads_%s' % self.post.pk)
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(NewReplyBaseView, TypeMixin):
    def response(self):
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("Your reply has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads_%s' % self.post.pk)
        else:
            self.request.messages.set_flash(Message(_("Your reply has been posted.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(EditReplyBaseView, TypeMixin):
    def response(self):
        self.request.messages.set_flash(Message(_("Your reply has been changed.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)
