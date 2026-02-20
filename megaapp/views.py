from django.shortcuts import render
from .models import Tweet
from .forms import tweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.
def home(request):
    return render(request,'first.html')

def Tweet_List(request):
    tweets=Tweet.objects.all().distinct()
    
    return render(request,'tweet_list.html',{
        "tweets":tweets
    })

@login_required
def Tweet_create(request):
    if request.method=='POST':
      form= tweetForm(request.POST,request.FILES)
      if form.is_valid():
          tweet=form.save(commit=False)
          tweet.user=request.user
          tweet.save()
          return redirect('tweet_List')
    
    else:
        form=tweetForm()
    return render(request,'tweet_form.html',{'form':form})    


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = tweetForm(request.POST,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_List') 
    else:
        form = tweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request,tweet_id):
    
     tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
     if request.method=='POST':
         tweet.delete()
         return redirect('tweet_List')    
     return render(request,'tweet_delete.html',{'tweet':tweet})


def register(request):
     if request.method=='POST':
         form=UserRegistrationForm(request.POST)
         if form.is_valid():
             user=form.save(commit=False)
             user.set_password(form.cleaned_data['password1'])
             user.save()
             login(request,user)
             return redirect('tweet_List')
             

     else:
         form=UserRegistrationForm()
     return render(request,'registration/register.html',{'form':form})




    


