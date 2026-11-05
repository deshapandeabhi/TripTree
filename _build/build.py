#!/usr/bin/env python3
"""Generates the TripTree site pages with one shared header / menu / footer.
Usage: python3 build.py "/path/to/TripTree Web"
"""
import os, sys, html, json

ROOT = sys.argv[1]
SITE = "https://triptree.co.in"          # production domain (used for canonical / og / sitemap)
BRAND = "TripTree Resorts & Homestays"
PHONE_TEL = "+919900005639"
PHONE_TXT = "+91 99000 05639"
EMAIL = "booking@triptree.co.in"
ADDRESS_HTML = "#2223, 3rd Floor, 12th Main,<br>3rd Block East, Jayanagar,<br>Bengaluru - 560011"
ADDRESS_TXT = "#2223, 3rd Floor, 12th Main, 3rd Block East, Jayanagar, Bengaluru 560011"
OFFICE_MAP = "https://maps.google.com/maps?q=3rd+Block+East,+Jayanagar,+Bengaluru+560011&z=15&output=embed"
YEAR = "2026"
IMG = "assets/images/triptree/"

def esc(s): return html.escape(s, quote=True)

def map_iframe(src, title, height=450):
    return (f'<iframe src="{src}" title="{esc(title)}" width="600" height="{height}" '
            f'style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')

# ---------------------------------------------------------------- properties
PROPS = [
    dict(slug="bandipur-farmhouse", name="Bandipur Farmhouse", place="Bandipur, Karnataka",
         banner="banner-bandipur.jpg", card="cottages-thatched.jpg",
         map="Bandipur+National+Park,+Karnataka",
         tagline="A Farm Stay Near Bandipur",
         prices=["Room (2 guests): Rs. 3,500 / night", "Large room (6 to 8 guests): Rs. 12,000 / night"],
         card_price="From Rs. 3,500 / night",
         short="Thatched cottages on open, tree-shaded grounds close to Bandipur Tiger Reserve.",
         text="Bandipur Farmhouse is a relaxed countryside stay close to Bandipur National Park, one of India's best-known tiger reserves. Cottages are spread across open, tree-shaded grounds where spotted deer often graze at dusk, making it an easy base for safaris and slow days in nature.",
         text2="Don't be surprised by an unexpected visit from the jungle's residents right at your doorstep.",
         photos=[("cottages-thatched.jpg", "Thatched cottages on the lawn"), ("sunrise-meadow.jpg", "Sunrise over the meadow"),
                 ("spotted-deer.jpg", "Spotted deer grazing near the property"), ("gaur.jpg", "A gaur in the forest"),
                 ("garden-seating.jpg", "Outdoor seating in the garden")],
         safari=True),
    dict(slug="harangi-backwaters", name="Harangi Backwaters", place="Harangi, Coorg, Karnataka",
         banner="banner-harangi.jpg", card="sunrise-meadow.jpg",
         map="Harangi+Reservoir,+Kodagu,+Karnataka",
         tagline="A Quiet Retreat by the Water",
         prices=["Room (2 guests): Rs. 3,500 / night", "Large room (6 to 8 guests): Rs. 12,000 / night"],
         card_price="From Rs. 3,500 / night",
         short="A peaceful getaway near the Harangi reservoir in the hills of Coorg.",
         text="Harangi Backwaters is a peaceful retreat near the Harangi reservoir in Coorg, surrounded by open countryside, water and greenery. It's an ideal getaway for families and groups looking for fresh air, quiet mornings and easy access to the sights of Coorg.",
         text2="Wake up early to catch the sunrise over the water.",
         photos=[("sunrise-meadow.jpg", "Sunrise over the water and meadow"), ("cottages-thatched.jpg", "Thatched cottages on the lawn"),
                 ("garden-seating.jpg", "Outdoor seating in the garden"), ("spotted-deer.jpg", "Spotted deer grazing at sunset"),
                 ("estate-building.jpg", "The main building and garden")],
         safari=False),
    dict(slug="masinagudi-estate", name="Masinagudi Estate", place="Masinagudi, Nilgiris, Tamil Nadu",
         banner="banner-masinagudi.jpg", card="estate-building.jpg",
         map="Masinagudi,+Tamil+Nadu",
         tagline="On the Edge of the Mudumalai Forest",
         prices=["Room: Rs. 4,500 / night", "Food: Rs. 2,800 / person / night"],
         card_price="Rs. 4,500 / night",
         short="An estate stay in the Nilgiri foothills, next to Mudumalai Tiger Reserve.",
         text="Masinagudi Estate sits in the foothills of the Nilgiris, on the edge of the Mudumalai Tiger Reserve. With the forest all around and wildlife never far away, it's a wonderful base for safaris, birdwatching and unhurried evenings outdoors.",
         text2="Don't be surprised by an unexpected visit from the jungle's residents right at your doorstep.",
         photos=[("estate-building.jpg", "The estate building and garden"), ("cottages-thatched.jpg", "Thatched cottages on the lawn"),
                 ("gaur.jpg", "A gaur in the forest"), ("spotted-deer.jpg", "Spotted deer grazing"),
                 ("sunrise-meadow.jpg", "Sunrise over the meadow")],
         safari=True),
    dict(slug="mudumalai-estate", name="Mudumalai Estate", place="Mudumalai, Nilgiris, Tamil Nadu",
         banner="mudumalai-cottages.jpg", card="mudumalai-cottages.jpg",
         map="Mudumalai+National+Park,+Tamil+Nadu",
         tagline="Deluxe Cottages in the Forest",
         prices=["Deluxe Cottage: Rs. 2,500 / person / night"],
         card_price="Rs. 2,500 / person / night",
         short="Deluxe cottages in the forest, owned and managed by local families.",
         text="Mudumalai Estate offers a unique and authentic experience of local culture, as the property is owned and managed by local families. With a range of amenities and services, the estate provides a comfortable stay for travellers looking to immerse themselves in the beauty and tranquillity of the region.",
         text2="Don't be surprised by an unexpected visit from the jungle's residents right at your doorstep.",
         photos=[("mudumalai-cottages.jpg", "Cottages among the trees"), ("mudumalai-cottage-night.jpg", "A cottage lit up at night"),
                 ("mudumalai-terrace.jpg", "Dining terrace overlooking the forest"), ("mudumalai-cottage.jpg", "Cottage entrance and verandah"),
                 ("mudumalai-room.jpg", "Deluxe cottage bedroom")],
         safari=True),
]

