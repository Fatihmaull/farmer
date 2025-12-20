from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MarketPrice
from farm.models import Crop


@login_required
def market_price_list(request):
    crop_filter = request.GET.get('crop')
    prices = MarketPrice.objects.all()
    
    if crop_filter:
        prices = prices.filter(crop_id=crop_filter)
    
    prices = prices.order_by('-date')[:100]
    crops = Crop.objects.all().order_by('name')
    
    import json
    price_trends = {}
    for price in prices:
        crop_name = price.crop.name
        if crop_name not in price_trends:
            price_trends[crop_name] = {
                'labels': [],
                'prices': [],
                'latest_price': price.price_per_kg,
                'unit': price.unit
            }
        price_trends[crop_name]['labels'].append(price.date.strftime('%Y-%m-%d'))
        price_trends[crop_name]['prices'].append(float(price.price_per_kg))
    
    # Reverse the order so charts show chronological order (oldest to newest)
    # Convert to JSON for template
    for crop_name in price_trends:
        price_trends[crop_name]['labels'].reverse()
        price_trends[crop_name]['prices'].reverse()
        price_trends[crop_name]['labels'] = json.dumps(price_trends[crop_name]['labels'])
        price_trends[crop_name]['prices'] = json.dumps(price_trends[crop_name]['prices'])
    
    context = {
        'prices': prices,
        'crops': crops,
        'selected_crop': int(crop_filter) if crop_filter else None,
        'price_trends': price_trends,
    }
    return render(request, 'market/market_price_list.html', context)

