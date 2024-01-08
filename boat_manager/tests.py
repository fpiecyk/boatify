from django.test import TestCase

# Create your tests here.

# @method_decorator(login_required, name='dispatch')
# class PierCreateView(CreateView):
#     model = Pier
#     form_class = PierForm
#     template_name = 'pier_create.html'
#     success_url = reverse_lazy('piers')
#
#     def form_invalid(self, form):
#         error = "Formularz zawiera błędy."
#         return render(self.request, self.template_name, {'error': error, 'form': form})
#
#
# @method_decorator(login_required, name='dispatch')
# class PierUpdateView(UpdateView):
#     model = Pier
#     form_class = PierForm
#     template_name = 'pier_create.html'
#     success_url = reverse_lazy('piers')
#
#     def form_invalid(self, form):
#         error = "Formularz zawiera błędy."
#         return render(self.request, self.template_name, {'error': error, 'form': form})
#
#
# @method_decorator(login_required, name='dispatch')
# class PierDeleteView(DeleteView):
#     model = Pier
#     success_url = reverse_lazy('piers')
#     template_name = 'pier_confirm_delete.html'
#
#
# @method_decorator(login_required, name='dispatch')
# class PierListView(ListView):
#     model = Pier
#     template_name = 'piers.html'
