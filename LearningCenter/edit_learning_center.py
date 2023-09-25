from django.contrib.auth.decorators import login_required
from .forms import CustomLearningCenterForm
from django.shortcuts import render, redirect

@login_required
def edit_learning_center(request):
    if request.method == 'POST':
        form = CustomLearningCenterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_learning_center') # change direction of redirect to learning center profile page
    else:
        form = CustomLearningCenterForm(instance=request.user)
    return render(request, 'edit_learning_center.html', {'form': form})