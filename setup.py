#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name="recon-backend",
    author="recon Backenders",
    author_email="mail@gmail.com",
    description="recon system",
    long_description=open("README.md").read(),
    url="http://gitlab.com/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "Django==5.0.6",
        "requests>=2.32.3",
        "psycopg2-binary==2.9.9",
        "djangorestframework==3.15.1",
        "django-filter==24.2",
        "pytz==2024.1",
        "gunicorn==22.0.0",
        "boto3==1.34.127",
        "django-cors-headers==4.3.1",
        "django_rest_passwordreset==1.4.1",
        "djangorestframework-simplejwt==5.3.1",
        "python-magic==0.4.27", # identifies file types
        "django-extensions==3.2.3",
        "drf-spectacular==0.27.2",
        "PyJWT==2.9.0",
        "django-storages==1.14.4",

    ],
    zip_safe=False,
)
