# Gunakan image Python 3.12
FROM python:3.12-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install ping dan dependensi sistem
RUN apt-get update && \
    apt-get install -y iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Buat direktori kerja
WORKDIR /app

# Salin semua file ke container
COPY . .

# Install dependensi Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        rich \
        requests \
        bs4 \
        lxml \
        pyopenssl \
        getmac \
        pyyaml
      
# Salin file beta CLI
COPY beta /usr/local/bin/beta
RUN chmod +x /usr/local/bin/beta

# Jangan jalankan apa-apa secara otomatis
CMD ["bash"]