NAV = [("index.html", "Home"), ("about.html", "About Us"), ("properties.html", "Our Properties"),
       ("gallery.html", "Gallery"), ("contact.html", "Contact")]

def nav_html(active):
    out = ['<ul class="navigation">']
    for href, label in NAV:
        cur = ' current' if href == active or (href == "properties.html" and active.startswith("prop:")) else ''
        if href == "properties.html":
            out.append(f'<li class="dropdown{cur}"><a href="{href}">{label}</a><ul>')
            out.append(f'<li><a href="properties.html">All Properties</a></li>')
            for p in PROPS:
                out.append(f'<li><a href="{p["slug"]}.html">{p["name"]}</a></li>')
            out.append('</ul></li>')
        else:
            cls = f' class="{cur.strip()}"' if cur else ''
            out.append(f'<li{cls}><a href="{href}">{label}</a></li>')
    out.append('</ul>')
    return "\n".join(out)

# ---------------------------------------------------------------- layout
def head(title, desc, fname, og_image="cottages-thatched.jpg", extra=""):
    canon = SITE + "/" + ("" if fname == "index.html" else fname)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/{IMG}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<!-- Stylesheets -->
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/style.css" rel="stylesheet">
<link href="assets/css/responsive.css" rel="stylesheet">
<link href="assets/css/color.css" rel="stylesheet">
<link href="assets/css/site.css" rel="stylesheet">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&amp;family=Roboto:wght@400;700&amp;family=Poppins:wght@400;500;700&amp;display=swap" rel="stylesheet">
<link rel="icon" href="assets/images/favicon.png" type="image/png">
{extra}</head>
'''

def header(active, home=False):
    style = "header-style-five" if home else "header-style-one"
    logo = "logo-light.svg" if home else "logo-dark.svg"
    bar = "icon-bar4.png" if home else "icon-bar.png"
    nav = nav_html(active)
    phone = (f'<div class="header-phone-number"><a href="tel:{PHONE_TEL}"><i class="flaticon-smartphone"></i> {PHONE_TXT}</a></div>'
             if home else '')
    right = f'''<div class="right-column">
                        <div class="navbar-right">
                            {phone}
                            <div class="link-btn"><a href="booking.html" class="theme-btn btn-style-one{' btn-md' if home else ''}">Book Now</a></div>
                        </div>
                    </div>'''
    return f'''<body class="dark_bg">
<div class="page-wrapper">
    <!-- Main Header -->
    <header class="main-header {style}">
        <div class="header-upper">
            <div class="auto-container">
                <div class="inner-container">
                    <div class="logo-box">
                        <div class="logo"><a href="index.html"><img src="assets/images/{logo}" width="170" alt="{esc(BRAND)}"></a></div>
                    </div>
                    <div class="nav-outer">
                        <div class="mobile-nav-toggler"><img src="assets/images/icons/{bar}" alt="Open menu"></div>
                        <nav class="main-menu navbar-expand-md navbar-light">
                            <div class="collapse navbar-collapse show clearfix" id="navbarSupportedContent">
{nav}
                            </div>
                        </nav>
                    </div>
                    {right}
                </div>
            </div>
        </div>
        <!-- Sticky Header -->
        <div class="sticky-header">
            <div class="header-upper">
                <div class="auto-container">
                    <div class="inner-container">
                        <div class="logo-box">
                            <div class="logo"><a href="index.html"><img src="assets/images/{logo}" width="150" alt="{esc(BRAND)}"></a></div>
                        </div>
                        <div class="nav-outer">
                            <div class="mobile-nav-toggler"><img src="assets/images/icons/{bar}" alt="Open menu"></div>
                            <nav class="main-menu navbar-expand-md navbar-light"></nav>
                        </div>
                        {right}
                    </div>
                </div>
            </div>
        </div>
        <!-- Mobile Menu -->
        <div class="mobile-menu">
            <div class="menu-backdrop"></div>
            <div class="close-btn"><i class="icon far fa-times"></i></div>
            <nav class="menu-box">
                <div class="nav-logo"><a href="index.html"><img src="assets/images/logo-light-2.svg" alt="{esc(BRAND)}"></a></div>
                <div class="menu-outer"></div>
                <div class="mobile-contact">
                    <a href="tel:{PHONE_TEL}"><i class="fas fa-phone"></i> {PHONE_TXT}</a>
                    <a href="mailto:{EMAIL}"><i class="fas fa-envelope"></i> {EMAIL}</a>
                </div>
            </nav>
        </div>
        <div class="nav-overlay">
            <div class="cursor"></div>
            <div class="cursor-follower"></div>
        </div>
    </header>
    <!-- End Main Header -->
