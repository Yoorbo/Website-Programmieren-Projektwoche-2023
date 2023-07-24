def programmierprojektmain(request):
    # Get the template directory path
    template_directory = os.path.join(settings.BASE_DIR, 'templates', 'pages', 'programmierprojekt')

    # Get a list of all files in the template directory
    files_in_directory = os.listdir(template_directory)

    # Extract filenames without extensions
    files_without_extension = [os.path.splitext(file)[0] for file in files_in_directory]

    # Exclude the "mainpage" itself from the list
    files_without_mainpage = [file for file in files_without_extension if
                              file not in ["mainpage", "janhasan2", "janhasan3"]]

    # List to store tuples of file name and first h1 title
    files_with_titles = []

    # Parse each HTML file to get the title
    for file in files_without_mainpage:
        file_path = os.path.join(template_directory, file + '.html')
        with open(file_path, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

            # Try to find the first non-empty title element
            title_tag = soup.find(['h1', 'title'])
            title = title_tag.text.strip() if title_tag else 'Website'

            files_with_titles.append((file, title))

    random.shuffle(files_with_titles)

    # Pass the list with filenames and their first h1 titles as a context variable to the template
    context = {
        'files_list': files_with_titles,
    }

    return render(request, "pages/programmierprojekt/mainpage.html", context)


def programmierprojektpages(request, slug):
    return render(request, f"pages/programmierprojekt/{slug}.html", {})


def pages(request):
    """
    This function pages(request) takes a request object as input and returns an HTTP response object. The function is
    responsible for rendering the appropriate HTML template file or static file based on the request path.

    The function first creates an empty dictionary object called context.

    It then attempts to load the template based on the request path. If the path ends with .html, it attempts to load
    the template file using Django's loader module. If the template file exists, it renders the template using the
    context dictionary and returns an HTTP response with the rendered HTML. If the template file does not exist,
    it attempts to load a static file using the path.

    If the path does not end with .html, it first checks if the path ends with a slash. If it does not, it attempts
    to load the index.html file in the same directory as the path. If the path ends with a slash, it loads the
    index.html file in the same directory as the path.

    If loading the template or static file fails, the function attempts to render an error template. If a
    TemplateDoesNotExist exception is raised, it attempts to load the static file based on the request path. If
    loading the static file fails, it renders a 404 error template. If any other exception is raised, it renders a
    500 error template.

    Overall, this function serves as a catch-all for rendering HTML and static files, and error templates in the case
    of failures.
    """
    context = {}
    try:
        try:
            load_template = request.path.replace("/", "", 1)
            context['segment'] = load_template
            if '.html' in load_template:
                html_template = loader.get_template(load_template)
                return HttpResponse(html_template.render(context, request))
            else:
                if load_template[-1] != '/':
                    html_template = loader.get_template(load_template + '/index.html')
                    return HttpResponse(html_template.render(context, request))
                else:
                    html_template = loader.get_template(load_template + 'index.html')
                    return HttpResponse(html_template.render(context, request))

        except template.TemplateDoesNotExist:
            try:
                load_path = f"static{request.get_full_path()}"
                if load_path.endswith(".js"):
                    return FileResponse(open(load_path, 'rb'), content_type='text/javascript')
                return FileResponse(open(load_path, 'rb'))
            except:
                html_template = loader.get_template('pages/errors/page-404.html')
                return HttpResponse(html_template.render(context, request))
    except:

        html_template = loader.get_template('pages/errors/page-500.html')
        return HttpResponse(html_template.render(context, request))
