import { Stomp } from "@stomp/stompjs";

export class RabbitMQConnection {
  constructor(addResult) {
    this.client = Stomp.over(new WebSocket("ws://127.0.0.1:15674/ws"));

    const onMessage = (message) => {
      addResult(JSON.parse(message.body));
      this.client.subscribe("/queue/result", onMessage);
    };
    const onConnect = () => {
      console.log("connected to ws");
      this.client.subscribe("/queue/result", onMessage);
    };
    const onError = () => console.error("error while connecting to ws");

    this.client.reconnect_delay = 5000;
    this.client.connect("guest", "guest", onConnect, onError);
  }

  sendRequest(phrase, path, fileTypes, searchModes) {
    const message = createMessage(phrase, path, fileTypes, searchModes);
    this.client.send(
      "/exchange/words/words." + getQueueName(searchModes),
      {},
      JSON.stringify(message)
    );
  }
}

function createMessage(phrase, path, fileTypes, searchModes) {
  return {
    phrase: phrase,
    path: directory,
    filters: {
      filterTypes: fileTypes,
      filterModes: searchModes,
    },
    words: phrase.split(' ')
  };
}

function getQueueName(searchModes) {
  return searchModes.length > 0 ? searchModes[0] : "scraper";
}
