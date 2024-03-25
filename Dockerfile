FROM python
WORKDIR /bot
COPY ./ /bot
RUN pip install update
RUN pip install -r requirements.txt



CMD python chatbot.py

