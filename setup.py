from setuptools import setup, find_packages

setup(
    name="beta",  # Nama aplikasi
    version="1.0.0",  # Versi aplikasi
    packages=find_packages(),  # Otomatis mencari paket di dalam folder
    py_modules=["beta"], 
    install_requires=[
        "rich",
        "requests",
        "bs4",
        "lxml",
    ],
    entry_points={
        'console_scripts': [
            'beta=beta:main', 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',  # Versi Python minimum
    author="sh4dowByte",  # Nama pembuat aplikasi
    author_email="Ahmad Juhdi <ahmadjuhdi007@gmail.com>",  # Email pembuat (opsional)
    description="Beta - A Python tool for scanning and information gathering",  # Deskripsi singkat
)
