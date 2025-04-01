FROM python:3.9-slim

# Update and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    vim \
    ssh \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy from github repository by corngang
ADD https://github.com/corngang/TicketService_FastAPI_Streamlit/archive/refs/heads/main.tar.gz main.tar.gz
RUN tar --strip-components=1 -xvf main.tar.gz
RUN rm -rf main.tar.gz

# Set working directory
WORKDIR /TicketService_FastAPI_Streamlit/streamlit_front

# Move fastapi, streamlit_front directory and files
RUN mv -f /fastapi /TicketService_FastAPI_Streamlit/fastapi
RUN mv -f /streamlit_front /TicketService_FastAPI_Streamlit

# Install package from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set env
ENV LOGIN_URL=http://login_auto:8000/login
ENV USER_URL=http://user_auto:8000/user
ENV RESERVE_URL=http://reserve_auto:8000/reserve
ENV VERIFY_URL=http://reserve_auto:8000/verify_user_info
ENV TICKET_INFO_URL=http://reserve_auto:8000/ticket

# Open port
EXPOSE 8501

# Run command in container
CMD ["streamlit", "run", "streamlit_mono.py", "--server.address=0.0.0.0", "--server.port=8501"]