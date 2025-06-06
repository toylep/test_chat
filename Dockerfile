FROM python:3.13-slim


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    default-libmysqlclient-dev \
    build-essential \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev \
    libzbar-dev \
    ldap-utils \
    curl \
    openssh-server \
    apt-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*e~

# configure ssh server
RUN passwd -d root
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config

COPY . /srv/app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /srv/app
RUN pip install uv


RUN uv pip install -r pyproject.toml
