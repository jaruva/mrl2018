# -*- coding: utf-8 -*-
# TODO just fuckin redesign the whole goddamn webpage

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import LoginForm, CreateForm, AddBookForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from datetime import datetime
import pickle
import os
import isbnlib

def get_pickle_location(username):
    ''' Returns a filename for a user's assocciated .pickle file '''
    
    dir_path = os.path.dirname(os.path.normpath(__file__))
    filename = '\\book_data\\' + str(username) + '.pickle'
    filename = dir_path + filename
    return filename

def create_pickle_file(filename):
    ''' Creates an empty .pickle file with the given filename '''
    
    fil = open(filename, 'wb')
    pickle.dump({}, fil)
    fil.close()

def get_pickle_file(mode, user):
    '''mode: what mode you want open() to use
    Creates the file object of the specified .pickle file and returns it, and if it doesnt exists, creates a new .pickle file and returns the new object'''
    
    if mode == 'w' or 'r':
        filename = get_pickle_location(user)
        
        if os.path.exists == False:
            create_pickle_file(filename)
        else:
            f = open(filename, mode + 'b')
            return f
        
    else:
        raise Exception("Enter a valid mode")
        
        
class IndexView(FormView):
    # login
    
    template_name = 'index.html'
    form_class = LoginForm
    success_url = '/user/'

    
    def form_valid(self, form):
        
        data = form.cleaned_data
            
        user = authenticate(self.request, username=data['username'], password=data['password'])
        
        # if the returned user value is None, returns invalid login
        if user != None:
            login(self.request, user)
            return super().form_valid(form)
            
        else:
            context = self.get_context_data()
            context['incorrect'] = 'Invalid login'
            
            return render(self.request, 'index.html', context)


class CreateView(FormView):
    # create user
    
    template_name = 'index.html'
    form_class = CreateForm
    success_url = ''
    
    def form_valid(self, form):
        data = form.cleaned_data
        
        if data['new_password'] != data['confirm_password']:
            # renders the same page with the incorrect tag filled with these parameters
            context = self.get_context_data()
            context['incorrect'] = 'Passwords do not match'
            return render(self.request, 'index.html', context)
            
        # Checks if this is an existing user, and if not makes the variable False for the later If statement
        try:
            is_existing_user = User.objects.get(username=data['new_username'])
            
        except:
            is_existing_user = False
            
        if is_existing_user:
            context = self.get_context_data()
            context['incorrect'] = 'User already exists'
            return render(self.request, 'index.html', context)
        
        # Creaters a new user in the database, and creates an empty
        User.objects.create_user(username=data['new_username'], password=data['new_password'])
        create_pickle_file(get_pickle_location(self))
        return super().form_valid(form)
                       
                       
class UserView(TemplateView):
    # display user data
    
    # redirects unauthorised users to the login page
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    template_name = 'user.html'
    
    def get_context_data(self, **kwargs):
        # fills user tag with currently logged in user
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        
        # grabs data from the users associated .pickle file, and fills the books tag with the data
        book_data = get_pickle_file('r', self.request.username)
        books = pickle.load(book_data)
        book_data.close()
        context['books'] = books
        # todo make this dictionary multiple iterables
        return context
            
            
class AddBook(FormView):
    # add book
    
    # redirects unauthorised users to the login page
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    template_name = 'addbook.html'
    form_class = AddBookForm
    success_url = '/user/'
    
    def form_valid(self, form):

        data = form.cleaned_data
        
        # tries to grab the associated book metadata from openlibrary.com's API, or fills the incorrect tag
        try:
            book = isbnlib.meta(data['ISBN'], 'openl')
            
        except:
            context = self.get_context_data()
            context['incorrect'] = 'Invalid ISBN'
            return render(self.request, 'addbook.html', context)
        
        # Appends to the user's .pickle file
        book_data = get_pickle_file('r', self)
        time = datetime.now().replace(microsecond=0)
        dic = pickle.load(book_data)
        dic[time] = book
        book_data.close()
        book_data = get_pickle_file('w', self)
        pickle.dump(dic, book_data)
        book_data.close()
        
        return super().form_valid(form)