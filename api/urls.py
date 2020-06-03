from vegetable.views import VegetableListViewSet

vegetable_list = VegetableListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
