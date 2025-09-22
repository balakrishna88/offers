from datetime import datetime, timedelta
from django.shortcuts import render

from products.models import TrendingProduct




CATEGORY_MAP = {
    "men": [
        "men blazers", "men boots", "men cargos", "men casual shirts", "men casual shoes",
        "men casual trousers", "men dhoti", "men ethnic sets", "men fabrics", "men flip flops",
        "men formal shirts", "men formal shoes", "men formal trousers", "men jackets", "men jeans",
        "men kurta", "men loafers", "men lungi", "men pyjama", "men raincoats",
        "men running shoes", "men sandals floaters", "men sherwanis", "men shorts",
        "men sneakers", "men sports shoes", "men sweaters", "men sweatshirts",
        "men t shirts", "men three fourths", "men ties socks caps", "men track pants", "men tracksuits",
        "backpacks for men", "belts for man", "wallets for man", "sunglasses for men stylish"
    ],
    "women": [
        "women boots", "women bras", "women camisoles", "women capris", "women casual shoes",
        "kurta set women", "palazzos women", "party dresses women", "women dress material",
        "women dresses", "women ethnic bottoms", "women ethnic trousers", "women flats",
        "women handbags", "women heels", "women jeans", "women jeggings", "women jewellery",
        "women kurtis", "women lingerie sets", "women night dress", "women panties",
        "women sandals", "women sarees", "women shapewear", "women shoes", "women shorts",
        "women skirts", "women spectacle frames", "women sports shoes", "women sportswear",
        "women sunglasses", "women swimwear", "women topwear", "women totes", "women wallets belts",
        "women wedges", "women western wear", "women winter wear", "dupattas", "saree shapewear"
    ],
    "kids": [
        "boys jackets", "boys footwear", "boys sport shoes", "boys sweatshirts", "boys winter wear",
        "boys_clothing_ethnic", "boys_clothing_shirts", "boys_clothing_shorts", "boys_clothing_tshirts",
        "boys_innerwear", "girls dresses", "girls ethnic wear", "girls flats bellies", "girls footwear",
        "girls innerwear", "girls jackets", "girls sport shoes", "girls sweatshirts", "girls t shirts",
        "girls winter wear", "kids sandals", "infant footwear", "infant winter wear", "baby boys combo",
        "baby boys innerwear", "baby boys t shirts", "baby girls combo", "baby girls dress", "baby girls innerwear",
        "baby gear", "baby gift set combo"
    ],
    "electronics": [
        "smartphones", "smart watches", "smart bands", "smart headphones", "smart glasses (vr)",
        "tws", "tws earphones", "tws under 2000", "tws under 3000", "neckband earphones",
        "wired headphone", "headphones headsets", "camera bags", "camera flash lighting",
        "camera gimbals", "camera lenses", "camera memory cards", "camera tripods",
        "dslr cameras", "mirrorless cameras", "point and shoot cameras", "gopro cameras",
        "gopro accessories", "gopro batteries", "smart security cameras", "smart door locks online at best prices in india | 19",
        "sound bar", "tv", "tv units", "gaming consoles", "gaming accessories", "memory cards",
        "mobile cables", "mobile cases", "mobile chargers", "mobile holders", "vr glasses"
    ],
    "accessories": [
        "power banks", "screen guards", "jewellery", "precious jewellery", "silver jewellery",
        "clutches", "shoulder bags", "sling bags", "bags", "ties", "socks", "caps", "belts for man", "wallets for man",
        "women wallets belts"
    ],
    "kitchen": [
        "microwave oven", "mixer grinder 500-5000", "mixer grinder 5000-above", "otg oven",
        "hand blender", "coffee maker", "pop up toaster", "electric cooker", "electric kettle above 1000",
        "electric kettle under 1000", "food processor", "sandwich maker", "water purifier 1000-10000",
        "water purifier above 10000", "water geyser above 5000", "water geyser under 5000",
        "kitchen chimney above 10000", "kitchen chimney under 10000", "dining table set",
        "dishwasher machine", "voltage stabilizer"
    ],
    "appliances": [
        "air conditioners", "air cooler", "refrigerator", "washing machine fully automatic front load",
        "washing machine fully automatic top load", "washing machine fully semi automatic", "wet grinder",
        "inverter", "iron", "immersion rod", "ceiling fan 2500-5000", "ceiling fan above 5000", "ceiling fan under 2500"
    ],
    "books": [
        "academic books", "entrance exams", "e-learning books", "indian language books", "literature fiction books",
        "non fiction books", "self help books", "book preorders", "young readers books"
    ],
    "automobile": [
        "car stereo system", "car usb", "car charger fast charging", "car holder", "car inflator",
        "car perfumes", "car vacuum cleaner"
    ],
    "toys": [
        "gifting combos", "character shoes", "bean bags", "nuts dry fruits"  # you can add more
    ],
    "baby": [
        "baby bath hair skin care", "baby bathing accessories", "baby bedding", "baby boys combo",
        "baby boys innerwear", "baby boys t shirts", "baby cleaners detergents", "baby diapers",
        "baby feeding bottle accessories", "baby feeding utensils accessories", "baby food",
        "baby gear", "baby gift set combo", "baby girls combo", "baby girls dress",
        "baby girls innerwear", "baby grooming", "baby medical health care", "baby oral care",
        "baby proofing safety", "baby wipes", "diaper potty training", "nursing breast feeding"
    ]
}

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(request, queryset, per_page=50):
    """
    Paginate any list or queryset.

    Args:
        request: Django request object
        queryset: List or QuerySet to paginate
        per_page: Items per page (default 50)

    Returns:
        page_obj: Paginator page object
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


from django.shortcuts import render


def index(request):
    # Fetch latest 100 products (already with price drop), ordered by updated_at
    recent_trending = TrendingProduct.objects.all().order_by('-updated_at')[:100]

    # Apply pagination: 20 products per page
    page_obj = paginate_queryset(request, recent_trending, per_page=20)

    context = {
        "products": page_obj,
        "section_title": "Top Price Drop Products"
    }

    return render(request, "index.html", context)




from datetime import datetime, timedelta
from django.shortcuts import render

from django.shortcuts import render


def category_view(request):
    main_category = request.GET.get("category", "electronics").lower()
    section_title = f"Top {main_category.title()} Products"

    # Get subcategories for main category
    subcategories = CATEGORY_MAP.get(main_category, [main_category])

    # Fetch latest 100 products for this category/subcategories
    recent_products = TrendingProduct.objects.filter(
        category__in=subcategories
    ).order_by("-updated_at")[:100]  # latest 100

    # Apply pagination: 20 per page
    page_obj = paginate_queryset(request, recent_products, per_page=20)

    context = {
        "products": page_obj,
        "section_title": section_title,
        "subcategories": subcategories,
        "main_category": main_category,
    }

    return render(request, "category.html", context)


from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django.shortcuts import render
from django.http import JsonResponse

AFFILIATE_TAG = "telanganahy0a-21"
AFFILIATE_ID = "jbalakris"

def convert_to_affiliate_url(url: str) -> str:
    """Amazon URL conversion"""
    try:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs["tag"] = [AFFILIATE_TAG]
        new_query = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
    except Exception:
        return url

def convert_flipkart_affiliate_url(url: str) -> str:
    """Flipkart URL conversion"""
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        allowed_keys = {"pid", "lid", "marketplace", "store", "srno", "iid", "ppt", "ppn", "ssid"}
        filtered_params = {k: v for k, v in query_params.items() if k in allowed_keys}
        filtered_params["affid"] = [AFFILIATE_ID]
        new_query = urlencode(filtered_params, doseq=True)
        new_netloc = "dl.flipkart.com"
        new_path = "/dl" + parsed.path
        return urlunparse(parsed._replace(scheme="http", netloc=new_netloc, path=new_path, query=new_query))
    except Exception:
        return url

def affiliate_converter(request):
    result_url = ""
    if request.method == "POST":
        original_url = request.POST.get("url", "").strip()
        if "flipkart.com" in original_url:
            result_url = convert_flipkart_affiliate_url(original_url)
        elif "amazon." in original_url:
            result_url = convert_to_affiliate_url(original_url)
        else:
            result_url = original_url

    return render(request, "affiliate_converter.html", {"result_url": result_url})
