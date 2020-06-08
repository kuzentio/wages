from vegetable.views import VegetableListViewSet, VegetableImageList

vegetable_list = VegetableListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

vegetable_image_list = VegetableImageList.as_view({
    'post': 'create'
})
