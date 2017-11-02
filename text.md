I have recently started working on Django projects for my job at Truth Initiative. It's been fun. I have about 4 years of informal Python experience, but mostly with Python 2.7, and aside from a couple of tiny Django projects I have done to learn enough to get started, I have usually just used Python for scripting.

Lately also I have been following Linux from Scratch to build my own Linux kernel from source code. This project takes a very bottom-up approach to learning some of the Linux internals, and its unique learning path got me thinking what this would look like if applied to Django.

So I formulated a learning plan to take me from scratch to my own implementation of a subset of the Django framework.

The goal is to create a framework with no dependencies on Django that runs the same model, route, controller/view, and test code that works in Django.

I felt that the best way to propel this project along was to have in mind a finished project I wanted to implement in my own Django, so I chose something really, really simple that can be implemented in real Django with a very small set of Django features: a blog.

# The blog feature list

So what kind of blog do I want to create? A super, duper, simple one that is probably so basic it should not even be called a blog.

Here is the feature list for my "blog":

* A page with text on it
* Anonymous comments on the bottom

I do not expect this to be production ready. No one should use my Django for *anything* except learning. This means 

# The framework feature list

The key to making this project plausible for one person seems to lie in choosing a suitably tiny set of Django features to implement, so I settled on the following list:

* WSGI integration
* Models
* Fields
* Routes
* Views
* Templates
* Tests

Unfortunately this list is hilariously expansive. It could cover almost everything in Django if interpreted loosely.

Some of the only things glaringly absent from this list are Django settings files and the `manage` commands. And while I will need some bits of each of the above features, Django is made to support many wildly different, and much bigger, projects. For instance, there are *lots* of built-in Django Field types. In fact, 27 are documented in the official [Django 1.11 Field docs](https://docs.djangoproject.com/en/1.8/ref/models/fields/) alone.

So this this list needs to be narrowed down to the parts of each feature I actually need.

(This is now me from the future talking.) But of course, the problem with narrowing down this feature list was that I kind of didn't know what parts of these Django features I would actually need to create the blog. I had some ideas. Out of the available Django Fields, I knew I would need a TextField, a CharField, and an auto-incrementing automatic PK field, but I did not know whether I had missed big features or how to describe/name some of the things I needed.

Below is the same list of features, narrowed down to the parts of those features I actually implemented:

* WSGI integration
* Models
* Fields
* Routes
* Views
* Templates
* Tests

# The technical approach

My plan is to create my blog in Django 1.11, on Python 3.6.1, in a Docker container running Nginx in front of Gunicorn. I will make sure I have re-implemented the Django blog by creating a supporting unit test suite in Django that makes heavy use of a non-Django mock library, as well as one or two very simple headless browser automated tests using a non-Django testing framework. I will then bring this same test code into a new, blank project inside a new Docker image, and start writing code until the unit tests run (I need a test runner!), and, ultimately, pass. Then I will start on making sure the automated browser tests pass.

While satisfying each test, I will try to do as much coding as possible without referring to the Django source, but the point of this is to learn about Django's pieces, so I will refer to the Django source often to document differences between the two implementations, particularly noting places where Django does stuff in more abstract ways that support the full-fledged framework but are too abstract to make my project feasible.

# A little more on the tech

I will not support multiple database backends. For simplicity, I will do a really dumb thing and support only SQLite (which is even dumber inside a Docker container).

As part of not supporting the Django `manage` commands, I will not have Django serve static assets such as images, JS, and CSS. Any of those will be served by Nginx in the same way for both the Django app and my app.

Docker will be useful in helping me create an image that runs the same Nginx/Gunicorn configuration for both apps, forcing me to adhere to that interface in my Django. The two containers will only differ in the files copied or mounting into the application filesystem tree.

# The source code

I am tracking this whole thing in a git repository hosted on GitHub [here](https://github.com/eppeters/djangofromscratch).