'''

FOOTER_PICS = [("cottages-thatched", "Thatched cottages"), ("spotted-deer", "Spotted deer"), ("mudumalai-cottages", "Mudumalai cottages"),
               ("gaur", "Gaur in the forest"), ("estate-building", "Estate building"), ("mudumalai-terrace", "Dining terrace")]

def footer(scripts_extra=""):
    gal = "".join(f'''
                    <div class="col-lg-2 col-md-4 col-6">
                        <div class="image gallery-overlay">
                            <div class="inner-box">
                                <img src="{IMG}{n}-sq.jpg" alt="{esc(a)}" loading="lazy" width="400" height="400">
                                <div class="overlay-box"><div class="overlay-inner"><div class="content">
                                    <a href="{IMG}{n}.jpg" class="lightbox-image link" data-fancybox="footer-gallery" data-caption="{esc(a)}" aria-label="View photo: {esc(a)}"><span class="icon fas fa-eye"></span></a>
                                </div></div></div>
                            </div>
                        </div>
                    </div>''' for n, a in FOOTER_PICS)
    props = "\n".join(f'<li><a href="{p["slug"]}.html">{p["name"]}</a></li>' for p in PROPS)
    return f'''
    <!-- Footer -->
    <footer class="main-footer">
        <div class="auto-container">
            <div class="footer-gallery">
                <div class="row">{gal}
                </div>
            </div>
            <div class="widgets-section">
                <div class="row clearfix">
                    <div class="column col-lg-4 col-md-12">
                        <div class="widget contact-widget">
                            <div class="image"><a href="index.html"><img src="assets/images/logo-light.svg" width="240" alt="{esc(BRAND)}"></a></div>
                            <table>
                                <tr><td class="lebel">Tel :</td><td><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></td></tr>
                                <tr><td class="lebel">Email :</td><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
                                <tr><td class="lebel">Office :</td><td>{ADDRESS_HTML}</td></tr>
                            </table>
                        </div>
                    </div>
                    <div class="column col-lg-4 col-md-6">
                        <div class="widget links-widget">
                            <h3 class="widget-title">Quick Links</h3>
                            <div class="widget-content">
                                <ul>
                                    <li><a href="about.html">About Us</a></li>
                                    <li><a href="properties.html">Our Properties</a></li>
                                    <li><a href="gallery.html">Gallery</a></li>
                                    <li><a href="booking.html">Book Your Stay</a></li>
                                    <li><a href="contact.html">Contact Us</a></li>
                                    <li><a href="terms-conditions.html">Terms &amp; Conditions</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="column col-lg-4 col-md-6">
                        <div class="widget links-widget">
                            <h3 class="widget-title">Our Properties</h3>
                            <div class="widget-content">
                                <ul>
{props}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="auto-container">
            <div class="boder-bottom-four"></div>
        </div>
        <div class="footer-bottom">
            <div class="auto-container">
                <div class="wrapper-box">
                    <div class="copyright text-center">
                        <div class="text">&copy; {YEAR} {esc(BRAND)}. All rights reserved.</div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</div>
<!--End pagewrapper-->

<div class="scroll-to-top scroll-to-target" data-target="html" aria-label="Back to top"><span class="fas fa-arrow-up"></span></div>

<script src="assets/js/jquery.js"></script>
<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/jquery.fancybox.js"></script>
<script src="assets/js/isotope.js"></script>
<script src="assets/js/owl.js"></script>
<script src="assets/js/appear.js"></script>
<script src="assets/js/wow.js"></script>
<script src="assets/js/scrollbar.js"></script>
<script src="assets/js/TweenMax.min.js"></script>
<script src="assets/js/swiper.min.js"></script>
<script src="assets/js/parallax-scroll.js"></script>
<script src="assets/js/jquery-ui-1.9.2.custom.min.js"></script>
<script src="assets/js/jquery.nice-select.min.js"></script>
<script src="assets/js/script.js"></script>
{scripts_extra}</body>
</html>
'''

def page_title(h1, bg):
    return f'''
    <!-- Page Title -->
    <section class="page-title" style="background-image: url({bg});">
        <div class="auto-container">
            <div class="text-center">
                <h1>{h1}</h1>
            </div>
        </div>
    </section>
