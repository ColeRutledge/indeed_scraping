# docker build -t ubuntu1604py36
FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3.8 && apt-get install -y python3-pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN pip3 install pipenv

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron
COPY . .
RUN chmod 0744 test.py
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
RUN apt-get update
RUN apt-get -y install cron


# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log




######################################################################
# FROM selenium/standalone-chrome

# RUN sudo apt-get update && sudo apt-get install -y python3.8 && sudo apt-get install -y python3-pip

# RUN sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# COPY . .

# RUN sudo pip3 install pipenv

# RUN pipenv lock --requirements > requirements.txt && pip install -r requirements.txt

# # CMD [ "python3", "-u", "scrape.py" ]


# RUN sudo apt-get -y install cron

# # Copy hello-cron file to the cron.d directory
# COPY hello-cron /etc/cron.d/hello-cron

# # Give execution rights on the cron job
# RUN sudo chmod 777 /etc/cron.d/hello-cron
# RUN sudo chmod 777 /var/run

# # Apply cron job
# RUN crontab /etc/cron.d/hello-cron

# # Create the log file to be able to run tail
# RUN sudo touch /var/log/cron.log

# # Run the command on container startup
# # CMD sudo cron && sudo tail -f /var/log/cron.log
# CMD sudo cron -f
