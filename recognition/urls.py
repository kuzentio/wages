from recognition.views import RecogniseViewSet

recognise_view = RecogniseViewSet.as_view({
    'post': 'retrieve'
})