'''

def write(fname, content):
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", fname)

FORMS_JS = '<script src="assets/js/forms.js"></script>\n'

def prop_card(p, col="col-lg-6"):
    return f'''
                <div class="{col} room-block-two">
                    <div class="image"><a href="{p["slug"]}.html"><img src="{IMG}{p["card"]}" alt="{esc(p["name"])}" loading="lazy"></a>
                        <div class="text">{p["card_price"]}</div>
                    </div>
                    <h3><a href="{p["slug"]}.html">{p["name"]}</a></h3>
                    <div class="icon-list">
                        <ul>
                            <li><i class="fas fa-map-marker-alt"></i>{p["place"]}</li>
                        </ul>
                    </div>
                    <div class="text-two">{p["short"]}</div>
                    <div class="link-btn"><a href="{p["slug"]}.html" class="theme-btn btn-style-one btn-md"><span>View Details</span></a></div>
                </div>'''

# ================================================================ HOME
def build_home():
    ld = {
        "@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": SITE + "/",
        "logo": SITE + "/assets/images/logo-dark.png", "email": EMAIL, "telephone": PHONE_TEL,
        "address": {"@type": "PostalAddress", "streetAddress": "#2223, 3rd Floor, 12th Main, 3rd Block East, Jayanagar",
                    "addressLocality": "Bengaluru", "postalCode": "560011", "addressRegion": "Karnataka", "addressCountry": "IN"},
    }
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    acc = "".join(f'''
                <div class="accomodation-block">
                    <div class="image"><a href="{p["slug"]}.html"><img src="{IMG}{p["card"]}" alt="{esc(p["name"])}"></a></div>
                    <div class="content">
                        <div class="row">
                            <div class="col-md-5">
                                <div class="price">{p["card_price"]}</div>
                                <h3><a href="{p["slug"]}.html">{p["name"]}</a></h3>
                            </div>
                            <div class="col-md-7">
                                <div class="info-list">
                                    <ul>
                                        <li><i class="fas fa-map-marker-alt"></i>{p["place"]}</li>
                                    </ul>
                                </div>
                                <div class="text">{p["short"]} <a href="{p["slug"]}.html" class="inline-link">View details &rarr;</a></div>
                            </div>
                        </div>
                    </div>
                </div>''' for p in PROPS)
    exp = [("fa-binoculars", "Jungle Safari", "Forest Department safaris into Bandipur and Mudumalai, arranged at an extra charge."),
           ("fa-paw", "Wildlife Spotting", "Spotted deer, gaur and a wide variety of birds are regular visitors."),
           ("fa-hiking", "Trekking", "Explore the surrounding countryside on foot with guided walks and treks."),
           ("fa-fire", "Night Bonfire", "End the day around a bonfire under a sky full of stars."),
           ("fa-om", "Meditation &amp; Fitness", "Quiet spaces to unwind, with gym and fitness coaching available on demand."),
           ("fa-mountain", "Sightseeing", "Discover viewpoints and local attractions close to each property.")]
    expb = "".join(f'''
                        <div class="col-md-6 amenities-block">
                            <div class="inner-box">
                                <div class="icon"><i class="fas {i}"></i></div>
                                <h3>{t}</h3>
                                <div class="text">{d}</div>
                            </div>
                        </div>''' for i, t, d in exp)
    body = f'''
    <!-- Banner -->
    <section class="banner-section-three style-two">
        <div class="wrapper-box" style="background-image: url({IMG}cottages-thatched.jpg);">
            <div class="auto-container">
                <div class="content-box">
                    <div class="inner">
                        <h1 class="banner-title">TripTree Resorts <br>&amp; Homestays</h1>
                        <div class="text">Jungle cottages, farmhouses and estates near Bandipur, <br>Mudumalai, Masinagudi and Harangi.</div>
                        <div class="link-btn"><a href="properties.html" class="theme-btn btn-style-one"><span>Explore Our Properties</span></a></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Welcome -->
    <section class="welcome-section-seven">
        <div class="auto-container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="title-box">
                        <div class="sub-title">welcome to TripTree</div>
                        <h2 class="sec-title text-light">Stay Close to the Wild</h2>
                        <div class="text">TripTree brings together nature stays on the edges of South India's best-known forests, Bandipur, Mudumalai and Masinagudi, along with a quiet retreat near the Harangi backwaters in Coorg. Our properties are small and personal, offering warm, home-style hospitality and plenty of space to slow down.<br><br>Spend your days on a jungle safari, walking through the countryside or watching deer graze at sunset, and your evenings around a bonfire.</div>
                        <div class="link-btn"><a href="about.html" class="read-more-btn">Discover More</a></div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="content-block">
                        <div class="inner-box">
                            <div class="icon"><i class="flaticon-resort"></i></div>
                            <h3>Four Nature <br> Stays</h3>
                            <div class="text-two">Bandipur &middot; Mudumalai <br> Masinagudi &middot; Harangi</div>
                            <div class="link-btn"><a href="booking.html" class="theme-btn btn-style-two">Book Now</a></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Wildlife -->
    <section class="we-invite-section border-shape-top mx-60">
        <div class="bg-image" style="background-image: url(assets/images/background/bg-1.jpg);"></div>
        <div class="auto-container">
            <div class="row">
                <div class="col-lg-6">
                    <div class="image-block">
                        <div class="image"><img src="{IMG}spotted-deer.jpg" alt="Spotted deer grazing near our property"></div>
                        <div class="image-two"><img src="{IMG}gaur-sq.jpg" alt="A gaur in the forest"></div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="contact-block">
                        <div class="sub-title">enjoy the unique experience</div>
                        <h2 class="sec-title">We Invite You To <br> Celebrate Wildlife</h2>
                        <div class="text">Our Bandipur, Masinagudi and Mudumalai properties sit close to some of the richest wildlife habitats in the Nilgiri Biosphere Reserve. Herds of spotted deer, gaur and a wide variety of birds are regular visitors, and an unexpected encounter at your doorstep is all part of the experience.</div>
                        <div class="text-two">Jungle safaris are run by the Forest Department at an additional charge, payable on arrival. We're happy to help you plan yours.</div>
                        <div class="link-btn"><a href="about.html" class="theme-btn btn-style-one"><span>Read More <i class="flaticon-right-arrow"></i></span></a></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experiences -->
    <section class="amenities-section-two light-bg mx-60 border-shape-bottom">
        <div class="auto-container">
            <div class="row">
                <div class="col-lg-4">
                    <div class="title-box">
                        <div class="sub-title">experiences</div>
                        <h2 class="sec-title">Things To Do <br> On Your Stay</h2>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="row">{expb}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Properties -->
    <section class="accomodation-section">
        <div class="auto-container">
            <div class="title-box text-center">
                <div class="sub-title">accommodation</div>
                <h2 class="sec-title text-light">Our Properties</h2>
            </div>
            <div class="theme_carousel owl-theme owl-carousel" data-options='{{"loop": true, "center": false, "margin": 30, "autoheight":true, "lazyload":true, "nav": true, "dots": true, "autoplay": true, "autoplayTimeout": 6000, "smartSpeed": 1000, "responsive":{{ "0" :{{ "items": "1" }}, "1200":{{ "items" : "1" }}}}}}'>{acc}
            </div>
            <div class="text-center mt-5"><a href="properties.html" class="theme-btn btn-style-one"><span>View All Properties</span></a></div>
        </div>
    </section>

    <!-- Location & contact -->
    <section class="news-section-two light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="row">
                <div class="col-lg-6">
                    <div class="title-box">
                        <div class="sub-title">reach us</div>
                        <h2 class="sec-title">Our Office</h2>
                    </div>
                    <div class="contact-map">
                        {map_iframe(OFFICE_MAP, "Map of the TripTree office in Jayanagar, Bengaluru")}
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="title-box">
                        <div class="sub-title">plan your stay</div>
                        <h2 class="sec-title">Get In Touch</h2>
                    </div>
                    <div class="home-contact">
                        <p>Tell us your dates and the property you'd like to visit, and we'll confirm availability and pricing for you.</p>
                        <ul class="home-contact-list">
                            <li><i class="fas fa-phone"></i><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></li>
                            <li><i class="fas fa-envelope"></i><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                            <li><i class="fas fa-map-marker-alt"></i><span>{ADDRESS_TXT}</span></li>
                        </ul>
                        <div class="btn-row">
                            <a href="booking.html" class="theme-btn btn-style-one"><span>Send a Booking Enquiry</span></a>
                            <a href="tel:{PHONE_TEL}" class="theme-btn btn-style-one dark-btn"><span>Call Us</span></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
