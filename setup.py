from setuptools import setup, find_packages

setup(
    name="screen-translator",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for capturing screen regions, extracting text via OCR, translating it, and displaying the result.",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pytesseract",
        "Pillow",
        "deep-translator",
        "tkinter",  # tkinter is usually included with Python, but you can specify it if needed
    ],
    entry_points={
        'console_scripts': [
            'screen-translator=main:translate_image',  # Adjust this if you want a specific entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)