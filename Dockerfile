FROM python
WORKDIR /bot
COPY ./ /bot
RUN pip install update
RUN pip install -r requirements.txt




ARG BOT_TOKEN
ARG COSMOSDB_URL
ARG COSMOSDB_KEY

ENV BOT_TOKEN=${BOT_TOKEN}
ENV COSMOSDB_URL=${COSMOSDB_URL}
ENV COSMOSDB_KEY=${COSMOSDB_KEY}

CMD python chatbot.py