'''
    write("index.html",
          head(f"{BRAND} | Jungle Stays in Bandipur, Mudumalai, Masinagudi & Coorg",
               "Nature stays and jungle cottages near Bandipur, Mudumalai, Masinagudi and Harangi (Coorg). Book farmhouse and estate stays with TripTree Resorts & Homestays.",
               "index.html", extra=extra)
          + header("index.html", home=True) + body + footer())

# ================================================================ ABOUT
def build_about():
    feats = ["Spa / gym", "Meditation", "Shopping", "Trekking", "Sightseeing", "Elephant safari",
             "Facials / makeup", "Live music band", "Night bonfire"]
    lis = "\n".join(f'<li><i class="flaticon-checkmark"></i>{f}</li>' for f in feats)
    cards = "".join(prop_card(p) for p in PROPS)
    body = page_title("About TripTree", IMG + "banner-lake.jpg") + f'''
    <!-- Welcome -->
    <section class="welcome-section-six light-bg mx-60 border-shape-top">
        <div class="auto-container">
            <div class="row">
                <div class="col-lg-6">
                    <div class="title-box">
                        <div class="sub-title">welcome to TripTree</div>
                        <h2 class="sec-title small mb-30">Nature Stays, <br>Thoughtfully Hosted</h2>
                        <div class="text">Holidays close to nature, made simple.</div>
                        <div class="text-two">TripTree Resorts &amp; Homestays is a Bengaluru-based collection of nature stays near some of South India's most loved wildlife destinations: Bandipur, Mudumalai and Masinagudi in the Nilgiri Biosphere Reserve, and Harangi in Coorg.</div>
                        <div class="text-three">Each property has its own character, from thatched farmhouse cottages to forest estates, but they share the same idea: comfortable rooms, honest food, warm hosts and the wild right outside your door.</div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="text-lg-end">
                        <div class="image about-portrait"><img src="{IMG}mudumalai-terrace.jpg" alt="Dining terrace at Mudumalai Estate"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Why Choose Us -->
    <section class="why-choose-us-section light-bg mx-60 pt-0 border-shape-bottom">
        <div class="auto-container">
            <div class="title-box text-center">
                <div class="sub-title">Our Features</div>
                <h2 class="sec-title mb-30">Why Choose Us</h2>
                <div class="text">Whether you're planning a family holiday, a weekend with friends or a quiet break on your own, we'll help you find the stay that suits you.</div>
            </div>
            <div class="row">
                <div class="col-lg-6 why-choose-us-block">
                    <div class="image"><img src="{IMG}spotted-deer.jpg" alt="Spotted deer at sunset"></div>
                    <div class="inner-box">
                        <div class="image-block"><img src="{IMG}gaur-sq.jpg" alt="Gaur in the forest"></div>
                        <div class="text-three"><span>4</span> Nature <br> Stays</div>
                    </div>
                </div>
                <div class="col-lg-6 why-choose-us-block">
                    <div class="text-two">At TripTree, we understand the different expectations of visitors. We feel elated when you come back for a second time!</div>
                    <div class="icon-list">
                        <ul>
{lis}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Our properties -->
    <section class="checkout-section mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="sub-title">where we are</div>
            <h2 class="sec-title">Our Properties</h2>
            <div class="row room-grid">{cards}
            </div>
            <div class="text-center about-help">Not sure which property is right for you? Call us on <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a> or <a href="contact.html">send us a message</a> and we'll help you plan your trip.</div>
        </div>
    </section>
'''
    write("about.html", head(f"About Us | {BRAND}",
          "TripTree Resorts & Homestays is a Bengaluru-based collection of nature stays near Bandipur, Mudumalai, Masinagudi and Harangi.",
          "about.html", og_image="mudumalai-terrace.jpg") + header("about.html") + body + footer())

# ================================================================ PROPERTIES LIST
def build_properties():
    cards = "".join(prop_card(p) for p in PROPS)
    body = page_title("Our Properties", IMG + "banner-bandipur.jpg") + f'''
    <section class="checkout-section light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="sub-title">choose your stay</div>
            <h2 class="sec-title">Resorts &amp; Homestays</h2>
            <div class="row room-grid">{cards}
            </div>
        </div>
    </section>
'''
    write("properties.html", head(f"Our Properties | {BRAND}",
          "Explore TripTree's nature stays: Bandipur Farmhouse, Harangi Backwaters, Masinagudi Estate and Mudumalai Estate.",
          "properties.html") + header("properties.html") + body + footer())

# ================================================================ PROPERTY PAGES
AMENITIES = [[("flaticon-air-conditioner", "Air conditioner"), ("flaticon-cable-tv", "Cable TV"), ("flaticon-pool", "Swimming pool"), ("flaticon-wifi-signal", "High speed WiFi")],
             [("flaticon-iron", "Ironing board"), ("flaticon-terrace", "Balcony or terrace"), ("flaticon-kettle", "Tea / coffee kettle"), ("flaticon-bath-1", "Bathtub")],
             [("flaticon-hair-dryer", "Hair dryer"), ("flaticon-bed", "King size bed"), ("flaticon-breakfast", "Breakfast included"), ("flaticon-bath", "Shower")]]

def build_property(p):
    slides = "".join(f'''
                        <div class="swiper-slide"><div class="image"><img src="{IMG}{f}" alt="{esc(a)}"></div></div>''' for f, a in p["photos"])
    thumbs = "".join(f'''
                        <div class="swiper-slide"><div class="thumb"><img src="{IMG}{f}" alt="" loading="lazy"></div></div>''' for f, a in p["photos"])
    amen = "".join('<div class="col-md-4"><ul class="list-one">' + "".join(f'<li><i class="{i}"></i>{t}</li>' for i, t in col) + '</ul></div>' for col in AMENITIES)
    prices = "<br>".join(p["prices"])
    safari = ('''
                    <h4>Jungle Safari</h4>
                    <div class="text">Safaris are operated by the Forest Department at an additional charge, payable on arrival. Our team can help you plan your safari.</div>
