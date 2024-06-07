FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /api

# Copy the current directory contents into the container at /api
COPY . /api

# Install sudo and curl
RUN apt-get update && apt-get install -y sudo curl bash zsh git && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ls -lah / 
RUN ls -lah /api 
RUN pwd -P

# Install install_dotfiles script:
RUN mv /api/install_dotfiles /usr/bin/install_dotfiles && chmod +x /usr/bin/install_dotfiles

# Install rye from script
RUN chmod +x /api/install_rye && /api/install_rye

# Change over to zsh
SHELL ["/bin/zsh", "-c"]

# # Install any needed packages specified in requirements.txt
# RUN rm -rf /api/.venv && \
#     rye init && rye sync

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for the container (in this case, the name of the user)
ENV NAME World

# Run main.py when the container launches
CMD ["/api/.venv/bin/python", "/api/src/api/main.py"]