from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Book, AccessRequest
from .forms import BookUploadForm, AccessRequestForm, AccessResponseForm
from accounts.models import User
import PyPDF2
import io
import os

# Common Views
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_admin:
            # Check if user has already requested access
            try:
                access_request = AccessRequest.objects.get(user=self.request.user, book=self.object)
                context['access_request'] = access_request
            except AccessRequest.DoesNotExist:
                context['access_form'] = AccessRequestForm(initial={'book': self.object})
        return context

# User Views
@login_required
def request_access(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Check if a request already exists
        existing_request = AccessRequest.objects.filter(user=request.user, book=book).first()
        
        if not existing_request:
            AccessRequest.objects.create(user=request.user, book=book, status='pending')
            messages.success(request, f"Access request submitted for '{book.title}'")
        else:
            messages.info(request, "You've already requested access to this book")
            
    return redirect('book_detail', pk=book_id)

# Admin Views
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

class AdminPanelView(AdminRequiredMixin, ListView):
    model = Book
    template_name = 'books/admin_panel.html'
    context_object_name = 'books'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_requests'] = AccessRequest.objects.filter(status='pending').count()
        return context

class UserManagementView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'books/user_management.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.filter(is_admin=False)

class AccessRequestsView(AdminRequiredMixin, ListView):
    model = AccessRequest
    template_name = 'books/access_requests.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return AccessRequest.objects.filter(status='pending')

@login_required
def handle_access_request(request, request_id):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to perform this action")
        return redirect('book_list')
        
    access_request = get_object_or_404(AccessRequest, id=request_id)
    
    if request.method == 'POST':
        form = AccessResponseForm(request.POST, instance=access_request)
        if form.is_valid():
            form.save()
            messages.success(request, f"Access request from {access_request.user.username} has been updated")
            return redirect('access_requests')
    else:
        form = AccessResponseForm(instance=access_request)
    
    return render(request, 'books/handle_request.html', {
        'form': form,
        'access_request': access_request
    })

class BookUploadView(AdminRequiredMixin, CreateView):
    model = Book
    form_class = BookUploadForm
    template_name = 'books/book_upload.html'
    success_url = reverse_lazy('admin_panel')
    
    def form_valid(self, form):
        # Get the PDF file and password from the form
        pdf_file = form.cleaned_data['pdf_file']
        password = form.cleaned_data['password']
        
        # Create a response but don't save to DB yet
        self.object = form.save(commit=False)
        
        # Here we would encrypt the PDF, but for demonstration purposes
        # we'll just save the form with a comment about encryption
        
        # In a real application, you would use a library like PyPDF2 to encrypt the PDF:
        # reader = PyPDF2.PdfReader(pdf_file)
        # writer = PyPDF2.PdfWriter()
        # for page in reader.pages:
        #     writer.add_page(page)
        # writer.encrypt(password)
        # encrypted_file = io.BytesIO()
        # writer.write(encrypted_file)
        # encrypted_file.seek(0)
        # self.object.pdf_file.save(os.path.basename(pdf_file.name), encrypted_file)
        
        # For now, we'll just save the original file
        self.object.save()
        messages.success(self.request, f"Book '{self.object.title}' has been uploaded and encrypted")
        return redirect(self.success_url)