''' if p["safari"] else '')
    others = "".join(prop_card(o, "col-lg-4 col-md-6") for o in PROPS if o is not p)
    maps = f"https://maps.google.com/maps?q={p['map']}&z=11&output=embed"
    body = page_title(p["name"], IMG + p["banner"]) + f'''
    <!-- Property details -->
    <section class="room-details-section light-bg mx-60 border-shape-top">
        <div class="auto-container">
            <div class="single-items-carousel">
                <div class="swiper-container single-item-with-pager-carousel">
                    <div class="swiper-wrapper">{slides}
                    </div>
                </div>
                <div class="h_10 w_10"></div>
                <div class="swiper-container single-item-with-pager-thumb">
                    <div class="swiper-wrapper">{thumbs}
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-8">
                    <div class="room-block">
                        <div class="pricing">{prices}</div>
                        <h2 class="sec-title">{p["tagline"]}</h2>
                        <div class="property-location"><i class="fas fa-map-marker-alt"></i> {p["place"]}</div>
                        <div class="text">{p["text"]}</div>
                        <div class="text-two">{p["text2"]}</div>
                    </div>
                    <h4>Amenities</h4>
                    <div class="row">{amen}</div>
                    <h4>House Rules</h4>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="check">check in</div>
                            <div class="time">Check-in from 9:00 AM</div>
                            <div class="subject">Early check-in subject to availability</div>
                            <div class="age">Minimum check-in age: 18</div>
                        </div>
                        <div class="col-md-6">
                            <div class="check">check out</div>
                            <div class="time">Check-out before 12:00 noon</div>
                            <div class="subject">Express check-out available</div>
                        </div>
                    </div>
                    <h4>Before You Arrive</h4>
                    <div class="text">Once your booking is confirmed, our team will share directions and check-in details with you by phone or email. For any questions, contact us using the details on your booking confirmation.</div>

                    <h4>Children and Extra Beds</h4>
                    <div class="text">Children are welcome. Extra beds can be arranged on request; please ask us for current charges when you book.</div>
{safari}
                    <h4>Fitness, Medical and Health</h4>
                    <div class="text">Gym and fitness coaching are available on demand. We also keep general medicines on hand for emergencies.</div>

                    <h4>Cancellation</h4>
                    <div class="text">Cancellation and refund terms depend on your dates and booking, and are shared with you before you confirm. See our <a href="terms-conditions.html">Terms &amp; Conditions</a> or contact us for details.</div>

                    <h4>Location</h4>
                    <div class="contact-map property-map">
                        {map_iframe(maps, "Map of the " + p["name"] + " area", 380)}
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="block-six">
                        <h3>Book Your Stay</h3>
                        <ul class="list-two">
                            <li><i class="flaticon-phone-ringing"></i><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></li>
                            <li><i class="flaticon-mail"></i><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                        </ul>
                        <div class="link-btn"><a href="tel:{PHONE_TEL}" class="theme-btn btn-style-one dark-btn"><span>Call Now</span></a></div>
                        <div class="link-btn"><a href="booking.html?property={p["slug"]}" class="theme-btn btn-style-one"><span>Send Enquiry</span></a></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Other properties -->
    <section class="checkout-section mx-60 border-shape-bottom">
        <div class="auto-container">
            <div class="sub-title">explore more</div>
            <h2 class="sec-title">Other Properties</h2>
            <div class="row room-grid">{others}
            </div>
        </div>
    </section>
'''
    write(p["slug"] + ".html", head(f"{p['name']}, {p['place']} | {BRAND}",
          f"{p['name']} in {p['place']}. {p['short']} {p['card_price']}. Enquire and book with TripTree.",
          p["slug"] + ".html", og_image=p["card"]) + header("prop:" + p["slug"]) + body + footer())

# ================================================================ GALLERY
GALLERY = [("cottages-thatched", "cat-1", "Thatched cottages"), ("spotted-deer", "cat-2", "Spotted deer at sunset"),
           ("mudumalai-cottages", "cat-1", "Mudumalai Estate cottages"), ("sunrise-meadow", "cat-3", "Sunrise over the meadow"),
           ("gaur", "cat-2", "Gaur in the forest"), ("mudumalai-cottage-night", "cat-1", "Cottage at night"),
           ("estate-building", "cat-1", "Estate building and garden"), ("mudumalai-terrace", "cat-3", "Dining terrace"),
           ("garden-seating", "cat-3", "Garden seating"), ("mudumalai-cottage", "cat-1", "Cottage verandah"),
           ("mudumalai-room", "cat-1", "Deluxe cottage bedroom"), ("cottages-lawn", "cat-3", "Cottages and lawn")]

def build_gallery():
    items = "".join(f'''
                    <div class="gallery-block-four gallery-overlay masonry-item all {c} col-lg-4 col-md-6">
                        <div class="inner-box">
                            <div class="image"><img src="{IMG}{n}.jpg" alt="{esc(a)}" loading="lazy"></div>
                            <div class="overlay-box"><div class="overlay-inner"><div class="content">
                                <a href="{IMG}{n}.jpg" class="lightbox-image link" data-fancybox="gallery" data-caption="{esc(a)}" aria-label="View photo: {esc(a)}"><span class="icon fas fa-eye"></span></a>
                            </div></div></div>
                        </div>
                    </div>''' for n, c, a in GALLERY)
    body = page_title("Gallery", IMG + "banner-lake.jpg") + f'''
    <section class="gallery-section-four light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="filters">
                <ul class="filter-tabs filter-btns">
                    <li class="filter active" data-role="button" data-filter=".all">All</li>
                    <li class="filter" data-role="button" data-filter=".cat-1">Stays</li>
                    <li class="filter" data-role="button" data-filter=".cat-2">Wildlife</li>
                    <li class="filter" data-role="button" data-filter=".cat-3">Surroundings</li>
                </ul>
            </div>
            <div class="sortable-masonry">
                <div class="items-container row">{items}
                </div>
            </div>
        </div>
    </section>
