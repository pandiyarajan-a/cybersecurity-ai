FROM kalilinux/kali-rolling

# Update package lists
RUN apt update --fix-missing

# Install packages in smaller groups to reduce memory pressure
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    nmap \
    libxml2-utils \
    python3-pip \
    git

# Install Metasploit separately (it's the largest package)
RUN DEBIAN_FRONTEND=noninteractive apt install -y metasploit-framework

# Install routersploit separately
RUN DEBIAN_FRONTEND=noninteractive apt install -y routersploit

# Clean up apt cache to free space
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Copy script into image
COPY scripts/connect_msf_postgres.sh /usr/local/bin/connect_msf.sh
RUN chmod +x /usr/local/bin/connect_msf.sh

WORKDIR /root
CMD ["/bin/bash"]


