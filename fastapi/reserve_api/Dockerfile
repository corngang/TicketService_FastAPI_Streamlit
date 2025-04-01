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
WORKDIR /TicketService_FastAPI_Streamlit/fastapi

# Move fastapi, streamlit_front directory and files
RUN mv -f /fastapi /TicketService_FastAPI_Streamlit
RUN mv -f /streamlit_front /TicketService_FastAPI_Streamlit/streamlit_front

# Install package from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set env
ENV PORT=8000

# Open port
EXPOSE 8000

# Run command in container
CMD ["python3", "reserve_api/reserve.py"]