'''
    write("gallery.html", head(f"Gallery | {BRAND}", "Photos of TripTree's cottages, estates and the wildlife around our properties.",
          "gallery.html", og_image="spotted-deer.jpg") + header("gallery.html") + body + footer())

# ================================================================ CONTACT
def build_contact():
    body = page_title("Contact Us", IMG + "banner-masinagudi.jpg") + f'''
    <section class="contact-form-section light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="sec-title">
                <div class="sub-title">get in touch</div>
                <h2>Send Us a Message</h2>
                <div class="text">Questions about a property, group bookings or anything else? Fill in the form and our team will get back to you. <br>To check availability for specific dates, use our <a href="booking.html">booking enquiry form</a>.</div>
            </div>
            <div class="row">
                <div class="col-lg-8">
                    <div class="contact-form style-two">
                        <form method="post" action="inc/sendemail.php" class="js-ajax-form" novalidate>
                            <input type="hidden" name="form_type" value="contact">
                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label class="visually-hidden" for="c-name">Your name</label>
                                    <input type="text" id="c-name" class="form-control" name="name" placeholder="Your Name *" required maxlength="100" autocomplete="name">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="visually-hidden" for="c-email">Your email</label>
                                    <input type="email" id="c-email" class="form-control" name="email" placeholder="Your Email *" required maxlength="150" autocomplete="email">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="visually-hidden" for="c-phone">Phone number</label>
                                    <input type="tel" id="c-phone" class="form-control" name="phone" placeholder="Phone Number *" required maxlength="20" pattern="[0-9 +\\-\\(\\)]{{7,20}}" autocomplete="tel">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="visually-hidden" for="c-subject">Subject</label>
                                    <input type="text" id="c-subject" class="form-control" name="subject" placeholder="Subject" maxlength="150">
                                </div>
                                <div class="form-group col-md-12">
                                    <label class="visually-hidden" for="c-message">Message</label>
                                    <textarea id="c-message" name="message" class="form-control" placeholder="Write your message *" required maxlength="3000"></textarea>
                                </div>
                                <div class="form-group col-md-12 hp-field" aria-hidden="true">
                                    <label for="c-website">Leave this field empty</label>
                                    <input type="text" id="c-website" name="website" tabindex="-1" autocomplete="off">
                                </div>
                                <div class="form-group col-md-12">
                                    <button class="theme-btn btn-style-one" type="submit"><span>Send Message</span></button>
                                    <div class="form-status" role="status" aria-live="polite"></div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="col-lg-4 icon_box">
                    <div class="inner-box">
                        <h4>{esc(BRAND)}</h4>
                        <div class="border-shap"></div>
                        <div class="text-two">{ADDRESS_HTML}</div>
                        <div class="text-three"><a href="mailto:{EMAIL}">{EMAIL}</a></div>
                    </div>
                    <div class="icon-box">
                        <h4>Reservations</h4>
                        <div class="icon"><h5><i class="fas fa-phone"></i><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></h5></div>
                        <div class="text-four">Check-in: from 9:00 AM <br>Check-out: before 12:00 noon</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="map-section-two mx-60">
        <div class="auto-container">
            <div class="contact-map">
                {map_iframe(OFFICE_MAP, "Map of the TripTree office in Jayanagar, Bengaluru", 500)}
            </div>
        </div>
    </section>
'''
    write("contact.html", head(f"Contact Us | {BRAND}",
          f"Contact TripTree Resorts & Homestays. Call {PHONE_TXT} or email {EMAIL}. Office in Jayanagar, Bengaluru.",
          "contact.html") + header("contact.html") + body + footer(FORMS_JS))

# ================================================================ BOOKING
def build_booking():
    opts = "\n".join(f'<option value="{p["slug"]}">{p["name"]}</option>' for p in PROPS)
    body = page_title("Book Your Stay", IMG + "banner-bandipur.jpg") + f'''
    <section class="contact-form-section light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="sec-title">
                <div class="sub-title">booking enquiry</div>
                <h2>Check Availability</h2>
                <div class="text">Send us your dates and preferred property. We'll confirm availability, pricing and payment details with you by phone or email. <br>Prefer to talk? Call us on <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a>.</div>
            </div>
            <div class="row">
                <div class="col-lg-8">
                    <div class="contact-form style-two">
                        <form method="post" action="inc/sendemail.php" class="js-ajax-form booking-form" novalidate>
                            <input type="hidden" name="form_type" value="booking">
                            <div class="row">
                                <div class="form-group col-md-12">
                                    <label class="field-label" for="b-property">Property *</label>
                                    <select id="b-property" name="property" class="form-control" required>
                                        <option value="">Select a property</option>
{opts}
                                        <option value="not-sure">Not sure yet - please advise</option>
                                    </select>
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="field-label" for="b-checkin">Check-in date *</label>
                                    <input type="date" id="b-checkin" class="form-control" name="checkin" required>
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="field-label" for="b-checkout">Check-out date *</label>
                                    <input type="date" id="b-checkout" class="form-control" name="checkout" required>
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="field-label" for="b-adults">Adults *</label>
                                    <input type="number" id="b-adults" class="form-control" name="adults" min="1" max="50" value="2" required>
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="field-label" for="b-children">Children</label>
                                    <input type="number" id="b-children" class="form-control" name="children" min="0" max="50" value="0">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="field-label" for="b-name">Your name *</label>
                                    <input type="text" id="b-name" class="form-control" name="name" required maxlength="100" autocomplete="name">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="field-label" for="b-phone">Phone number *</label>
                                    <input type="tel" id="b-phone" class="form-control" name="phone" required maxlength="20" pattern="[0-9 +\\-\\(\\)]{{7,20}}" autocomplete="tel">
                                </div>
                                <div class="form-group col-md-12">
                                    <label class="field-label" for="b-email">Email *</label>
                                    <input type="email" id="b-email" class="form-control" name="email" required maxlength="150" autocomplete="email">
                                </div>
                                <div class="form-group col-md-12">
                                    <label class="field-label" for="b-message">Special requests</label>
                                    <textarea id="b-message" name="message" class="form-control" maxlength="3000" placeholder="Room preference, food requirements, safari plans..."></textarea>
                                </div>
                                <div class="form-group col-md-12 hp-field" aria-hidden="true">
                                    <label for="b-website">Leave this field empty</label>
                                    <input type="text" id="b-website" name="website" tabindex="-1" autocomplete="off">
                                </div>
                                <div class="form-group col-md-12">
                                    <button class="theme-btn btn-style-one" type="submit"><span>Send Booking Enquiry</span></button>
                                    <div class="form-status" role="status" aria-live="polite"></div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="col-lg-4 icon_box">
                    <div class="inner-box">
                        <h4>Good to know</h4>
                        <div class="border-shap"></div>
                        <div class="text-two">Check-in from 9:00 AM<br>Check-out before 12:00 noon<br>Minimum check-in age: 18</div>
                        <div class="text-three"><a href="terms-conditions.html">Read our Terms &amp; Conditions</a></div>
                    </div>
                    <div class="icon-box">
                        <h4>Call Reservations</h4>
                        <div class="icon"><h5><i class="fas fa-phone"></i><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></h5></div>
                        <div class="text-four"><a href="mailto:{EMAIL}">{EMAIL}</a></div>
                    </div>
                </div>
            </div>
        </div>
    </section>
