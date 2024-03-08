# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Main Page</title>
#     <link rel="stylesheet" href="static/blog/css/styles.css">
#     <link rel="preconnect" href="https://fonts.googleapis.com">
#     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#     <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
# </head>
# <body>
# {% extends 'base.html' %}
# {% load static %}
# {% block content %}
# <section id="blog">
#     <div class="blog-heading">
#         <strong>Recent Blog</strong>
#         <h3>Our Blog</h3>
#     </div>
#     {% for post in object_list %}
#     <div class="blog-box-container">
#         <div class="blog-box">
#             <div class="blog-box-img">
#                 {% if post.header_image %}
#                     <img src="{{ post.header_image.url }}">
#                 {% endif %}
#                 <a href="{% url 'article-detail' post.pk %}" class="blog-img-link">
#                     <i class="fa-solid fa-arrow-up-right-from-square" style="margin-top: 16px"></i>
#                 </a>
#             </div>
#             <div class="blog-box-text">
#                 <strong class="category-name"><a href="{% url 'category' post.category|slugify %}">{{ post.category }}</a></strong>
#                 <p class="post-title">{{ post.title }}</p>
#                 <p>
#                 {% if post.snippet|length > 200 %}
#                     {{ post.snippet|slice:":200" }}...
#                 {% else %}
#                     {{ post.snippet }}
#                 {% endif %}
#                 </p>
#             </div>
#             <div class="blog-author" style="margin-right: 65px">
#                 <div class="blog-author-img">
#                     {% if post.author.profile.profile_pic %}
#                         <img src="{{ post.author.profile.profile_pic.url }}">
#                     {% else %}
#                         <img src="{% static 'blog/images/default_profile_pic.webp' %}" class="card-img" width="200" height="200">
#                      {% endif %}
#                 </div>
#                 <div class="blog-author-text">
#                     <strong>{{ post.author.first_name }} {{ post.author.last_name }}</strong>
#                     <span>{{ post.post_date }}</span>
#                 </div>
#             </div>
#         </div>
#     </div>
# </section>
#
# {% endfor %}
# {% endblock %}
# </body>
# </html>