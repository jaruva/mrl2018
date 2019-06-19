from django.shortcuts import render, redirect
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

def get_pickle_file(mode):
    '''mode: what mode you want open() to use
    Creates the object of the specified .pickle file and returns it, and if it doesnt exists, creates a new .pickle file and returns the new object'''
    dir_path = os.path.dirname(os.path.normpath(__file__))
    filename = '\\book_data\\' + str(super().self.request.user) + '.pickle'
    filename = dir_path + filename
    f = open(filename, mode + 'b')
    
    if os.path.exists(filename):
        return f
    else:
        pickle.dump({}, f)
        return f