'''
    write("booking.html", head(f"Book Your Stay | {BRAND}",
          "Send a booking enquiry for Bandipur Farmhouse, Harangi Backwaters, Masinagudi Estate or Mudumalai Estate.",
          "booking.html") + header("booking.html") + body + footer(FORMS_JS))

# ================================================================ TERMS
TERMS = [
    ("Bookings and confirmation", "A booking is confirmed only once you receive a confirmation from TripTree by phone, email or message, along with any advance payment requested. Rates shown on this website are indicative and may vary by season, occupancy and availability; the rate stated in your confirmation applies."),
    ("Payments", "Payment details, including any advance required, are shared with your booking confirmation. Charges for extras such as additional meals, extra beds and activities are payable at the property unless agreed otherwise."),
    ("Cancellations and refunds", "Cancellation and refund terms depend on the property, season and booking, and are communicated to you before you confirm. Please contact us as early as possible if you need to change or cancel your booking."),
    ("Check-in and check-out", "Check-in is from 9:00 AM and check-out is before 12:00 noon. Early check-in and late check-out are subject to availability. The minimum age to check in is 18, and all adult guests may be asked to show a valid government-issued photo ID at check-in."),
    ("Children and extra beds", "Children are welcome. Extra beds can be arranged on request and may be charged separately. Please share the number and ages of children when you book."),
    ("Jungle safaris and activities", "Jungle safaris are operated by the Forest Department, not by TripTree, and are charged separately and payable on arrival. Safari timings and availability are decided by the Forest Department and may change at short notice."),
    ("Wildlife and guest safety", "Our properties are close to forests and wildlife. For your safety, please follow staff instructions, do not feed or approach animals, avoid walking outside lit areas after dark and keep children supervised at all times."),
    ("Guest conduct and property", "Guests are responsible for any damage caused to the property during their stay. Please respect the local community and environment, keep noise to a minimum at night and dispose of waste responsibly."),
    ("Your information", f"Details you share through our contact and booking forms are used only to respond to your enquiry and manage your booking. We do not sell or share your information with third parties except where needed to fulfil your booking. To have your details removed, email us at {EMAIL}."),
]

def build_terms():
    half = (len(TERMS) + 1) // 2
    def acc(items, first):
        out = []
        for i, (q, a) in enumerate(items):
            active = ' active-block' if (first and i == 0) else ''
            cur = ' active' if (first and i == 0) else ''
            show = ' current' if (first and i == 0) else ''
            out.append(f'''
                            <li class="accordion block{active}">
                                <div class="acc-btn{cur}"><div class="icon-outer"><span class="icon icon-plus fa fa-plus"></span> <span class="icon icon-minus fa fa-minus"></span></div>{q}</div>
                                <div class="acc-content{show}"><div class="content"><div class="text">{a}</div></div></div>
                            </li>''')
        return "".join(out)
    body = page_title("Terms &amp; Conditions", IMG + "banner-lake.jpg") + f'''
    <section class="faq-section light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="mb_80">
                <div class="row">
                    <div class="col-lg-8">
                        <h5>These terms apply to all bookings made with {esc(BRAND)}.</h5>
                        <div class="text">Please read them before confirming your stay. If anything is unclear, call us on <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-6">
                    <div class="accordian-boxed style-two">
                        <ul class="accordion-box style-three">{acc(TERMS[:half], True)}
                        </ul>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="accordian-boxed style-two">
                        <ul class="accordion-box style-three">{acc(TERMS[half:], False)}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
'''
    write("terms-conditions.html", head(f"Terms & Conditions | {BRAND}",
          "Booking, payment, cancellation and stay terms for TripTree Resorts & Homestays.",
          "terms-conditions.html") + header("terms-conditions.html") + body + footer())

# ================================================================ 404 / THANK YOU
def simple_page(fname, title, h1, h2, text, desc, noindex=True):
    extra = '<meta name="robots" content="noindex">\n' if noindex else ''
    body = page_title(h1, IMG + "banner-lake.jpg") + f'''
    <section class="error-section light-bg mx-60 border-shape-top border-shape-bottom">
        <div class="auto-container">
            <div class="content text-center">
                <h2>{h2}</h2>
                <div class="text">{text}</div>
                <a href="index.html" class="theme-btn btn-style-one">Go to home page</a>
            </div>
        </div>
    </section>
'''
    write(fname, head(title, desc, fname, extra=extra) + header("") + body + footer())

def build_misc():
    simple_page("404.html", f"Page Not Found | {BRAND}", "404", "Sorry, that page can't be found",
                'The page you are looking for doesn\'t exist or may have moved. Try our <a href="properties.html">properties</a> or <a href="contact.html">contact us</a>.',
                "Page not found.")
    simple_page("thank-you.html", f"Thank You | {BRAND}", "Thank You", "We've received your message",
                f'Our team will get back to you shortly. For urgent queries, call us on <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a>.',
                "Thank you for contacting TripTree.")

def build_sitemap():
    pages = ["", "about.html", "properties.html"] + [p["slug"] + ".html" for p in PROPS] + \
            ["gallery.html", "booking.html", "contact.html", "terms-conditions.html"]
    urls = "\n".join(f"  <url><loc>{SITE}/{u}</loc></url>" for u in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nDisallow: /_archive/\nDisallow: /_build/\nDisallow: /inc/\n\nSitemap: {SITE}/sitemap.xml\n")

build_home(); build_about(); build_properties()
for p in PROPS: build_property(p)
build_gallery(); build_contact(); build_booking(); build_terms(); build_misc(); build_sitemap()
